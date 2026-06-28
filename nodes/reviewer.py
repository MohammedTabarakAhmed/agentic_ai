from state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm=ChatGroq(model="llama-3.1-8b-instant")

def reviewer(state:AgentState):
    prompt = f"""
    You are a senior code reviewer with 30+ years experience.

    User wanted to build: {state['user_goal']}

    Plan that was followed: {state['plan_steps']}

    Generated files:
    {state['generated_files']}

    Review the code carefully for:
    - Missing files
    - Bugs or logic errors
    - Does it actually match what user wanted
    - Is the code complete or incomplete

    Reply with ONLY one of these two options:
    - "approved" if code is good
    - "rejected: <specific reason>" if code has issues

    No explanation. Just approved or rejected with reason.
    """
    response=llm.invoke([
        SystemMessage(content="You are a strict senior code reviewer who ensures code quality."),
        HumanMessage(content=prompt)
    ])

    content = response.content.strip()
    return {"review_feedback": content}