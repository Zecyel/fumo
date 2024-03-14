import sdk.api as api
from typing import Union

def message_from_id(session: str, message_id: int, target: int) -> Union[str, dict]:
    # target may be group_id or friend_id
    ret = api.get(f"/messageFromId?sessionKey={session}&messageId={message_id}&target={target}")
    return ret["data"]
