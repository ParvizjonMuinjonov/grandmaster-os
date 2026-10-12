from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from typing import List
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Grandmaster OS")

# Allow Telegram to load the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Mini App
import os
if os.path.exists("apps/miniapp"):
    app.mount("/miniapp", StaticFiles(directory="apps/miniapp"), name="miniapp")

@app.get("/app")
def serve_app():
    return FileResponse("apps/miniapp/index.html")

TASKS_FILE = "tasks.json"
CONTRACTS_FILE = "contracts.json"
MESSAGES_FILE = "messages.json"

class Task(BaseModel):
    id: str
    owner: str
    description: str
    status: str = "todo"
    file_scope: str = ""
    dependencies: List[str] = []

class Contract(BaseModel):
    id: str
    version: str
    schema: dict

class Message(BaseModel):
    message_id: str
    run_id: str = "run-1"
    task_id: str
    sender: str
    recipient: str
    type: str
    plan_version: str = "v1"
    content: str
    requested_action: str = ""

def load_json_file(path, model):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
                return {k: model(**v) for k, v in data.items()}
            except:
                return {}
    return {}

def save_json_file(path, data):
    with open(path, "w") as f:
        json.dump({k: v.model_dump() for k, v in data.items()}, f, indent=2)

TASKS = load_json_file(TASKS_FILE, Task)
CONTRACTS = load_json_file(CONTRACTS_FILE, Contract)
MESSAGES = load_json_file(MESSAGES_FILE, Message)

@app.get("/")
def home():
    return {"status": "Grandmaster OS is running - BOSS is live!"}

@app.post("/tasks")
def create_task(task: Task):
    if task.id in TASKS:
        return {"error": "Duplicate task ID! Task already exists."}
    for t in TASKS.values():
        if t.file_scope == task.file_scope and t.status != "done" and task.file_scope != "":
            return {"error": f"File locked! File {task.file_scope} is already owned by {t.id}"}
    for dep in task.dependencies:
        if dep not in TASKS:
            return {"error": f"Dependency {dep} does not exist"}
        if TASKS[dep].status != "done":
            return {"error": f"Dependency {dep} is not done yet. Status is {TASKS[dep].status}"}
    TASKS[task.id] = task
    save_json_file(TASKS_FILE, TASKS)
    return {"message": "Task created", "task": task}

@app.get("/tasks")
def list_tasks():
    return TASKS

@app.put("/tasks/{task_id}")
def update_task(task_id: str, status: str):
    if task_id not in TASKS:
        return {"error": "Task not found"}
    TASKS[task_id].status = status
    save_json_file(TASKS_FILE, TASKS)
    return {"message": f"Task {task_id} updated to {status}", "task": TASKS[task_id]}

@app.post("/contracts")
def create_contract(contract: Contract):
    CONTRACTS[contract.id] = contract
    save_json_file(CONTRACTS_FILE, CONTRACTS)
    return {"message": "Contract locked", "contract": contract}

@app.get("/contracts")
def list_contracts():
    return CONTRACTS

@app.post("/messages")
def create_message(msg: Message):
    if msg.message_id in MESSAGES:
        return {"error": "Duplicate message_id! Already exists"}
    MESSAGES[msg.message_id] = msg
    save_json_file(MESSAGES_FILE, MESSAGES)
    return {"message": "Message recorded", "data": msg}

@app.get("/messages")
def list_messages():
    return MESSAGES

@app.get("/messages/{task_id}")
def messages_for_task(task_id: str):
    result = {k: v for k, v in MESSAGES.items() if v.task_id == task_id}
    return result

@app.post("/ask-brain")
def ask_brain(question: str):
    client = OpenAI(
        base_url=os.getenv("CLEANAPIS_BASE_URL"),
        api_key=os.getenv("CLEANAPIS_API_KEY")
    )
    response = client.chat.completions.create(
        model="claude-opus-4.8",
        messages=[{"role": "user", "content": question}]
    )
    return {"answer": response.choices[0].message.content}