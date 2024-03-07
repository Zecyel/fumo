import sdk.api as api

async def set_essence(session: str, message_id: int, group_id: int):
    api.post('/setEssence', {
        "sessionKey": session,
        "messageId": message_id,
        "target": group_id
    })
