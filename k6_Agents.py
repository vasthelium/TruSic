from langchain.tools import tool
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver
import os
import pathlib
from k2_privacy_killswitch import privacy_switch
from langchain_openai import ChatOpenAI
import shutil

@tool
def delete_file(full_ab_path: str) -> str:
    """Delete a file from the filesystem."""
    if os.path.exists(full_ab_path):
        shutil.move(full_ab_path, "/Users/hussain/raw_soundfiles_trash")
        return f"Deleted {full_ab_path}"
    else:
        return f"File not found: {full_ab_path}"

checkpointer = MemorySaver()

agent = create_deep_agent(
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0),
    tools=[delete_file],
    interrupt_on={},
    checkpointer=checkpointer  # Required!
)

def agentic():
    _, speech_files = privacy_switch() #throwaway, dont care about first return
    audio_files = "/Users/hussain/raw_soundfiles"
    
    for files in speech_files:
        file_name = files["file_name"]
        full_ab_path = os.path.join(audio_files, file_name)
        response = agent.invoke(
        {
        "messages": [
            {"role": "user", "content": f"Delete this file: {full_ab_path}"}
            ]
        },
        config={"configurable": {"thread_id": "trusic_session_1"}}
        )
        print(response)

if __name__ == "__main__":
    agentic()










