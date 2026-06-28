from typing import TypedDict

class AgentState(TypedDict):
    user_goal:str
    active_agent:str
    retrieved_docs:list
    search_results:list
    app_plan:str
    generated_files:dict
    is_complete:bool

    #new fields to add
    plan_steps:list #writes detail steps
    review_feedback:str #write whats wrong
    execution_result:str
    execution_error:str
    retry_count:int
    memory:list