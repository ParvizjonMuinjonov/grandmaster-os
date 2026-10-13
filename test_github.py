import os, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
print("Checking GitHub token...")
if token:
    print("Token found:", token[:10] + "...")
else:
    print("Token NOT found in .env")
    exit()

print("Trying to connect to GitHub...")
headers = {"Authorization": f"token {token}"}
r = requests.get("https://api.github.com/user", headers=headers)

if r.status_code == 200:
    print("SUCCESS! GitHub connected")
    print("Your GitHub user:", r.json()["login"])
else:
    print("FAILED:")
    print(r.status_code, r.text)