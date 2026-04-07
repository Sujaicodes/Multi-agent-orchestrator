from app.mcp.tools import TOOL_REGISTRY

class BaseAgent:
    def __init__(self, name: str, allowed_tools: list):
        self.name = name
        self.allowed_tools = allowed_tools

    async def execute(self, instruction: str) -> dict:
        # IN PRODUCTION: Pass instruction + allowed_tools schema to an LLM here.
        # The LLM returns a structured JSON requesting a tool call.
        
        # MOCK LLM REASONING BASED ON INSTRUCTION KEYWORDS
        log = {"agent": self.name, "instruction": instruction, "tool_used": None}
        
        if self.name == "Task Agent" and "task" in instruction.lower():
            result = await TOOL_REGISTRY["create_task"]("Finish assignment", "Friday")
            log["tool_used"] = "create_task"
            log["result"] = result
            
        elif self.name == "Scheduler Agent" and "schedule" in instruction.lower():
            result = await TOOL_REGISTRY["create_event"]("Meeting", "Tomorrow 5pm")
            log["tool_used"] = "create_event"
            log["result"] = result
            
        elif self.name == "Notes Agent" and "note" in instruction.lower():
            result = await TOOL_REGISTRY["save_note"]("User prefers meetings at 5pm", ["preference"])
            log["tool_used"] = "save_note"
            log["result"] = result
            
        return log

# Instantiate Agents
task_agent = BaseAgent("Task Agent", ["create_task", "update_task"])
scheduler_agent = BaseAgent("Scheduler Agent", ["create_event", "check_calendar"])
notes_agent = BaseAgent("Notes Agent", ["save_note", "search_notes"])