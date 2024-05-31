import json
import time
from shutil import copyfile


from flask import Flask, make_response, request
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import requests
import base64
import hashlib

import os
import threading
from abc import ABC, abstractmethod
from streamlit_pyvista.utils import (find_free_port, is_server_available,
                                                     is_server_alive, wait_for_server_alive, ServerItem)
from streamlit_pyvista.server_managers.ServerMessageInterface import ServerMessageInterface, EndpointsInterface
import logging
from streamlit_pyvista import ROOT_URL

root_logger = logging.getLogger("streamlit-server-manager")
root_logger.propagate = True
root_logger.setLevel(logging.INFO)


class ServerManagerBase(ABC):
    """ This class is the base for any ServerManager implementation """

    def __init__(self, host="0.0.0.0", port=8080, ) -> None:
        self.app = Flask(__name__)
        # register API endpoints
        self.app.add_url_rule(EndpointsInterface.InitConnection, "init_connection", self.init_connection)
        self.app.add_url_rule(ROOT_URL + EndpointsInterface.InitConnection, "init_connection", self.init_connection)

        self.servers_running = []
        self.host = host
        self.port = port
        self.viewer_runner_script = None

        self.viewer_dir = "viewers"
        os.makedirs(self.viewer_dir, exist_ok=True)
        # Set up a scheduler used to periodically kill servers that are not in use
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self._lifecycle_task_kill_server, 'interval',
                               kwargs={"servers_running": self.servers_running}, seconds=30, max_instances=2)

    @abstractmethod
    def init_connection(self):
        """
        This function receive request of clients that require a trame server to display meshes. It's in this class that
        we need by any means start a trame server and get its endpoints
        Returns:
            return a response containing a json with all required endpoint for a MeshViewerComponent to work properly
        """
        pass

    def run_server(self):
        """ Start the flask server and the scheduler """
    
        self.scheduler.start()
        self.app.run(host=self.host, port=self.port, debug=True, use_reloader=False)
    

    @staticmethod
    @abstractmethod
    def get_launch_path():
        """
        This function must be used to get the path to the file of the manager that will be launched
        Returns:
            the path to the file that launche the server
        """
        pass

    def find_available_server(self, type):
        """
        Check in the servers_running attribute if any server is there idling if it's the case it return
        the address of this server
        Returns:
            The address of idling server, if none is found return None
        """
        for server in self.servers_running:
            if type == server.type and is_server_alive(server.host) and is_server_available(server):
                self.servers_running.remove(server)
                return server
        return None

    def _lifecycle_task_kill_server(self, servers_running):
        """
        Task executed periodically by the scheduler to kill all unused server
        Args:
            servers_running: A list of server currently running

        Returns:
            The server that were killed
        """
        elements_to_remove = []
        for server in servers_running:
            if is_server_alive(server.host) and is_server_available(server):
                try:
                    requests.get(f"{server.host}/kill_server", timeout=1)
                except requests.exceptions.Timeout:
                    pass
                elements_to_remove.append(server)
        for el in elements_to_remove:
            print(f"REMOVE VIEWER WITH PATH {el.path}")
            if el.path is not None and os.path.exists(el.path):
                os.remove(el.path)
            servers_running.remove(el)
        return elements_to_remove


def run_trame_viewer(server_port, file_path):
    """ Launch a Trame server using python subprocess """
    try:
        # p = f"{os.path.dirname(ServerManager.get_launch_path())}/docker_dir"
        # copyfile(file_path, f"{p}/tmp_viewer.py")
        #
        # subprocess.run(
        #     ["docker", "build", "-t", f"viewer:{file_path.split('/')[-1]}", p],
        #     # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        #     check=True)
        # subprocess.run(
        #     ["docker", "run", "-rm", "-p", f"{server_port}:3000", f"viewer:{file_path.split('/')[-1]}"],
        #     # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        #     check=True)
        subprocess.run(
            ["python3", file_path,
             "--server", "--port", str(server_port)],
            # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            check=True)
    except subprocess.CalledProcessError as e:
        root_logger.error(f"The server running on port {server_port} crashed")


class ServerManager(ServerManagerBase):
    """ Implementation of a ServerManagerBase to run trame viewer locally """

    def __init__(self, host="0.0.0.0", port=8080):
        super().__init__(host, port)
        self.timeout = 20

    def init_connection(self):

        req = json.loads(request.json)
        file_content = req.get(ServerMessageInterface.ViewerField, None)
        if file_content is None:
            return make_response({"Viewer missing": "You should include the content of your viewer "
                                                    "class file in the init_connection request"}, 400)

        file_content = base64.b64decode(file_content)
        checksum = hashlib.sha256(file_content).hexdigest()

        # Check if any server already running is available and if one was found use it and response with its endpoints
        available_server = self.find_available_server(checksum)
        if available_server is not None:
            self.servers_running.append(available_server)
            r = requests.get(
                f"{available_server.host}{EndpointsInterface.InitConnection}")
            return make_response(r.content, 200)

        port = find_free_port()

        file_path = f"{self.viewer_dir}/viewer_{port}.py"
        with open(file_path, "wb") as f:
            f.write(file_content)
        # Run the trame server in a new thread
        threading.Thread(target=run_trame_viewer, args=[port, file_path]).start()
        # Wait for server to come alive
        print("WAITINGFOR SERVER TO COME ALIVE")
        wait_for_server_alive(f"{EndpointsInterface.Localhost}:{port}", self.timeout)
        # Get endpoints of the server
        print(f"Making request to {EndpointsInterface.Localhost}:{port}{EndpointsInterface.InitConnection} from manager")
        res = requests.get(f"{EndpointsInterface.Localhost}:{port}{EndpointsInterface.InitConnection}").json()
        self.servers_running.append(ServerItem(res[ServerMessageInterface.Host], checksum, file_path))
        print("RECEIVED RESPONSE")
        return make_response(res, 200)

    @staticmethod
    def get_launch_path():
        return os.path.abspath(__file__)


if __name__ == "__main__":
    server_manager = ServerManager()
    server_manager.run_server()
