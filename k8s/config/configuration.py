import os
import google.auth
import oauthlib.oauth2
import urllib3
import datetime
import google.auth.transport.requests
from k8s.utils import parse_as_yaml_file
from .dateutil import UTC, format_rfc3339, parse_rfc3339

DEFUALT_FILE_CONFIG = "~/.kube/config"


# class NodeCofig(object):
#
#     def __init__(self, name, value):
#         self.name = name
#         self.value = value


class Configuration(object):

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.config_dict = None
        self.host = None
        self.current_context = None
        self.token = None
        self.token_expiry = None

    def init(self):
        config_file = self.config_file if self.config_file else os.path.expanduser(DEFUALT_FILE_CONFIG)
        self.config_dict = parse_as_yaml_file(config_file)
        self.current_context = self.config_dict['current-context']

        for item in self.config_dict['clusters']:
            if item['name'] == self.current_context:
                self.host = item['cluster']['server']

        for item in self.config_dict['users']:
            if item['name'] == self.current_context:
                self.token = item['user']['auth-provider']['config']['expiry']
                self.token_expiry = item['user']['auth-provider']['config']['access-token']

    def token_is_expired(self):
        now = datetime.datetime.now()
        if now > self.token_expiry:
            return True
        return False

    def load_token(self):
        if not self.token or self.token_is_expired():
            self.refresh_gcp_token()

        self.token = "Bearer %s" % self.token
        return self.token

    def refresh_gcp_token(self):
        credentials = self._refresh_credentials()
        self.token = credentials.token
        self.token_expiry = format_rfc3339(credentials.expiry)

    def _refresh_credentials(self):
        credentials, project_id = google.auth.default(
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        return credentials


def load_config(config_file=None):
    config = Configuration(config_file)
    config.init()
    return config
