"""reads generated_files
        ↓
saves files to disk temporarily
        ↓
tries to run the main file
        ↓
if works → writes execution_result
if fails → writes execution_error"""

import subprocess
import os
import tempfile
from state import AgentState

def executor(state:AgentState):
    try:
        files=state['generated_files']

        #save files to o/p folder
        os.makedirs("output",exist_ok=True)
        for filename, code in files.items():
            filepath=f"output/{filename}"
            os.makedirs(os.path.dirname(filepath),exist_ok=True)#create a c\subfolder too
            with open(filepath,"w") as f:
                f.write(code)

        #find th emainpython file to run
        
        py_files=[f for f in files.keys() if f.endswith(".py")]

        if not py_files:
            return{
                "execution_result":"success",
                "execution_error":""
            }
        
        #run the py file first
        result=subprocess.run(
            ["python",f"output/{py_files[0]}"], #grab the forst .py because it would be app.py as we llm we assign like that
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode==0: #0 means everythong worked and executed and 1+ means soemthong failed
            return {"execution_result": result.stdout,"execution_error":""}
        else:
            return {"execution_resul": "failed","execution_error":result.stderr}
        """result.stdout  # what the program printed normally
        result.stderr  # what error it threw if it crashed"""

    except Exception as e:
        return{
            "execution_result":"failed",
            "execution_error":str(e)
        }