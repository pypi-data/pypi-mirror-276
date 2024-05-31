import pyvista as pv
import argparse
from pyvista.trame.ui import plotter_ui
from trame.app import get_server
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html
from aiohttp import web
from trame.decorators import TrameApp, change, controller
import validators
import base64

import logging
import os
import numpy as np
import time, threading
import asyncio
from abc import ABC, abstractmethod
from typing import Dict

from streamlit_pyvista.server_managers.ServerMessageInterface import ServerMessageInterface, EndpointsInterface
from streamlit_pyvista.utils import (is_web_link, save_mesh_content_from_url, update_cache,
                                     save_mesh_content, save_mesh_content_from_file)

root_logger = logging.getLogger("streamlit_pyvista")
root_logger.propagate = True
root_logger.setLevel(logging.INFO)


class TrameBackend(ABC):
    """ A Trame server class that manage the view of a 3d mesh and its controls """

    def __init__(self, mesh=None, plotter=None, server=None, port=8080, host="0.0.0.0"):
        root_logger.info("Server started")
        pv.OFF_SCREEN = True
        self.host = host
        self.exposed_host = "127.0.0.1"

        if server is None:
            self.server = get_server(port=port)
        else:
            self.server = server

        self.path = None
        self.mesh = None
        self.clean_mesh = None
        self.cache_path = ".streamlit-pyvista-cache"

        self.style = {
            "background-color": "black",
            "font-color": "white"
        }

        self.pl = self.setup_pl()

        # Setup server lifecycle callback functions
        setattr(self, "on_server_bind", self.server.controller.add("on_server_bind")(self.on_server_bind))
        setattr(self, "on_client_exited", self.server.controller.add("on_client_exited")(self.on_client_exited))
        setattr(self, "on_client_connected",
                self.server.controller.add("on_client_connected")(self.on_client_connected))
        setattr(self, "on_server_exited", self.server.controller.add("on_server_exited")(self.on_server_exited))

        self.client_counter = 1
        threading.Timer(3, self.client_counter_cb).start()
        threading.Timer(60 * 5, self.stop_server).start()

        # Setup api endpoints
        self.my_routes = [
            web.get(EndpointsInterface.SelectMesh, self.change_mesh),
            web.get(EndpointsInterface.InitConnection, self.init_connection),
            web.get(EndpointsInterface.UploadMesh, self.upload_mesh),
            web.get(EndpointsInterface.ClientsNumber, lambda x: web.json_response(
                {ServerMessageInterface.NumberClientsField: self.client_counter}, status=200)),
            web.get(EndpointsInterface.KillServer, self.kill_server),
        ]
        self.mesh_missing = None
        self.sequence_bounds = [0, 0]
        self.setup_state()

        self.mesh_array = None
        self.width = 800
        self.height = 900
        self.ui = self.build_ui()

    def client_counter_cb(self):
        self.client_counter -= 1

    async def kill_server(self, request):
        await self.server.stop()
        return web.json_response({"success": "Server killed"}, status=200)

    async def stop_server(self):
        if self.client_counter == 0:
            await self.server.stop()
        else:
            threading.Timer(60 * 5, self.stop_server).start()

    def setup_pl(self) -> pv.Plotter:
        """ Setup all class attributes related to the pyvista Plotter """
        # Create the plotter and add its styles
        pl = pv.Plotter()
        pl.background_color = self.style["background-color"]
        pl.theme.font.color = self.style["font-color"]
        self.bounds_scalar = None
        self.scalar_bar_mapper = None
        return pl

    @abstractmethod
    def setup_state(self):
        """ Set up all the state variables to initial values """
        pass

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    def update_mesh_from_index(self, idx):
        """
        Update the mesh displayed in the plotter using its index in the sequence
        Args:
            idx: an int setting the index of the mesh to show
        """
        if self.mesh_array is not None:
            if idx < self.sequence_bounds[1]:
                self.clean_mesh = self.mesh_array[idx]
                self.replace_mesh(self.mesh_array[idx])

    def handle_new_mesh(self, mesh_path):
        """
        This function handles the loading of new mesh in the server
        Args:
            mesh_path: the path of the mesh
        """
        self.mesh_array = []
        missing_mesh = []
        # If the mesh is a sequence, then format its path and load all element in the mesh array
        for i, path in enumerate(mesh_path):
            saved_path = f"{self.cache_path}/{path.split('/')[-1]}"
            # If the path is a link, call function to cache download and store the mesh
            if is_web_link(path):
                if not validators.url(path):
                    root_logger.error(f"The link {path} is not valid")
                    self.mesh_array.append(None)
                    continue
                path = save_mesh_content_from_url(path, saved_path, decimate=True)
                if not path:
                    root_logger.error(f"An error occurred when fetching link {mesh_path[i]}")
                    continue

            elif not os.path.exists(path):
                # If the file does not exist mark it as missing to notify it in the response
                missing_mesh.append((path, i))
                self.mesh_array.append(None)
                continue
            else:
                # If the file exists, cache it also to allow for all decimation features
                path = save_mesh_content_from_file(path, saved_path, decimate=False)
            self.mesh_array.append(pv.read(path))
        return missing_mesh

    async def change_mesh(self, request):
        """
        This function is called when a request to '/select_mesh' is made
        Args:
            request: the request received

        Returns:
            a http status 200 if there was no error, else a http status 400
        """
        request_body: Dict[str, str] = await request.json()
        # Retrieve information from the request
        self.path = request_body.get("mesh_path", None)
        self.width = request_body.get("width", self.width)
        self.height = request_body.get("height", self.height)
        self.sequence_bounds[1] = request_body.get("nbr_frames", self.sequence_bounds[1])
        if self.path is None:
            root_logger.error("No filepath found in the change mesh request")
            return web.json_response({"error": "No filepath found in the change mesh request"}, status=400)

        # Reset the viewer to an empty state
        self.clear_viewer()

        # Get the mesh and prepare it to be displayed
        self.mesh_missing = self.handle_new_mesh(self.path)
        if len(self.mesh_missing) > 0:
            root_logger.info(f"Missing mesh: {self.mesh_missing}, request made to client")
            return web.json_response({"request_files": self.mesh_missing}, status=200)
        if len(self.mesh_array) == 0:
            root_logger.error("None of the mesh passed as argument seemed to be working properly")
            return web.json_response({"error": "No valid path passed"}, status=400)

        self.handle_new_mesh_request()
        # If the height allocated by the streamlit component, ask for more space in the response of the request
        response_body = {}
        # if self.height - self.estimate_controller_height()[1] < 700:
        #     response_body["request_space"] = 1.65 * self.height
        return web.json_response(response_body, status=200)

    def handle_new_mesh_request(self):

        self.replace_mesh(self.mesh_array[0])

        # Prepare ui elements that depends on the mesh
        self.state.options = self.mesh_array[0].array_names.copy()
        self.state.options.insert(0, "None")
        self.state.options_warp = self.state.options.copy()

        # Show the new mesh in the viewers and its controls
        self.computes_bounds_scalar()
        self.update_ui()
        self.pl.reset_camera()


    async def upload_mesh(self, request):

        request_body: Dict[str, str] = await request.json()
        for key, (encoded_content, index) in request_body.items():
            content = base64.b64decode(encoded_content)
            loc = save_mesh_content(content, f"{self.cache_path}/{key}")
            self.mesh_array[index] = pv.read(loc)
            self.mesh_missing.remove((key, index))

        if self.mesh_missing is None or len(self.mesh_missing) == 0:
            self.handle_new_mesh_request()

        return web.json_response({"success": "Mesh uploaded successfully"}, status=200)

    def compute_field_interval(self, field=None):
        """
        Compute the min and max of a field of vector over all it's frame ot get the all-time min and max to get the upper
        and lower bound of the scalar bar
        Args:
            field: the field you want to compute the bounds

        Returns: (min, max), it returns a tuple with the min and max

        """
        # If the field is None get the default field on which to compute the min and max
        if field is None:
            field = self.state.mesh_representation
        if field is None or field == "None":
            field = self.state.options[1]
        # Loop over all the images and find the max of the array and the min
        max_bound = -np.inf
        min_bound = np.inf
        for i in range(self.sequence_bounds[1]):
            l_max = self.mesh_array[i].get_array(field).max()
            l_min = self.mesh_array[i].get_array(field).min()
            if l_max > max_bound:
                max_bound = l_max
            if l_min < min_bound:
                min_bound = l_min
        return min_bound, max_bound

    def computes_bounds_scalar(self):
        """ Compute the bounds of all the scalars of the mesh and store it in an attribute
        to avoid doing all the computation everytime a bar is shown """
        if self.state.options is None:
            return

        # Store bounds and mapper for all the fields available except "None" which is the first one of the options array
        self.bounds_scalar = {}
        for field in self.state.options[1:]:
            self.bounds_scalar[field] = self.compute_field_interval(field)

    @abstractmethod
    def replace_mesh(self, new_mesh):
        """
            Change the mesh displayed in the plotter and its related data
            Args:
                new_mesh: the new mesh to display
        """
        pass

    @abstractmethod
    def clear_viewer(self):
        """ Reset the viewer and its related attribute to an empty viewer """
        pass
    @abstractmethod
    def build_ui(self):
        """
        Build all the ui frontend with all different components
        Returns:
            a VAppLayout for the server
        """
        pass

    @abstractmethod
    def update_ui(self):
        """ Force to redraw the ui """
        pass

    def start_server(self):
        """ Start the server """

        self.server.start(host=self.host)

    def on_server_bind(self, wslink_server):
        """
        When the server is bind, add api endpoint to it and update the cache
        Args:
            wslink_server: the socket manager of the server
        """
        # Update the cache
        update_cache(self.cache_path)
        root_logger.info("Server endpoints were bind")
        wslink_server.app.add_routes(self.my_routes)

    def on_client_exited(self):
        self.client_counter -= 1
        root_logger.info(f"A client disconnected, there are {self.client_counter} clients connected")

    def on_client_connected(self):
        self.client_counter += 1
        root_logger.info(f"A client connected, there are {self.client_counter} clients connected")

    def on_server_exited(self, **kwargs):
        root_logger.info("Server stopped")
        update_cache(self.cache_path)

    async def init_connection(self, request):
        """
        Base api endpoint on '/init_connection' to inform the client of all the endpoints available and their locations
        Args:
            request: the request made to this endpoint

        Returns:
            a json with all information about endpoints required and a success status 200
        """
        response_body = {
            ServerMessageInterface.SelectMesh: EndpointsInterface.SelectMesh,
            ServerMessageInterface.UploadMesh: EndpointsInterface.UploadMesh,
            ServerMessageInterface.Host: f"{EndpointsInterface.Protocol}://{self.exposed_host}:{self.server.port}"
        }
        root_logger.info("Connection was initiated")
        return web.json_response(response_body, status=200)

    @staticmethod
    @abstractmethod
    def get_launch_path():
        pass

    def get_viewer_file_content(self):
        with open(self.get_launch_path(), "rb") as f:
            return f.read()





