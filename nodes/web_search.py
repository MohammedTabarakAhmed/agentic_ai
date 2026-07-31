from tavily import TavilyClient
from state import AgentState

from dotenv import load_dotenv
load_dotenv()

try:
    tav_client = TavilyClient()
except Exception:
    tav_client = None


def web_search(state: AgentState):
    if tav_client is None:
        return {"search_results": []}

    try:
        results = tav_client.search(query=state["user_goal"])
        return {"search_results": results.get("results", [])}
    except Exception:
        return {"search_results": []}