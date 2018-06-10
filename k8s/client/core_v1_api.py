from api_client import ApiClient


class CoreV1Api(object):
    def __init__(self):
        self.api_client = ApiClient()

    def list_pod_for_all_namespaces(self):
        self.api_client.api_call('GET', 'api/v1/pods')
