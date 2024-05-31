import os
import time
import logging
from typing import Type

import streamlit.components.v1 as components
from streamlit.web.server.websocket_headers import _get_websocket_headers
import requests
import json
import subprocess
import threading
import validators
from aiohttp import web
import base64

from .utils import is_localhost, is_web_link, replace_host, is_server_alive
from .server_managers import ServerManagerBase, ServerManager
from .viewer import TrameBackend
from .TrameViewer import TrameViewer
from streamlit_pyvista.server_managers.ServerMessageInterface import ServerMessageInterface, EndpointsInterface

root_logger = logging.getLogger("solidipes")
root_logger.propagate = True
root_logger.setLevel(logging.INFO)
if "FULL_SOLIDIPES_LOG" not in os.environ:
    root_logger.setLevel(logging.INFO)


class MeshViewerComponent:
    """Streamlit component to display 3d mesh using pyvista and it's Trame backend"""

    def __init__(self, mesh_path: str | list[str] = None,
                 server_url: str = "http://127.0.0.1:8080",
                 setup_endpoint: str = "/init_connection",
                 server_manager_class: Type[ServerManagerBase] = ServerManager,
                 trame_viewer_class: Type[TrameBackend] = TrameViewer):

        # If the user specified only the path of one file, transform it to an element in a list
        if isinstance(mesh_path, str):
            mesh_path = [mesh_path]

        self.manager = server_manager_class
        self.viewer = trame_viewer_class()


        self.check_valid_input_files(mesh_path)
        self.mesh_path = mesh_path
        self.sequence_size = len(mesh_path)

        self.width = 1200
        self.height = 900

        self.server_url = server_url
        self.server_timeout = 1
        self.max_retries = 3

        # Set all attribute related to the dynamic endpoints settings.
        # Set the default required endpoints,
        # select mesh is used to ask the server to show a specific mesh and host is the host of the data rendering
        self.required_endpoints = ["select_mesh", "upload_mesh", "host"]
        # Dict that will contained value received for our endpoints. Init connection is the default endpoint to
        # request the server to give use all it's required endpoints
        self.endpoints = {
            ServerMessageInterface.InitConnection: setup_endpoint,
            ServerMessageInterface.Host: self.server_url
        }

        # If the default server url is on localhost we launch the server locally
        if is_localhost(self.server_url):
            self.setup_server()

        # Set up the endpoints
        self.setup_endpoints()
        self.set_mesh()

        root_logger.info("MeshViewer Created")

    def check_valid_input_files(self, list_of_path):
        """ Take a path and a sequence_size and check that each file of the sequence exists.
        If it does not it outputs an error message """
        for i in range(len(list_of_path)):
            if is_web_link(list_of_path[i]):
                if not validators.url(list_of_path[i]):
                    root_logger.error(f"The link {list_of_path[i]} is not valid")
                continue
            if not os.path.isabs(list_of_path[i]):
                list_of_path[i] = f"{os.getcwd()}/{list_of_path[i]}"
            if not os.path.exists(list_of_path[i]):
                root_logger.error(f"The file {list_of_path[i]} does not exists")

    def setup_server(self):
        """ Launch a local server using python subprocess on another thread. If a Trame server isn't already running """

        if is_server_alive(self.server_url, self.server_timeout):
            return
        trame_viewer_thread = threading.Thread(target=self.run_server_manager)
        trame_viewer_thread.start()
        root_logger.info("Local Trame Server Launched")

    def setup_endpoints(self):
        """ Fill the endpoints dictionary with the info received from the server """
        # If the server was launched locally, we need to wait for it to be up
        print("SETTING ENDPOITNS")
        self.wait_for_server_alive()
        print("FINISH TO WAIT")
        base64_bytes = base64.b64encode(self.viewer.get_viewer_file_content())
        request_body = {ServerMessageInterface.ViewerField: base64_bytes.decode('utf-8')}
        
        print(f"Making request to {self.server_url + self.endpoints[ServerMessageInterface.InitConnection]}")
        res = requests.get(self.server_url + self.endpoints[ServerMessageInterface.InitConnection],
                           json=json.dumps(request_body), timeout=20)

        try:
            json_res = res.json()
        except json.JSONDecodeError as e:
            root_logger.error("Invalid server response")
            return

        # Check that all necessary endpoints where given in the request and fill the endpoints Dict
        for endpoint in self.required_endpoints:
            if endpoint not in json_res:
                root_logger.error(f"ERROR, the endpoint {endpoint} was not specified by the server")
                continue
            self.endpoints[endpoint] = json_res[endpoint]

    def run_server_manager(self):
        """ Launche a Trame server using python subprocess """
        try:
            subprocess.run(["python3", self.manager.get_launch_path()],
                           # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, # Comment this line to debug this subprocess call
                           check=True)
        except subprocess.CalledProcessError as e:
            root_logger.error("It seems like the server crashed")

    def wait_for_server_alive(self):
        """ Try to ping the server to see if it is up  """
        init_time = time.time()
        attempt = 0
        print("CHEKING ", self.endpoints["host"])
        while not is_server_alive(self.endpoints["host"]) and attempt <= self.max_retries:
            if time.time() - init_time >= self.server_timeout:
                init_time = time.time()
                self.setup_server()
                attempt += 1

    def set_mesh(self, meshes=None):
        """ 
            Set the mesh viewed on the server by making a request 
        
        Args:
            meshes (list[str]): List of paths to the meshes to display
        """
        print("-------- ENPOINTS ----------")
        print(self.endpoints)
        if meshes is None:
            meshes = self.mesh_path.copy()
        if "select_mesh" not in self.endpoints:
            return
        url = self.endpoints["host"] + self.endpoints["select_mesh"]
        data = {
            "mesh_path": meshes,
            "nbr_frames": len(meshes),
            "width": self.width,
            "height": self.height
        }
        headers = {"Content-Type": "application/json"}
        print("-------- SET MESH -----------")
        print(url)
        # Check in the response if any action is necessary such as make the iframe bigger or uploading files
        response = requests.get(url, data=json.dumps(data), headers=headers, timeout=2000)

        try:
            resp_body = response.json()

            if response.status_code == 400:
                if "error" in resp_body:
                    root_logger.error(resp_body["error"])
            else:
                if "request_space" in resp_body:
                    self.height = resp_body["request_space"]
                elif "request_files" in resp_body:
                    missing_files = resp_body["request_files"]
                    self.send_missing_files(missing_files)

        except requests.exceptions.JSONDecodeError:
            return

    def send_missing_files(self, missing_files):
        for file, index in missing_files:
            request_body = {}
            if file in self.mesh_path:
                with open(file, 'rb') as f:
                    content = f.read()
                base64_bytes = base64.b64encode(content)
                request_body[file] = (base64_bytes.decode('utf-8'), index)

                url = self.endpoints["host"] + self.endpoints["upload_mesh"]
                headers = {"Content-Type": "application/json"}
                requests.get(url, data=json.dumps(request_body), headers=headers, timeout=2000)

    def show(self):
        """ Render the streamlit component """
        headers = _get_websocket_headers()
        host = headers.get("Host")
        if host is not None and not is_localhost(host) and is_localhost(self.server_url):
            iframe_host =  replace_host(self.endpoints["host"], host)
        else:
            iframe_host = self.endpoints["host"]
        url = iframe_host + "/index.html"
        return components.iframe(url, height=self.height)
