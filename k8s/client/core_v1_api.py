from api_client import ApiClient


class CoreV1Api(object):
    def __init__(self):
        self.api_client = ApiClient()

    def list_pods(self, **kwargs):

        namespace = kwargs.get('namespace')
        url = 'api/v1/pods'
        if namespace:
            url = 'api/v1/namespaces/{}/pods'.format(namespace)

        headers = {
            'Content-type': 'application/json'
        }

        return self.api_client.api_call('GET', url, headers=headers)

    def list_services(self, **kwargs):

        namespace = kwargs.get('namespace')
        url = 'api/v1/services'
        if namespace:
            url = 'api/v1/namespaces/{}/services'.format(namespace)
        headers = {
            'Content-type': 'application/json'
        }

        return self.api_client.api_call('GET', url, headers=headers)

    def submit_deployment(self, **kwargs):
        if ('data' not in kwargs) or (kwargs['data'] is None):
            raise ValueError("Missing the required parameter `data` when calling `submit_deployment`")

        data = kwargs.get('data')
        namespace = kwargs.get('namespace', 'default')
        url = 'apis/extensions/v1beta1/namespaces/{}/deployments'.format(namespace)
        headers = {
            'Content-type': 'application/yaml'
        }
        return self.api_client.api_call('POST', url, data=data, headers=headers)

