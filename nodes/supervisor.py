"""
supervisor node receives state(notebook)
        ↓
builds a prompt → sends to LLM
        ↓
LLM replies with one word → "web" / "rag" / "app_builder" / "done"
        ↓
supervisor writes that to active_agent
        ↓
puts notebook down
"""
from state import AgentState
# from langchain_core.messages import SystemMessage, HumanMessage
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# load_dotenv()

# llm=ChatGroq(model="llama-3.3-70b-versatile")

# def supervisor(state: AgentState):
#     prompt = f"""
#         You are a supervisor managing these agents: planner, web, rag, app_builder, reviewer, executor.

#         User goal: {state['user_goal']}
#         Memory of past builds: {state['memory']}

#         Current state of work:
#         - plan_steps: {"done" if state['plan_steps'] else "empty"}
#         - search_results: {"done" if state['search_results'] else "empty"}
#         - retrieved_docs: {"done" if state['retrieved_docs'] else "empty"}
#         - generated_files: {"done" if state['generated_files'] else "empty"}
#         - review_feedback: {state['review_feedback']}
#         - execution_error: {state['execution_error']}
#         - retry_count: {state['retry_count']}

#         Rules — follow in STRICT order:
#         1. plan_steps is empty → reply: planner
#         2. search_results is empty → reply: web
#         3. retrieved_docs is empty → reply: rag
#         4. generated_files is empty → reply: app_builder
#         5. generated_files exists AND review_feedback is empty → reply: reviewer
#         6. review_feedback contains rejected → reply: app_builder
#         7. review_feedback contains approved AND execution_result is empty → reply: executor
#         8. execution_error exists → reply: app_builder
#         9. execution_result exists AND no error → reply: done

#         Reply with ONE word only. No explanation.
#         """

#     response=llm.invoke([
#         SystemMessage(content='You are a supervisor that routes tasks to agents.'),
#         HumanMessage(content=prompt)
#     ])
    
#     return {'active_agent': response.content.strip().lower()}
def supervisor(state: AgentState):
    print("DEBUG:", {
        "plan_steps": bool(state['plan_steps']),
        "search_results": bool(state['search_results']),
        "retrieved_docs": bool(state['retrieved_docs']),
        "generated_files": bool(state['generated_files']),
        "review_feedback": state['review_feedback'],
        "execution_result": state['execution_result'],
        "execution_error": state['execution_error'],
    })
    
    if not state['plan_steps']:
        return {"active_agent": "planner"}
    elif not state['retrieved_docs'] and not state['generated_files']:
        return {"active_agent": "rag"}
    elif state.get('retry_count', 0) >= 3 and state.get('generated_files'):
        return {"active_agent": "done"}
    elif not state['generated_files']:
        return {"active_agent": "app_builder"}
    elif not state['review_feedback']:
        return {"active_agent": "reviewer"}
    elif "rejected" in state['review_feedback'].lower():
        return {"active_agent": "app_builder"}
    elif not state['execution_result']:
        return {"active_agent": "executor"}
    elif state['execution_error']:
        return {"active_agent": "app_builder"}
    else:
        return {"active_agent": "done"}
"""
1. LLM is initialized with ChatGroq
2. supervisor() picks up the notebook (state)
3. converts state fields into a readable text prompt because llm can read tect not dict
4. sends it to LLM as:
   - SystemMessage → "you are a supervisor"
   - HumanMessage  → "here is the state, what's next?"
5. LLM replies "web" or "rag" or "app_builder" or "done"
6. supervisor writes that to active_agent in state
7. puts notebook down

Supervisor = LLM that reads the notebook 
             and writes one word back into it
"""