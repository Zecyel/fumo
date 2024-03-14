from openai import OpenAI
from config import API_KEY

client = OpenAI(
    base_url="https://api.chatgptid.net/v1",
    api_key=API_KEY
)

def ask(msg: list) -> str:
    return client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=msg
    ).choices[0].message.content

def plain_msg(msg: str) -> list:
    return [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": msg }
    ]