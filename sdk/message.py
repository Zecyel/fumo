from typing import Dict, List, Union
from config import QQ
from sdk.history import message_from_id

mapper = {
    "Source": "DUMMY",
    "Quote": "Q",
    "At": "@",
    "AtAll": "@A",
    "Face": "F",
    "Plain": "P",
    "Image": "I",
    "MarketFace": "M"
}

def parse_message_chain(msg_chain: List[Dict[str, any]]) -> Union[str, List[any]]:
    msg = msg_chain[1:] # remove the first element 'Source' 
    format = ""
    data = []
    for msg_segment in msg:
        if msg_segment["type"] == "Plain" and msg_segment["text"].strip() == "":
            continue
        if msg_segment["type"] not in mapper:
            print("Method Not Implemented")
            continue
        
        format += mapper[msg_segment["type"]]

        if msg_segment["type"] == "Plain":
            data.append(msg_segment["text"].strip())
        elif msg_segment["type"] == "Quote":
            data.append({
                "message_id": msg_segment["id"],
                "from": {
                    "group_id": msg_segment["groupId"],
                    "sender_id": msg_segment["senderId"]
                },
                "to": {
                    "group_id": msg_segment["targetId"]
                }
            })
        elif msg_segment["type"] == "At":
            data.append(msg_segment["target"])
            if msg_segment["target"] == QQ:
                format += "fumo" # @fumo
        elif msg_segment["type"] == "AtAll":
            data.append(None)
        elif msg_segment["type"] == "Image":
            data.append({
                "image_id": msg_segment["imageId"],
                "url": msg_segment["url"]
            })
        else:
            print("Method Not Implemented")
            
    return format, data

def convert_message(msg) -> Union[str, dict]:
    if not "messageChain" in msg:
        return "", {}
    
    message_chain = msg["messageChain"]
    format, data = parse_message_chain(message_chain)

    if msg["type"] == "GroupMessage":
        return f"group.{format}", {
            "group_id": msg["sender"]["group"]["id"],
            "sender_id": msg["sender"]["id"],
            "message": data
            # "message_id": msg["messageChain"][0]["id"]
        }
    elif msg["type"] == "FriendMessage":
        return f"friend.{format}", {
            "sender_id": msg["sender"]["id"],
            "message": data
            # "message_id": msg["messageChain"][0]["id"]
        }
    else:
        return "", {}

def text_message(msg: str) -> Dict[str, str]:
    return {
        "type": "Plain",
        "text": msg
    }

def img_message(msg: str) -> Dict[str, str]:
    return {
        "type": "Image",
        "url": msg
    }

def quote_message(session: str, message_id: str, group_id: str, user_id: str) -> Dict[str, str]:
    return {
        "type": "Quote",
        "id": message_id,
        "groupId": group_id,
        "senderId": user_id,
        "targetId": group_id,
        "origin": message_from_id(session, message_id, group_id)["messageChain"]
    }