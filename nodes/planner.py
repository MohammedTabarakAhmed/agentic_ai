from state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
import json
from dotenv import load_dotenv
load_dotenv()

llm=ChatGroq(model="llama-3.3-70b-versatile")


def planner(state:AgentState):
    prompt = f"""
    You are an expert planner with 30+ years experience.

    User wants to build: {state['user_goal']}

    Memory of past builds: {state['memory']}

    Break this goal into clear development steps.
    Reply ONLY with a JSON list like this:
    ["step 1", "step 2", "step 3"]
    No explanation. Just the JSON list.
    """

    try:
        response = llm.invoke([
            SystemMessage(content='You are an expert software project planner that breaks goals into clear development steps.'),
            HumanMessage(content=prompt)
        ])
        content = response.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()  # json issue
        plan_steps = json.loads(content, strict=False)
        return {"plan_steps": plan_steps}
    except Exception:
        goal = (state['user_goal'] or 'app').strip().lower()
        if 'calculator' in goal:
            fallback_steps = [
                'Define calculator operations',
                'Create a simple calculator UI',
                'Implement basic arithmetic logic',
                'Test the calculator interactions'
            ]
        else:
            fallback_steps = [
                'Define core requirements',
                'Create a simple interface',
                'Implement the main functionality',
                'Test the result'
            ]
        return {"plan_steps": fallback_steps}