import sdk.api as api
from typing import List

def user_group_nickname(session: str, group_id: int, member_id: int) -> str:
    profile = api.get(f"/memberProfile?sessionKey={session}&target={group_id}&memberId={member_id}")
    return profile["nickname"]

def group_user_list(session: str, group_id: int) -> List[int]:
    members = api.get(f"/memberList?sessionKey={session}&target={group_id}")
    return [user["id"] for user in members["data"]]