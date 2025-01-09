from transformers import ManagedAgent
import re

def base_agent_run(user_input: str,
                   agent: ManagedAgent) -> str:
    """
    Runs the agent on the user input string.

    : param user_input: (str) - given user input.
    : param agent: (ManagedAgent) - an agent with tools and llm.

    : return: (str) - agent's response.
    """
    return agent(user_input)

def extract_text(input_string: str, substring1: str, substring2: str) -> tuple:
    """
    Extracts text between two substrings and the combined text from before the first
    substring and after the second substring.

    Args:
        input_string (str): The input string to search within.
        substring1 (str): The first substring.
        substring2 (str): The second substring.

    Returns:
        tuple: A tuple containing:
            - The text between the two substrings.
            - The combined text of everything before the first substring and after the second substring.
    """
    try:
        # Find the start and end indices of the substrings
        start_index = input_string.index(substring1) + len(substring1)
        end_index = input_string.index(substring2, start_index)

        # Extract the text between the substrings
        between_text = input_string[start_index:end_index]

        # Extract the combined text of everything before and after
        before_text = input_string[:input_string.index(substring1)]
        after_text = input_string[end_index + len(substring2):]
        combined_text = before_text + after_text

        return between_text, combined_text

    except ValueError as e:
        # Handle cases where the substrings are not found
        return f"Error: {str(e)}", None


def extract_user_bot_pairs(input_string: str) -> list:
    """
    Extracts all "user: " and "bot: " substrings along with their respective texts
    and returns them as a list of tuples.

    Args:
        input_string (str): The input string containing "user: " and "bot: ".

    Returns:
        list: A list of tuples, each containing:
            - "user" or "bot" (str)
            - The associated text (str)
    """
    # Define a regular expression to match "user: " or "bot: " and their associated text
    pattern = r'(user|bot): (.*?)((?=user: )|(?=bot: )|$)'
    matches = re.findall(pattern, input_string, re.DOTALL)

    # Convert matches into a list of tuples with desired format
    result = [(match[0], match[1].strip()) for match in matches]
    return result