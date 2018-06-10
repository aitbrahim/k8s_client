import os
import datetime
import google.auth
import google.auth.transport.requests
from k8s.utils import parse_as_yaml_file

DEFUALT_FILE_CONFIG = "~/.kube/config"


class NodeCofig(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __getitem__(self, item):
        result = self.value.get(item)
        if result is None:
            raise Exception('Item {} Not Found in {}'.format(item, self.value))
        elif isinstance(result, list) or isinstance(result, dict):
            return NodeCofig(item, result)
        else:
            return result

    def get_item_with_context_name(self, context_name):
        for item in self.value:
            if item['name'] == context_name:
                return NodeCofig(context_name, item)


class Configuration(object):

    def __init__(self, config_dict):
        self.config_dict = config_dict
        self.node = NodeCofig('kube-config', config_dict)
        self.current_context = config_dict['current-context']
        self.context = None
        self.cluster = None
        self.user = None

    def token_is_expired(self, provider):
        now = datetime.datetime.now()
        if now > provider.value['expiry']:
            return True
        return False

    def load_token(self, context_name):
        provider = self.node['users'].get_item_with_context_name(context_name)['user']
        if 'access-token' not in provider.value or self.token_is_expired(provider):
            self.refresh_gcp_token(provider)

        token = "Bearer %s" % provider.value.get('access-token')
        return token

    def refresh_gcp_token(self, provider):
        credentials = self._refresh_credentials()
        provider.value['access-token'] = credentials.token
        provider.value['expiry'] = credentials.expiry

    def _refresh_credentials(self):
        credentials, project_id = google.auth.default(
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        return credentials


def load_config(config_file=None):

    config_file = config_file if config_file else os.path.expanduser(DEFUALT_FILE_CONFIG)
    config_dict = parse_as_yaml_file(config_file)
    return Configuration(config_dict)
