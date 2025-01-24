import os
import json
import autogen
from typing import Annotated

def get_student_details(SID: Annotated[str, "The student's ID number or SID"])  -> str:
    with open('dummy_data/student_data.json', 'r') as file:
        student_data = json.load(file)

    if SID in student_data:
        return json.dumps(student_data[SID], indent=4)
    else:
        return "No student data found."


def main():
    # Create working directory if it doesn't exist
    work_dir = "coding"
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    # Load configuration file
    config = autogen.config_list_from_json(
        env_or_file="../config.json"
    )[0]

    # Update Developer's system message to avoid bash commands
    chat_agent = autogen.AssistantAgent(
        name="ChatBot",
        llm_config={
            "api_key": config["api_key"],
            "model": config["model"]
        },
        system_message="""You are a helpful AI ChatBot for University Student Services.
        You design your own workflows to answer the student's question to the best of your ability.
        If it seems a task is too complex and outside of your abilities, then let the student know that 
        you are unable to complete the task. Do NOT answer any questions unrelated to the student or the University of Sydney.""",
    )
    chat_agent.register_for_llm(name="get_student_details", description="Get information about the using their ID.")(get_student_details)

    # Create an agent that represents the user
    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="ALWAYS",
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False
        }
    )
    user_proxy.register_for_execution(name="get_student_details")(get_student_details)

    user_proxy.initiate_chat(
        chat_agent,
        message="Student with SID has requested I look into their enrolments. Could you check which subjects they're taking?"
    )


if __name__ == "__main__":
    main()