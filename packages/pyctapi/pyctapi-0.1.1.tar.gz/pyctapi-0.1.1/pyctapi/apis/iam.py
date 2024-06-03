from dataclasses import dataclass
from typing import Optional

from .base import CtapiBaseClient


@dataclass
class CheckUserPermissionParam:
    
    action: str
    user_id: str
    account_id: str
    region_id: Optional[str] = None
    project_id: Optional[str] = None


class IamApi(CtapiBaseClient):

    def check_user_permission(self, param: CheckUserPermissionParam, timeout=1):
        params = {
            "action": param.action,
            "assumeUserId": param.user_id,
            "accountId": param.account_id,
            "regionId": param.region_id,
            "epId": param.project_id,
        }
        return self.perform_request('/v1/perm/validate', params, 'POST', timeout=timeout)
