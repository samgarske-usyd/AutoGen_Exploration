import autogen

def main():
    # Load configuration file
    config = autogen.config_list_from_json(
        env_or_file="../config.json"
    )[0]

    # Create a single agent for providing assistance (not necessarily code specific)
    code_agent = autogen.AssistantAgent(
        name="Code Assistant",
        llm_config={
            "api_key": config["api_key"],
            "model": config["model"]  # Add your model name here
        }
    )

    # Create an agent that represents the user
    # In this case it's simply transferring the user message to the coding agent
    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="ALWAYS",
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False
        }
    )

    user_proxy.initiate_chat(code_agent, message="Plot a chart of META and TESLA stock price change.")


if __name__ == "__main__":
    main()