import sdk.api as api

def user_group_nickname(session: str, group_id: int, member_id: int) -> str:
    profile = api.get(f"/memberProfile?sessionKey={session}&target={group_id}&memberId={member_id}")
    return profile["nickname"]
