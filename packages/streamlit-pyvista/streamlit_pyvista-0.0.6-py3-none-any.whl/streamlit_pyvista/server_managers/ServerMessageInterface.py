

class ServerMessageInterface:

    @classmethod
    @property
    def Host(self):
        return "host"

    @classmethod
    @property
    def SelectMesh(self):
        return "select_mesh"

    @classmethod
    @property
    def UploadMesh(self):
        return "upload_mesh"

    @classmethod
    @property
    def InitConnection(self):
        return "init_connection"

    @classmethod
    @property
    def NumberClientsField(self):
        return "nbr_clients"

    @classmethod
    @property
    def ViewerField(self):
        return "Viewer"

    @classmethod
    @property
    def GetViewerPath(self):
        return "GetViewerPath"

    @classmethod
    @property
    def GetViewerFile(self):
        return "GetViewerFile"


class EndpointsInterface:

    @classmethod
    @property
    def Protocol(self):
        return "http"

    @classmethod
    @property
    def Localhost(self):
        return f"{self.Protocol}://127.0.0.1"

    @classmethod
    @property
    def InitConnection(self):
        return "/init_connection"

    @classmethod
    @property
    def SelectMesh(self):
        return "/select_mesh"

    @classmethod
    @property
    def UploadMesh(self):
        return "/upload_mesh"

    @classmethod
    @property
    def ClientsNumber(self):
        return "/nbr_clients"

    @classmethod
    @property
    def KillServer(self):
        return "/kill_server"

    @classmethod
    @property
    def SetViewer(self):
        return "/set_viewer"
