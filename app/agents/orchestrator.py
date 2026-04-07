import os
import google.generativeai as genai
from app.mcp.tools import TOOL_REGISTRY

# Configure the Gemini client
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class OrchestratorAgent:
    def __init__(self):
        # We use Gemini 1.5 Flash because it is lightning fast and excellent at tool routing
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',            # 1. Define the tools for Gemini
            tools=[{
                "function_declarations": [
                    {
                        "name": "create_task",
                        "description": "Add a new task to the user's to-do list.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "title": {"type": "STRING", "description": "The title of the task"},
                                "deadline": {"type": "STRING", "description": "The deadline, e.g., 'Tomorrow 5pm'"}
                            },
                            "required": ["title"]
                        }
                    },
                    {
                        "name": "create_event",
                        "description": "Schedule a calendar event.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "title": {"type": "STRING", "description": "Title of the meeting/event"},
                                "time": {"type": "STRING", "description": "When it happens, e.g., 'Tomorrow 5pm'"}
                            },
                            "required": ["title", "time"]
                        }
                    },
                    {
                        "name": "get_current_time",
                        "description": "Call this tool FIRST if the user mentions relative time like 'tomorrow', 'next week', or 'today' so you know what the actual date is.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {} # No inputs needed!
                        }
                    },
                    {
                        "name": "web_search",
                        "description": "Use this tool to search the internet for current events, weather, news, or factual information you don't know.",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "search_query": {"type": "STRING", "description": "The exact query to type into the search engine"}
                            },
                            "required": ["search_query"]
                        }
                    }
                ]
            }]
        )

    async def process_query(self, query: str):
        # 2. Get Reasoning from Gemini
        response = self.model.generate_content(
            f"You are a helpful AI assistant. Use the provided tools to help the user. User query: {query}"
        )

        results = []
        tools_used = []
        final_text = "I have executed the requested actions."

        # 3. Handle Tool Calls
        # Check if Gemini decided to call any tools based on the prompt
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                
                # If Gemini returned a standard text response
                if part.text:
                    final_text = part.text

                # If Gemini requested to call a tool!
                if part.function_call:
                    func_name = part.function_call.name
                    # Extract arguments passed by Gemini
                    args = {key: val for key, val in part.function_call.args.items()}
                    
                    # Execute the actual Python code from our registry
                    if func_name in TOOL_REGISTRY:
                        result = await TOOL_REGISTRY[func_name](**args)
                        results.append({"tool": func_name, "status": "success", "data": result})
                        tools_used.append(func_name)

        # Fallback if no tools were used
        if not tools_used and final_text == "I have executed the requested actions.":
             final_text = "I couldn't determine the right tools to use for that request."

        return {
            "query": query,
            "plan": [f"Executed {t}" for t in tools_used] if tools_used else ["No actions required"],
            "agents_used": ["Orchestrator Agent (Gemini)"],
            "tools_used": tools_used,
            "final_response": final_text,
            "logs": results
        }