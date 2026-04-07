import aiosqlite
import json
from datetime import datetime
from duckduckgo_search import DDGS
from app.db import db

async def create_task(title: str, deadline: str = None) -> dict:
    """MCP Tool: Creates a task in the database."""
    task = {"type": "task", "title": title, "deadline": deadline, "status": "pending"}
    await db.insert("tasks", task)
    return {"tool": "create_task", "result": f"Task '{title}' created with deadline: {deadline}"}

async def create_event(title: str, time: str) -> dict:
    """MCP Tool: Creates a calendar event."""
    event = {"type": "event", "title": title, "time": time}
    await db.insert("events", event)
    return {"tool": "create_event", "result": f"Event '{title}' scheduled for {time}."}

async def get_current_time() -> dict:
    """MCP Tool: Gets the real-world current date and time."""
    now = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
    return {"tool": "get_current_time", "result": f"Current system time is: {now}"}

async def web_search(search_query: str) -> dict:
    """MCP Tool: Searches the live internet for up-to-date information."""
    try:
        # Fetch the top results from the internet
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(search_query, max_results=2)]
        return {"tool": "web_search", "result": results}
    except Exception as e:
        return {"tool": "web_search", "result": f"Search failed: {str(e)}"}

# The Registry that the Orchestrator uses to find these functions
TOOL_REGISTRY = {
    "create_task": create_task,
    "create_event": create_event,
    "get_current_time": get_current_time,
    "web_search": web_search
}