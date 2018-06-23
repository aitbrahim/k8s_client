import os
import datetime
import tempfile
import base64
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

    @property
    def token(self, context_name=None):
        context_name = context_name if context_name else self.config_dict['current-context']
        provider = self.node['users'].get_item_with_context_name(context_name)['user']
        if 'access-token' not in provider.value or self.token_is_expired(provider):
            self._refresh_gcp_token(provider)

        token = "Bearer %s" % provider.value.get('access-token')
        return token

    @property
    def host(self, context_name=None):
        context_name = context_name if context_name else self.config_dict['current-context']
        host = self.node['clusters'].get_item_with_context_name(context_name)['cluster']['server']
        return host

    @property
    def ssl_ca_cert_path(self, context_name=None):
        context_name = context_name if context_name else self.config_dict['current-context']
        ca_cert = self.node['clusters'].get_item_with_context_name(context_name)['cluster']['certificate-authority-data']

        ca_cert_base64 = base64.b64decode(
            ca_cert
        )

        cert = tempfile.NamedTemporaryFile(delete=False)

        with open(cert.name, 'w') as fh:
            fh.write(ca_cert_base64)

        return cert.name

    def _refresh_gcp_token(self, provider):
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
