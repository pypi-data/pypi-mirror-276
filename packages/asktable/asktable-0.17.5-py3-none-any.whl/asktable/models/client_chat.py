from atcommon.models import ChatCore
from atcommon.tools import format_time_ago
from asktable.models.client_base import convert_to_object, BaseResourceList
from asktable.models.client_run import RunList
from asktable.models.client_msg import MessageList, MessageClientModel
from asktable.api import APIRequest


class ChatClientModel(ChatCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    @property
    def runs(self):
        return RunList(self.api, endpoint=f"{self.endpoint}/{self.id}/runs")

    @property
    def messages(self):
        return MessageList(self.api, endpoint=f"{self.endpoint}/{self.id}/messages")

    @convert_to_object(cls=MessageClientModel)
    def ask(self, question) -> MessageClientModel:
        # 提问
        data = {"question": question}
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="POST", data=data)


class ChatList(BaseResourceList):
    __do_not_print_properties__ = ['tenant_id']


    @convert_to_object(cls=ChatClientModel)
    def _get_all_resources(self):
        return self._get_all_chats()

    def _get_all_chats(self):
        chats = self._get_all_resources_request()
        # 转换 created 字段
        for chat in chats:
            chat['created'] = format_time_ago(chat['created'])
            chat['latest_msg'] = format_time_ago(chat['latest_msg'])
        return chats

    @property
    @convert_to_object(cls=ChatClientModel)
    def latest(self):
        return self._get_latest_one_or_none()

    def page(self, page_number=1):
        return ChatList(self.api, self.endpoint, page_number=page_number)

    def all(self):
        return ChatList(self.api, self.endpoint, page_number=0, page_size=0)

    @convert_to_object(cls=ChatClientModel)
    def get(self, id):
        # 通过资源ID来获取
        return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")

    @convert_to_object(cls=ChatClientModel)
    def create(self, datasource_ids: list, **kwargs):

        # check datasource_ids
        if any(not isinstance(ds_id, str) for ds_id in datasource_ids):
            raise ValueError(f"datasource_ids must be a list of str: {datasource_ids}")
        #
        # if role_variables:
        #     if not isinstance(role_variables, dict):
        #         raise ValueError(f"role_variables must be a dict: {role_variables}")
        #     if not role_id and not role_name:
        #         raise ValueError("role_id or role_name must be provided if role_variables is provided")
        #
        data = {
            "datasource_ids": datasource_ids,
            **kwargs
        }
        return self.api.send(endpoint=self.endpoint, method="POST", data=data)
