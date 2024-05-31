DEFAULT_THRESHOLD = 3000
from pyvista import DataSet


def is_localhost(url: str) -> bool:
    """
    Check if the url is localhost or is remote
    Args:
        url: the url to check

    Returns:
        True if the url is a localhost url, False otherwise
    """
    from urllib.parse import urlparse
    if not url.startswith("http"):
        url = "http://" + url
    parsed_url = urlparse(url)
    # Check if the hostname is localhost or 127.0.0.1
    return parsed_url.hostname in ('localhost', '127.0.0.1')

def replace_host(url, new_host):
    """
    Replace the host in a given URL with a new host.

    Parameters:
    url (str): The original URL.
    new_host (str): The new host to replace the old host.

    Returns:
    str: The URL with the host replaced.
    """
    from urllib.parse import urlparse, urlunparse
    parsed_url = urlparse(url)
    # Construct the new URL with the replaced host
    new_url = urlunparse((
        parsed_url.scheme,
        new_host,
        parsed_url.path,
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment
    ))
    return new_url

def is_web_link(string: str) -> bool:
    """
    Check if the input is a link
    Args:
        string: string to check

    Returns:
        True if the string is a url, False otherwise
    """
    import re
    # Regular expression pattern to match a typical web link
    web_link_pattern = r'^https?://.*$'

    return bool(re.match(web_link_pattern, string))


def get_decimated_content(
        pv_mesh_instance: DataSet,
        file_ext: str
) -> str:
    """
    This function extract the String that represent a mesh
    Args:
        pv_mesh_instance: The mesh from which you want to get the String representation
        file_ext: The file extension of the mesh

    Returns:
        A string representing the mesh.

        It could be then be written in a file and read by pv.read function.
        This function is mainly copied from pv.DataDet.save method.
    """
    if pv_mesh_instance._WRITERS is None:
        raise NotImplementedError(
            f'{pv_mesh_instance.__class__.__name__} writers are not specified,'
            ' this should be a dict of (file extension: vtkWriter type)'
        )

    if file_ext not in pv_mesh_instance._WRITERS:
        raise ValueError(
            'Invalid file extension for this data type.'
            f' Must be one of: {pv_mesh_instance._WRITERS.keys()}'
        )

    # store complex and bitarray types as field data
    pv_mesh_instance._store_metadata()

    writer = pv_mesh_instance._WRITERS[file_ext]()
    writer.SetInputData(pv_mesh_instance)
    writer.SetWriteToOutputString(1)
    writer.Write()
    return writer.GetOutputString()


def get_decimated_mesh_path(file_path: str, save_dir: str, decimation_factor: float = 0.5) -> str:
    """
    This function decimate a mesh and store it in a file
    Args:
        file_path: The path to the mesh to decimate
        save_dir: The file in which we should save the decimated mesh
        decimation_factor: The reduction factor to aim. e.g. decimation_factor = 0.25, initial mesh number of cells 1000
            -> resulting mesh will have 750 cells

    Returns:
        The path to the decimated_mesh

    For more information about decimation using pyvista you can have a look at the doc here:
    https://docs.pyvista.org/version/stable/examples/01-filter/decimate#decimate-example
    """
    import pyvista as pv
    import hashlib
    import os

    m = pv.read(file_path)
    pv_mesh = m.triangulate().decimate_boundary(decimation_factor).interpolate(m, n_points=2)
    content = get_decimated_content(pv_mesh, ".vtk")
    checksum = hashlib.sha256(content.encode('utf-8')).hexdigest()
    save_path = f"{save_dir}/{checksum}.vtk"
    if not os.path.exists(save_path):
        pv_mesh.save(save_path)
    return save_path


def compute_decimation_factor(current_nbr_points: float, target_nbr_points: float) -> float:
    """
    Compute the decimation reduction factor required to get to a target size number of points
    Args:
        current_nbr_points: The number of points of the initial mesh.
        target_nbr_points: The number of points aimed after decimation.

    Returns:
        The decimation_factor required to reach the target
    """
    return min(1 - target_nbr_points / current_nbr_points, 0.7)


def get_number_of_point(path: str) -> int:
    """
    Open the mesh to get its number of cells
    Args:
        path: Path to the mesh from which we want obtain get the number of cells

    Returns:
        The number of cell of the mesh at the specified location
    """
    import pyvista as pv
    m = pv.read(path)
    return m.GetNumberOfCells()


def save_mesh_content(file_content: str, save_dir: str, ttl_minutes: int =10, decimate: bool = None,
                      decimation_factor: float = None,
                      decimation_threshold: int = DEFAULT_THRESHOLD):
    """
    Take the content passed as argument and look if a file exists already with the same content by comparing sha256 hash. 
    More details below...
    Args:
        file_content: Content of the file you want to save in the cache
        save_dir: file path that will store the content if it does not already exist
        ttl_minutes: Time to live of the element in the cache. If the ttl is expired, the file will be removed
        from the cache
        decimate: Force to get return a version of the mesh with less vertices
        decimation_factor: How much the mesh should be decimated
        decimation_threshold: What is the maximum number of vertices allowed for mesh displayed in the plotter

    Returns:
        The path to the mesh. This path either:
            - Already exists, hence no new file generated, just return the path existing either for the mesh
            or its decimated version
            - Did not exist, therefore the checksum is saved and added to a json storing all cached files and generate a
            decimated version of this new mesh and return the path to it or the original one
    """
    import os
    import hashlib
    import json
    from datetime import datetime

    # Compute checksum and create the cache directory if it does not exist
    checksum = hashlib.sha256(file_content).hexdigest()
    os.makedirs(os.path.dirname(save_dir), exist_ok=True)

    # Get all relevant data of the filename and generate a new unique one
    directory, filename = os.path.split(save_dir)
    name, extension = os.path.splitext(filename)
    filename = f"{name}_{checksum}{extension}"

    # If the cache is not empty, load all the data we have from the json to a dict
    checksums = {}
    checksum_file = f"{directory}/checksums.json"
    if os.path.exists(checksum_file):
        with open(checksum_file, 'r') as f:
            checksums = json.load(f)

    # If the file we are looking for already exists
    if filename in checksums and checksums[filename]["checksum"] == checksum:
        checksums[filename]["last_used"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nbr_points = get_number_of_point(f"{directory}/{filename}")
    else:
        # If not, write the content to a new file 
        with open(f"{directory}/{filename}", 'wb') as f:
            f.write(file_content)

        nbr_points = get_number_of_point(f"{directory}/{filename}")

        if decimation_factor is None:
            decimation_factor = compute_decimation_factor(nbr_points, decimation_threshold)

        # Generate a decimated version of the mesh
        decimated_path = get_decimated_mesh_path(f"{directory}/{filename}", directory, decimation_factor)
        checksums[filename] = {
            "checksum": checksum,
            "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ttl_minutes": ttl_minutes,
            "decimated_path": decimated_path
        }

    # Open the file that store the cache state and update it
    with open(checksum_file, 'w') as f:
        json.dump(checksums, f, indent=4)

    # Return either the decimated version or the original version of the mesh depending on the mode
    if (nbr_points < decimation_threshold and decimate is None) or (decimate is not None and not decimate):
        return f"{directory}/{filename}"
    return checksums[filename]["decimated_path"]


def save_mesh_content_from_url(url, save_dir, ttl_minutes=10, decimate=None, decimation_factor=None,
                               decimation_threshold=DEFAULT_THRESHOLD):
    import requests

    response = requests.get(url)
    if response.status_code != 200:
        return None

    return save_mesh_content(response.content, save_dir.split("?")[0], ttl_minutes, decimate,
                             decimation_factor=decimation_factor, decimation_threshold=decimation_threshold)


def save_mesh_content_from_file(path, save_dir, ttl_minutes=10, decimate=None, decimation_factor=None,
                                decimation_threshold=DEFAULT_THRESHOLD):
    with open(path, "rb") as f:
        content = f.read()

    return save_mesh_content(content, save_dir, ttl_minutes, decimate, decimation_factor=decimation_factor,
                             decimation_threshold=decimation_threshold)


def update_cache(cache_directory):
    import os
    import json
    from datetime import datetime, timedelta
    checksum_file = os.path.join(cache_directory, "checksums.json")
    if not os.path.exists(checksum_file):
        return

    with open(checksum_file, 'r') as f:
        try:
            checksums = json.load(f)
        except json.JSONDecodeError:
            return

    current_time = datetime.now()
    keys_to_remove = []
    for filename, entry in checksums.items():
        last_used = datetime.strptime(entry["last_used"], "%Y-%m-%d %H:%M:%S")
        ttl_minutes = entry["ttl_minutes"]
        if current_time - last_used > timedelta(minutes=ttl_minutes):
            keys_to_remove.append((filename, entry.get("decimated_path", None)))

    # Remove the keys of old entries
    for key in keys_to_remove:
        os.remove(os.path.join(cache_directory, key[0]))
        if key[1] is not None:
            os.remove(key[1])
        del checksums[key[0]]

    # Rewrite the checksums.json file
    with open(checksum_file, 'w') as f:
        json.dump(checksums, f, indent=4)


class ServerItem:
    def __init__(self, host, type=None, path=None):
        self.host = host
        self.type = type
        self.path = path


def find_free_port():
    import socket
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def is_server_available(server):
    import requests
    try:
        res = requests.get(f"{server.host}/nbr_clients")
        return int(res.json()["nbr_clients"]) == 0
    except Exception:
        return True


def is_server_alive(server, timeout=0.5):
    import requests
    """ Try to make a request to the server and see if it responds to determine if he is alive """
    try:
        print(server)
        print(requests.get(server, timeout=timeout))
        print("C'es go")
        return True
    except Exception as e:
        print("ERROR")
        print(e)
        return False


def wait_for_server_alive(server, timeout=2):
    import time
    """ Try to ping the server to see if it is up  """
    init_time = time.time()
    while not is_server_alive(server):
        if time.time() - init_time >= timeout:
            return

