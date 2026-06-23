"""
1. Created the graph
told LangGraph "use AgentState as the notebook"

2. Added nodes
registered each worker with the graph
gave each worker a name and a function

3. Set entry point
told the graph "always start at supervisor"

4. Fixed edges
web → always goes back to supervisor
rag → always goes back to supervisor
app_builder → always goes back to supervisor

5. Conditional edge
supervisor → reads active_agent field
           → routes to whatever it says
           → if "done" → END

6. Compiled
locked everything in → made it runnable        
"""

from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.supervisor import supervisor
from nodes.web_search import web_search
from nodes.rag import rag_search
from nodes.app_builder import app_builder

def route(state:AgentState):
    return state['active_agent']

#graph create
graph=StateGraph(AgentState)

#add nodes
graph.add_node("supervisor", supervisor)
graph.add_node("web", web_search)
graph.add_node("rag", rag_search)
graph.add_node("app_builder", app_builder)

# set entry point
graph.set_entry_point("supervisor")

#fixed edge =where each agent(node) goes to supervisor
graph.add_edge("web","supervisor")
graph.add_edge("rag","supervisor")
graph.add_edge("app_builder","supervisor")

#conditional edge - were supervisor decides where to go
graph.add_conditional_edges(
    "supervisor",
    route,
    {
        "web":"web",
        "rag":"rag",
        "app_builder":"app_builder",
        "done":END #conditional edge see "done" and stops the graph
    }
)

#compile
app=graph.compile()