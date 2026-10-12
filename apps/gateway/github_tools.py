import os
import requests
from dotenv import load_dotenv
load_dotenv()

def check_github():
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}
    r = requests.get("https://api.github.com/user", headers=headers)
    if r.status_code == 200:
        return True, r.json()["login"]
    else:
        return False, r.text