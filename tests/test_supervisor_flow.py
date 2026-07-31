from nodes.supervisor import supervisor


def test_supervisor_skips_web_when_search_results_empty():
    state = {
        "user_goal": "basic calculator",
        "active_agent": "supervisor",
        "retrieved_docs": [],
        "search_results": [],
        "app_plan": "",
        "generated_files": {},
        "is_complete": False,
        "plan_steps": ["build ui"],
        "review_feedback": "",
        "execution_result": "",
        "execution_error": "",
        "retry_count": 0,
        "memory": [],
    }

    result = supervisor(state)

    assert result["active_agent"] == "rag"
