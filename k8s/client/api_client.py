import requests
from k8s.config.configuration import load_config


class ApiClient(object):

    def __init__(self):
        self.config = load_config()

    def api_call(self, method, url, **kwargs):

        if method == 'GET':
            url_api = '{}/{}'.format(self.config.host, url)
            r = requests.get(url_api, verify=self.config.ssl_ca_cert_path, headers={
                'Accept': 'application/json',
                'Authorization': self.config.token
            })
            r.raise_for_status()
            return r.json()

        if method == 'POST':
            pass
