from api_client import ApiClient


class CoreV1Api(object):
    def __init__(self):
        self.api_client = ApiClient()

    def list_pods(self, **kwargs):

        namespace = kwargs.get('namespace')
        url = 'api/v1/pods'
        if namespace:
            url = 'api/v1/namespaces/{}/pods'.format(namespace)

        return self.api_client.api_call('GET', url)
