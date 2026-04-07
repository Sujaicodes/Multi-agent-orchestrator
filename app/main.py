from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.schemas import QueryRequest, OrchestratorResponse
from app.agents import OrchestratorAgent
from app.db import db

# This runs once when the server boots up
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    yield

app = FastAPI(title="Multi-Agent AI Orchestrator API", version="1.0.0", lifespan=lifespan)
orchestrator = OrchestratorAgent()

@app.post("/query", response_model=OrchestratorResponse)
async def process_user_query(request: QueryRequest):
    """Main entry point for natural language requests."""
    result = await orchestrator.process_query(request.query)
    
    # Save the AI's execution trace to the SQL logs table
    await db.insert("logs", result)
    return result

@app.get("/tasks")
async def get_tasks():
    """Fetch all tasks from the real database."""
    tasks = await db.fetch_all("tasks")
    return {"tasks": tasks}

@app.get("/events")
async def get_events():
    """Fetch all events from the real database."""
    events = await db.fetch_all("events")
    return {"events": events}