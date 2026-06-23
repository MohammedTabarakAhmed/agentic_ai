from typing import TypedDict

class AgentState(TypedDict):
    user_goal:str
    active_agent:str
    retrieved_docs:list
    search_results:list
    app_plan:str
    generated_files:dict
    is_complete:bool