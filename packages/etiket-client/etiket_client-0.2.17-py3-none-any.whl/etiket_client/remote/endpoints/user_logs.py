from typing import Optional, List

from etiket_client.remote.client import client
from etiket_client.remote.endpoints.models.user_logs import UserLogRead, UserLogUploadInfo

def create_user_log(file_name : str, reason : Optional[str]= None) -> UserLogUploadInfo:
    params = {"file_name": file_name, "reason": reason}
    response = client.post("/logs/deposit/create/", params=params)
    return UserLogUploadInfo.model_validate(response[0])

def confirm_user_log(key : str) -> None:
    params = {"key": key}
    client.post("/logs/deposit/confirm/", params=params)

def get_user_logs(username : str, offset : int = 0, limit : int = 10) -> List[UserLogRead]:
    params = {"username": username, "offset": offset, "limit": limit}
    response = client.get("/logs/", params=params)
    return [UserLogRead.model_validate(log) for log in response]