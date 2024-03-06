from typing import Dict, List, Union

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
                "msg_id": msg_segment["id"],
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

def convert_message(msg) -> Dict[str, Dict[str, any]]:
    message_chain = msg["messageChain"]
    format, data = parse_message_chain(message_chain)

    if msg["type"] == "GroupMessage":
        return {
            f"group.{format}": {
                "group_id": msg["sender"]["group"]["id"],
                "sender_id": msg["sender"]["id"],
                "message": data
            }
        }
    elif msg["type"] == "FriendMessage":
        return {
            f"friend.{format}": {
                "sender_id": msg["sender"]["id"],
                "message": data
            }
        }
    else:
        return {}

def text_message(msg: str) -> Dict[str, str]:
    return {
        "type": "Plain",
        "text": msg
    }