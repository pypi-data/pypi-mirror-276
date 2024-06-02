from atcommon.models.base import BaseCoreModel
from atcommon.tools import format_time_ago
from atcommon.models.qa import BIAnswer


class ChatCore(BaseCoreModel):
    id: str
    tenant_id: str
    datasource_ids: list[str]
    role_id: str
    role_variables: dict
    created: int

    __properties_init__ = ['tenant_id', 'id', 'datasource_ids', 'human_msgs', 'ai_msgs',
                           'created', 'latest_msg', 'role_id', 'role_variables']

    def __repr__(self):
        return f"<Chat[{self.role_id}] {self.id} [{format_time_ago(self.created)}]>"


class MessageCore(BaseCoreModel):
    id: str
    chat_id: str
    role: str
    content: dict
    reply_to_msg_id: str
    created: int

    # role: human | ai
    __properties_init__ = ['id', 'chat_id', 'created', 'role', 'content', 'reply_to_msg_id']

    def __repr__(self):
        if self.role == 'ai':
            return f"[{self.id}] [{self.role}] {BIAnswer.load_from_dict(self.content)}"
        else:
            return f"[{self.id}] [{self.role}] {self.content}"


class RunCore(BaseCoreModel):
    id: str
    chat_id: str

    # status: running | finished | failed | canceled
    __properties_init__ = ['id', 'chat_id', 'created', 'status', 'steps']

    def __repr__(self):
        return f"<ChatRun {self.id} [{format_time_ago(self.created)}]>"
