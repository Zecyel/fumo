from openai import OpenAI
from config import API_KEY, PROXY_URL

client = OpenAI(
    base_url=PROXY_URL,
    api_key=API_KEY
)

def draw(prompt: list) -> str:
    ret = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return ret.data[0].url
