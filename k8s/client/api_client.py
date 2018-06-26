import requests
from k8s.config.configuration import load_config
import yaml


class ApiClient(object):

    def __init__(self):
        self.config = load_config()

    def api_call(self, method, url, **kwargs):

        headers = kwargs.get('headers')
        headers.update({
            'Authorization': self.config.token
        })

        if method == 'GET':
            url_api = '{}/{}'.format(self.config.host, url)
            response = requests.get(
                url_api,
                verify=self.config.ssl_ca_cert_path,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

        if method == 'POST':
            url_api = '{}/{}'.format(self.config.host, url)
            response = requests.post(
                url_api,
                data=kwargs.get('data'),
                verify=self.config.ssl_ca_cert_path,
                headers=headers
            )
            response.raise_for_status()
            return response.content
