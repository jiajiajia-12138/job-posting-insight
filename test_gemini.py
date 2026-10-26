import os

# 这行必须在 import genai 之前设置，才能让 SDK 走代理
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",  # 免费层可用的模型
    contents="用一句话解释什么是 SQL"
)
print(response.text)