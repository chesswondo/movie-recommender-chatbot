from transformers import Agent

def base_agent_run(user_input: str,
                   agent: Agent) -> str:
    """
    Runs the agent on the user input string.

    : param user_input: (str) - given user input.
    : param agent: (Agent) - an agent with tools and llm.

    : return: (str) - agent's response.
    """
    return agent.run(user_input)