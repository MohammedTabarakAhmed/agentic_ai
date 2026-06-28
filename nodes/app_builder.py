"""
state (notebook)
        ↓
app_builder picks up notebook
        ↓
reads → user_goal + search_results + retrieved_docs
        ↓
builds prompt with all 3
        ↓
sends to LLM (llama-3.3-70b via Groq)
    - SystemMessage → "you are a senior SWE"
    - HumanMessage  → prompt with all context
        ↓
LLM generates all app files as JSON
{
    "app.py":      "code...",
    "index.html":  "code...",
    "styles.css":  "code..."
}
        ↓
json.loads() converts string → python dict
        ↓
writes → generated_files back to state
        ↓
puts notebook down → returns to supervisor
        ↓
supervisor sees generated_files is filled → replies "done"
        ↓
END
"""

from state import AgentState
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import json
from dotenv import load_dotenv
load_dotenv()

llm=ChatGroq(model="llama-3.3-70b-versatile")

def app_builder(state: AgentState):
    #code
    prompt = f"""
        You are an expert app builder, FAANG senior developer.

        User wants: {state['user_goal']}

        Development plan to follow: {state['plan_steps']}

        Research from web: {state['search_results']}

        Relevant docs: {state['retrieved_docs']}

        Previous review feedback (if any): {state['review_feedback']}
        This is attempt number: {state['retry_count']}

        If review feedback exists, fix those specific issues.
        If this is a retry, improve on previous attempt.

        Generate all necessary files for this app.
        Reply ONLY with a JSON object like this:
        {{
        "filename.py": "code here",
        "index.html": "code here",
        "styles.css": "code here"
        }}
        No explanation. Just the JSON.
        """
    
    response=llm.invoke([
        SystemMessage(content='You are a senior SWE that can build web sites and application better than anyone.'),
        HumanMessage(content=prompt)
    ])

    content = response.content.strip()
    content = content.replace("```json", "").replace("```", "").strip() #json issue 
    generated_files = json.loads(content, strict=False)
    return {
    "generated_files": generated_files,
    "retry_count": state['retry_count'] + 1
}

