from atcommon.models.base import BaseCoreModel
from datetime import datetime


class AuthPolicyCore(BaseCoreModel):
    tenant_id: str
    id: str
    permission: str
    name: str
    description: str
    dataset_config: dict

    __properties_init__ = [
        'tenant_id', 'id', 'permission', 'name', 'description',
        'dataset_config', 'created_at', 'modified_at',
    ]

    def __repr__(self):
        return f"[{self.name}]<{self.id}>"


class AuthRoleCore(BaseCoreModel):
    tenant_id: str
    id: str
    name: str
    description: str
    created_at: str | datetime
    modified_at: str | datetime

    __properties_init__ = [
        'tenant_id', 'id', 'name', 'description', 'created_at',
        'modified_at',
    ]

    def __repr__(self):
        return f"[{self.name}]<{self.id}>"



class AuthRoleVariableCore(BaseCoreModel):
    role_id: str
    datasource_id: str
    variables: list

    __properties_init__ = [
        'role_id', 'datasource_id', 'variables',
    ]

    def __repr__(self):
        return f"[{self.role_id}]<{self.datasource_id}>[{self.variables}]"
