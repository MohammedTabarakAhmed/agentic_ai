from state import AgentState

def memory(state: AgentState):
    # build one memory entry from this build
    entry = {
        "goal": state['user_goal'], #input
        "files": list(state['generated_files'].keys()), #just generated file name
        "result": state['execution_result'] #success or failed
    }

    # add it to existing memory list
    updated_memory = state['memory'] + [entry]

    # write back to state
    return {"memory": updated_memory}