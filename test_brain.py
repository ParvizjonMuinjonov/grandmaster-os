from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("CLEANAPIS_API_KEY")
url = os.getenv("CLEANAPIS_BASE_URL")

print("Checking .env...")
if key:
    print("Key found:", key[:10] + "...")
else:
    print("Key found: NOTHING")
print("URL found:", url)
print("")

print("Trying to connect to cleanapis.com...")
try:
    client = OpenAI(base_url=url, api_key=key)
    response = client.chat.completions.create(
        model="claude-opus-4.8",
        messages=[{"role": "user", "content": "Say hello, I am working!"}]
    )
    print("SUCCESS!")
    print(response.choices[0].message.content)
except Exception as e:
    print("FAILED:")
    print(e)