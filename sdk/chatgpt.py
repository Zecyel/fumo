from openai import OpenAI
from config import API_KEY, PROXY_URL

client = OpenAI(
    base_url=PROXY_URL,
    api_key=API_KEY
)

def ask(msg: list) -> str:
    ret = client.chat.completions.create(
      model="gpt-4",
      messages=msg
    )
    # print(ret)
    return ret.choices[0].message.content

def plain_msg(msg: str) -> list:
    return [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": msg }
    ]