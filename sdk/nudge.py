import sdk.api as api

async def group_nudge(session: str, group_id: int, user_id: int):
    api.post('/sendNudge', {
        "sessionKey": session,
        "target": user_id,
        "subject": group_id,
        "kind": "Group"
    })
    pass