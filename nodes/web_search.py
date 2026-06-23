from tavily import TavilyClient
from state import AgentState

from dotenv import load_dotenv
load_dotenv()

tav_client=TavilyClient()

def web_search(state: AgentState):
    results = tav_client.search(query=state["user_goal"])
    return {"search_results": results["results"]}