from sdk.persisted_data import alloc, fetch

def _get_key(user_id: int) -> str:
    return f'user_coin_{user_id}'

def init_data():
    return {
        "coin": 100,
        "transection": []
    }

def init_user(user_id: int):
    alloc(_get_key(user_id), init_data())
    print("allocated")

def get_user(user_id: int):
    user = fetch(_get_key(user_id))
    if user != None:
        return user
    
    init_user(user_id)
    return fetch(_get_key(user_id))

def get_coin(user_id: int):
    return get_user(user_id).get("coin")

def add_coin(user_id: int, delta: int):
    user = get_user(user_id)
    user.set("coin", user.get("coin") + delta)
