from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Grandmaster OS")

# Shared Memory - One Source of Truth
class Task(BaseModel):
    id: str
    owner: str
    description: str
    status: str = "todo"
    file_scope: str = ""

TASKS = {}

@app.get("/")
def home():
    return {"status": "Grandmaster OS is running - BOSS is live!"}

@app.post("/tasks")
def create_task(task: Task):
    if task.id in TASKS:
        return {"error": "Duplicate task ID! Task already exists."}
    TASKS[task.id] = task
    return {"message": "Task created", "task": task}

@app.get("/tasks")
def list_tasks():
    return TASKS

@app.post("/ask-brain")
def ask_brain(question: str):
    # This is how BOSS uses the BRAIN - cleanapis.com
    client = OpenAI(
        base_url=os.getenv("CLEANAPIS_BASE_URL"),
        api_key=os.getenv("CLEANAPIS_API_KEY")
    )
    response = client.chat.completions.create(
        model="claude-opus-4.8",
        messages=[{"role": "user", "content": question}]
    )
    return {"answer": response.choices[0].message.content}