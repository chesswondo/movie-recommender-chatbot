from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from transformers.agents import ReactJsonAgent
import re
from typing import Any

def create_input_message(user_input: str) -> dict:

    # Define ResponseSchemas
    year_schema = ResponseSchema(
        name="year",
        description="Extract all the years that are mentioned in the text if they relate to the \
                    description of the film. Output them comma-separated with spaces between. \
                        If no years are mentioned in the text, just return -1, don't make them up."
    )
    genre_schema = ResponseSchema(
        name="genre",
        description="Extract all the movie genres that are mentioned in the text if they relate to the \
                    description of the film. Output them comma-separated with spaces between. \
                        If no genres are mentioned in the text, just return -1, don't make them up."
    )

    description_schema = ResponseSchema(
        name="description",
        description="Extract the description of the film that the author of the text wants to watch. \
            Don't mention any years. If there is no description besides years, just output -1, don't make it up."
    )

    # Create StructuredOutputParser
    response_schemas = [year_schema, genre_schema, description_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    # Simplified prompt template
    review_template_2 = """\
    For the following text, extract the requested information.

    Text: {text}

    {format_instructions}

    Respond with only the single JSON object. Don't add any additional text. Stop after providing the answer. End of response. Response:
    """

    # Generate the prompt
    prompt = PromptTemplate.from_template(template=review_template_2)
    messages = prompt.format(text=user_input, format_instructions=format_instructions)

    return {'messages': messages,
            'parser': output_parser}


def retrieve_json(model_response: str,
                  parser: Any) -> Any:
    
    # Find all JSON-like objects (non-recursive, but it should work in this controlled case)
    json_matches = re.findall(r'\{(?:[^{}]*|\{[^{}]*\})*\}', model_response)

    # Check if we have any JSON matches and select the last one
    if json_matches:
        last_json = json_matches[-1]
    else:
        raise ValueError("No JSON object found in the response")

    response = ""

    # Parse the JSON
    try:
        response = parser.parse(last_json)
    except Exception as e:
        print(f"Parsing error: {e}")
        print(f"Raw response received: {model_response}")

    return response


def base_agent_run(user_input: str,
                   agent: ReactJsonAgent) -> str:
    """
    Runs the agent on the user input string.

    : param user_input: (str) - given user input.
    : param agent: (ReactJsonAgent) - an agent with tools and llm.

    : return: (str) - agent's response.
    """
    return agent.run(user_input)