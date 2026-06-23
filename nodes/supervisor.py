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
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm=ChatGroq(model="llama-3.3-70b-versatile")

def supervisor(state: AgentState):
    prompt = f"""
You are a supervisor managing these agents: web, rag, app_builder.

User goal: {state['user_goal']}

Current state of work:
- search_results: {"done" if state['search_results'] else "empty"}
- retrieved_docs: {"done" if state['retrieved_docs'] else "empty"}
- generated_files: {"done" if state['generated_files'] else "empty"}

Rules:
- If search_results is empty → reply: web
- If retrieved_docs is empty → reply: rag
- If both done but no generated_files → reply: app_builder
- If generated_files exists → reply: done

Reply with ONE word only: web, rag, app_builder, or done
"""

    response=llm.invoke([
        SystemMessage(content='You are a supervisor that routes tasks to agents.'),
        HumanMessage(content=prompt)
    ])
    
    return {'active_agent': response.content.strip()}
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