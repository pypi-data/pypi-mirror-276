import threading
import subprocess
import logging
import json
import base64
import hashlib
import ipaddress

import requests
from flask import Flask, request, make_response
from flask_sock import Sock

import os
from streamlit_pyvista import ROOT_URL
from streamlit_pyvista.server_managers.ServerManager import ServerManagerBase
from streamlit_pyvista.utils import (find_free_port, is_server_available, is_server_alive,
                                                     wait_for_server_alive, ServerItem)
from streamlit_pyvista.server_managers.ServerMessageInterface import ServerMessageInterface, EndpointsInterface

root_logger = logging.getLogger("streamlit-server-manager")
root_logger.propagate = True
root_logger.setLevel(logging.INFO)


def run_trame_viewer(server_port, file_path):
    """ Launch a Trame server using python subprocess """
    try:
        print(os.listdir())
        print(os.getcwd())
        
        print(f"Trying to start {file_path} on port {server_port}")
        subprocess.run(["python", file_path,
                        "--server", "--port", str(server_port)],
                       # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       check=True)  # stdout=subprocess.DEVNULL,  stderr=subprocess.DEVNULL,
    except subprocess.CalledProcessError as e:
        print("An error occured")


class ServerManagerProxyfied(ServerManagerBase):
    """ Implementation of ServerManagerBase that make use of a proxy for remote connection """
    def __init__(self, host="0.0.0.0", port=8080, proxy_host="127.0.0.1", proxy_port=5000):
        super().__init__(host, port)

        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.base_url = ROOT_URL

    def init_connection(self):
        print("REQUEST FOR INIT CO", request.url)
    
        self.proxy_host = request.headers.get("Host").split(":")
        if len(self.proxy_host) > 1:
            self.proxy_host[1] = str(self.proxy_port)
            self.proxy_host = ":".join(self.proxy_host) 
        else:
            self.proxy_host = self.proxy_host[0]     
        print("Pass Header", self.proxy_host)
        if request.is_json:
            req = json.loads(request.json)
        else:
            return make_response({"Invalid format": "init_connection expected a json with field 'Viewer' "})
        print("Pass Json fecth")
        file_content = req.get(ServerMessageInterface.ViewerField, None)
        
        if file_content is None:
            return make_response({"Viewer missing": "You should include the content of your viewer "
                                                    "class file in the init_connection request"}, 400)

        print("Extract content")
        file_content = base64.b64decode(file_content)
        checksum = hashlib.sha256(file_content).hexdigest()
        print("Get checksum")
        # Check if any server already running is available and if one was found use it and response with its endpoints
        available_server = self.find_available_server(checksum)
        # Get the remote proxy host
        print("CHECK I SERVER AV")
        
        if available_server is not None:
            
            self.servers_running.append(available_server)
            res = requests.get(f"{available_server.host}/init_connection").json()
            print("Host", self.proxy_host)
            print("URL COMPUTED", f"http://{self.proxy_host}{self.base_url}/server/{available_server.host.split('/')[-1]}")
            res["host"] = f"http://{self.proxy_host}{self.base_url}/server/{available_server.host.split('/')[-1]}"
            return make_response(res, 200)

        print("No server av")

        port = find_free_port()
        print("Found free port")
        file_path = f"{self.viewer_dir}/viewer_{port}.py"
        with open(file_path, "wb") as f:
            f.write(file_content)
        print("Written the trame file")
        print(file_path)
        # Run the trame server in a new thread
        threading.Thread(target=run_trame_viewer, args=[port, file_path]).start()
        # Wait for server to come alive
        wait_for_server_alive(f"{EndpointsInterface.Localhost}:{port}", timeout=10)
        print("Server launch")
        res = requests.get(f"{EndpointsInterface.Localhost}:{port}/init_connection")
        print(res.content)
        res = res.json()
        # Add the new server to the proxy server list
        print("making request at ", f"{EndpointsInterface.Localhost}:{self.proxy_port}{self.base_url}/update_available_servers")
        proxy_res = requests.get(f"{EndpointsInterface.Localhost}:{self.proxy_port}{self.base_url}/update_available_servers",
                                 json={"action": "add", "server_url": res['host']})
        server_id = proxy_res.json()["server_id"]
        # Change the host's endpoint to use the proxy, check if the host is an ip or a domain to reply with the right host
        try:
            ipaddress.ip_address(self.proxy_host)
            res["host"] = f"http://{self.proxy_host}{self.base_url}/server/{server_id}"

        except ValueError:
            res["host"] = f"http://{self.proxy_host}{self.base_url}/server/{server_id}"
           
        print("Got the host", res["host"])
        # Since communication with the server runing is local, no need to use the url, localhost + port is always working
        self.servers_running.append(ServerItem(f"{EndpointsInterface.Localhost}:{self.proxy_port}{self.base_url}/server/{server_id}", checksum, file_path))
        return make_response(res, 200)

    @staticmethod
    def get_launch_path():
        return os.path.abspath(__file__)

    def _lifecycle_task_kill_server(self, servers_running):
        servers_killed = super()._lifecycle_task_kill_server(servers_running)
        # Complete the routine by notifying the proxy of all the server that needs to be unreferenced
        for server in servers_killed:
            payload = {"action": "remove", "server_url": server.host}
            requests.get(f"http://{self.proxy_host}:{self.proxy_port}/update_available_servers", json=payload)




if __name__ == "__main__":
    server_manager = ServerManagerProxyfied()
    try:
        server_manager.run_server()
    except KeyboardInterrupt:
        print("STOPPING")
