import autogen
import os  # Add this import


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
    developer_agent = autogen.AssistantAgent(
        name="Developer",
        llm_config={
            "api_key": config["api_key"],
            "model": config["model"]
        },
        system_message="""You are a Python Developer. You create Python solutions to the given problem.
            You make amendments to the code based on the advice of the code reviewers.
            DO NOT include bash commands or pip install commands in your responses.
            Instead, mention required packages in comments.
            When the reviewer is satisfied with the code and has signalled that it is completed and ready for production,
            save the python code to the working directory.
            """
    )

    # Create a second agent for QAing and assessing the code
    review_agent = autogen.AssistantAgent(
        name="Reviewer",
        llm_config={
            "api_key": config["api_key"],
            "model": config["model"]
        },
        system_message="""You are a Senior Python Developer, who reviews the developers code to industry standards and best practice.
                          You review Python scripts given to you by the developer, and assess if they fit the required task.
                          If the code meets your standards, signal to the developer that the code is complete and ready for production. 
                          If there are any issues or potential improvements, provide feedback to the developer. """,
        # code_execution_config={  # Add execution config for reviewer
        #     "work_dir": "coding",
        #     "use_docker": False,
        # }
    )


    # Create an agent that represents the user
    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False
        }
    )

    group_chat = autogen.GroupChat(
        agents=[user_proxy, developer_agent, review_agent],
        messages=[],
        max_round=30
    )

    manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config={
            "api_key": config["api_key"],
            "model": config["model"]
        }
    )

    user_proxy.initiate_chat(
        manager,
        message="Create a chart of META and TESLA stock price over time. Save the code and the chart."
    )


if __name__ == "__main__":
    main()