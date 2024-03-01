from typing import Tuple, Dict

def convert_message(msg) -> Tuple[str, Dict[str, any]]:
    if msg["type"] == "GroupMessage":
        msg_chain = msg["messageChain"]
        # because the first element of msg_chain must be 'Source'
        if len(msg_chain) == 2 and msg_chain[1]["type"] == "Plain":
            return "group.text_message", {
                "group_id": msg["sender"]["group"]["id"],
                "sender_user_id": msg["sender"]["id"],
                "message": msg_chain[1]["text"]
            }
        else:
            return "group.message", {
                "group_id": msg["sender"]["group"]["id"],
                "sender_user_id": msg["sender"]["id"],
                "message": msg_chain[1:]
            }
    print("Method Not Implmented")
    return "", {}

def text_message(msg: str) -> Dict[str, str]:
    return [{
        "type": "Plain",
        "text": msg
    }]

def img_message(url: str) -> Dict[str, str]:
    return [{
        "type": "Image",
        "url": url
    }]