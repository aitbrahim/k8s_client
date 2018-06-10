import requests
from k8s.config.configuration import load_config


class ApiClient(object):

    def __init__(self):
        self.config = load_config()

    def api_call(self, method, url, **kwargs):
        import pdb;pdb.set_trace()
        if method == 'GET':
            url_api = '{}/{}'.format(self.config.host(self.config.current_context), url)
            requests.get(url_api, headers={
                'Accept': 'application/json',
                'Authorization': self.config.token(self.config.current_context)
            })

        if method == 'POST':
            pass
