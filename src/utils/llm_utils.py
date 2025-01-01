from transformers import ManagedAgent

def base_agent_run(user_input: str,
                   agent: ManagedAgent) -> str:
    """
    Runs the agent on the user input string.

    : param user_input: (str) - given user input.
    : param agent: (ManagedAgent) - an agent with tools and llm.

    : return: (str) - agent's response.
    """
    return agent(user_input)