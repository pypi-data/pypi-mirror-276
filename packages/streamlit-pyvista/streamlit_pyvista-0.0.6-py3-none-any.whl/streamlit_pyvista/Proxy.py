from flask import Flask, request
from flask_sock import Sock
import requests
from websocket import create_connection
import threading
import simple_websocket
from flask_cors import CORS
import os

from streamlit_pyvista import ROOT_URL

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
sock = Sock(app)

available_servers = {}
base_url = ROOT_URL
print("ROOT URL", base_url)

# API endpoint top specify server available
# Default route have url args to specify which server to connect, a list of id for example

# @app.route('/', defaults={'path': ''})
@app.route(f'{base_url}/server/<server_id>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(server_id, path):
    """
    Main route of the proxy. This route simply forward the request to and return the result
    Args:
        server_id: id of the server, it will be looked in the available_servers map
        path: Path of the request to make to the server

    Returns: Response of the target server to the request
    """
    if path == "ws":
        # In case websocket are requested pm classical http just return 200
        return 200

    # This route is for HTTP requests
    method = request.method
    # Save headers
    headers = {key: value for key, value in request.headers}
    # Save request data
    data = request.get_data()

    # Make request to the target server
    url = f"{available_servers[server_id]}/{path}"
    response = requests.request(method, url, headers=headers, data=data)
    # return the response of the server
    return response.content, response.status_code, {'Content-Type': response.headers.get('Content-Type')}


@app.route(f'{base_url}/update_available_servers', methods=['GET', 'POST', 'PUT', 'DELETE'])
def update_available_servers():
    """
    This route is used by a server manager to update the available_servers map by adding or removing servers
    Returns:
        A response containing information about the action taken. If a server was added,
        add to the response the associated id of the server
    """
    re = request.json
    resp = {}
    if re["action"] == "add":
        # Check that the server is not already in the map to avoid having multiple times the same server
        if re["server_url"] not in available_servers.values():
            # Set the server id
            resp["server_id"] = str(len(available_servers))
            # Populate the available_servers map with the new key value pair
            available_servers[resp["server_id"]] = re["server_url"]
        else:
            return {"message": f"Server {re['server_id']} already exists"}, 400
    elif re["action"] == "remove":
        # Loop in the map and remove the entry if it's the server we need to delete
        for key in list(available_servers.keys()):
            if available_servers[key] == re["server_url"]:
                del available_servers[key]
    return {"message": f"Server {re['server_url']} updated succesfully with action {re['action']}"} | resp, 200


def forward_client_to_target(ws, target_ws):
    """
    This function forward the websocket of the client to the server
    Args:
        ws: client's websocket
        target_ws: server's websocket
    """
    while ws.connected and target_ws.connected:
        try:
            client_data = ws.receive()
            target_ws.send(client_data)
        except simple_websocket.errors.ConnectionClosed:
            break


def forward_target_to_client(ws, target_ws):
    """
    This function forward the websocket of the server to the client
    Args:
        ws: server's websocket
        target_ws: client's websocket
    """
    while target_ws.connected and ws.connected:
        try:
            target_data = target_ws.recv()
            ws.send(target_data)
        except simple_websocket.errors.ConnectionClosed:
            break


@sock.route(f'{base_url}/server/<server_id>/ws')
def echo(ws: simple_websocket.ws.Server, server_id):
    """
    This route connect the websocket from the client and the server together and launch forwarding function
    in both direction
    Args:
        ws: the websocket of the client
        server_id: the id of the server it tries to communicate with

    """
    # If the server_id does not exist return
    if server_id not in available_servers:
        return

    # Create the websocket with the target server
    target_ws = create_connection(f"ws://{available_servers[server_id].split('//')[1]}/ws")

    # Create separate threads for forwarding messages
    client_to_target_thread = threading.Thread(target=forward_client_to_target, args=(ws, target_ws))
    target_to_client_thread = threading.Thread(target=forward_target_to_client, args=(ws, target_ws))

    # Start the threads
    client_to_target_thread.start()
    target_to_client_thread.start()

    # Wait for threads to finish
    client_to_target_thread.join()
    target_to_client_thread.join()

    # Close the websockets
    ws.close()
    target_ws.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
