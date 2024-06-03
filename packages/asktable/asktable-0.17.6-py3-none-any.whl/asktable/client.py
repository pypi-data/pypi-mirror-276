from asktable import models
from asktable.api import APIRequest
from atcommon.version import VERSION
from asktable import exceptions as errors


class AskTable:
    __version__ = VERSION
    version = VERSION

    DataSource = models.DataSourceClientModel
    Policy = models.AuthPolicyClient
    Role = models.AuthRoleClient
    SecureTunnel = models.SecureTunnel

    errors = errors

    def __init__(self, api_url='https://api.asktable.com',
                 token='token1', debug=False, user_id=None):
        self.api_url = api_url
        self.token = token
        self.debug = debug
        self.user_id = user_id

    @property
    def api(self):
        return APIRequest(api_url=self.api_url, token=self.token, debug=self.debug, user_id=self.user_id)

    @property
    def datasources(self):
        return models.DataSourceList(api=self.api, endpoint="/datasources")

    @property
    def chats(self):
        return models.ChatList(api=self.api, endpoint="/chats")

    @property
    def securetunnels(self):
        return models.SecureTunnelList(api=self.api, endpoint="/securetunnels")

    @property
    def roles(self):
        return models.AuthRoleList(self.api, endpoint="/auth/roles")

    @property
    def policies(self):
        return models.AuthPolicyList(self.api, endpoint="/auth/policies")


    @property
    def token_id(self):
        return self.api.send(endpoint="/account/token", method="GET")

