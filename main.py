from graph import app
import json, os

#get user goal
user_goal=input("What app do you want to build?")
#set initial state

initial_state = {
    "user_goal": user_goal,
    "active_agent": "supervisor", #start at supervisor
    "retrieved_docs": [],
    "search_results": [],
    "app_plan": "",
    "generated_files": {},
    "is_complete": False
}

#run the graph
result = app.invoke(initial_state)

#output folder
os.makedirs("output", exist_ok=True)

#lloop through each file and save it
for filename, code in result["generated_files"].items():
    filepath = f"output/{filename}"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # creates subfolders too
    with open(filepath, "w") as f:
        f.write(code) #write the code thinf into the file

print("Files saved to /output folder!")