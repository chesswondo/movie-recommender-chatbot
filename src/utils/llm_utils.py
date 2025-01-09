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

def extract_text(input_string: str,
                 substring1: str,
                 substring2: str) -> tuple[str, str]:
    """
    Extracts text between two substrings and the combined text from before the first
    substring and after the second substring.

    : param input_string: (str) - the input string to search within.
    : param substring1: (str) - the first substring.
    : param substring2: (str) - the second substring.

    : return: (tuple) - a tuple containing:
        - the text between the two substrings
        - the combined text of everything before the first substring and after the second substring
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


def extract_role_pairs(input_string: str,
                       role1: str,
                       role2: str) -> list[tuple]:
    """
    Extracts all substrings with the specified roles and their associated texts
    and returns them as a list of tuples.

    : param input_string: (str) - the input string containing the role identifiers and associated texts.
    : param role1: (str) - the first role identifier (e.g., "user").
    : param role2: (str) - the second role identifier (e.g., "bot").

    : return: (list) - a list of tuples, each containing:
        - role1 or role2 (str)
        - the associated text (str)
    """
    # Define a regular expression to match the roles and their associated text
    pattern = rf'({re.escape(role1)}|{re.escape(role2)}): (.*?)((?={re.escape(role1)}: )|(?={re.escape(role2)}: )|$)'
    matches = re.findall(pattern, input_string, re.DOTALL)

    # Convert matches into a list of tuples with desired format
    result = [(match[0], match[1].strip()) for match in matches]
    return result