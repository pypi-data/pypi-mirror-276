
from asktable.models.client_base import convert_to_object, BaseResourceList
from atcommon.models.securetunnel import SecureTunnelCore, SecureTunnelLinkCore
from asktable.api import APIRequest


class SecureTunnelLinkList(BaseResourceList):
    __do_not_print_properties__ = ['created_at']

    @convert_to_object(cls=SecureTunnelLinkCore)
    def _get_all_resources(self):
        return self._get_all_resources_request()


class SecureTunnel(SecureTunnelCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    def update(self, name, client_info):
        return self.api.send(
            endpoint=f"/securetunnels/{self.id}",
            method="POST",
            data={"atst_name": name, "client_info": client_info}
        )

    @property
    def links(self):
        return SecureTunnelLinkList(self.api, endpoint=f"{self.endpoint}/{self.id}/links")


class SecureTunnelList(BaseResourceList):
    __do_not_print_properties__ = ['tenant_id', 'created_at', 'info']

    @convert_to_object(cls=SecureTunnel)
    def create(self):
        return self.api.send(endpoint=self.endpoint, method="POST")

    @convert_to_object(cls=SecureTunnel)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @property
    @convert_to_object(cls=SecureTunnel)
    def latest(self):
        return self._get_latest_one_or_none()

    @convert_to_object(cls=SecureTunnel)
    def get(self, id):
        return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")
