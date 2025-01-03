import re
from enum import Enum

class SpecialCharacter(str, Enum):
    """
    Enumeration for some of telegram markdown special characters.

    Possible values:
    - SpecialCharacter.UNDERSCOPE: "UNDERSCOPE"
    - SpecialCharacter.ASTERISC: "ASTERISC"
    - SpecialCharacter.HYPHEN: "HYPHEN"
    - SpecialCharacter.LEFT_BRACKET: "LBRACKET"
    - SpecialCharacter.RIGHT_BRACKET: "RBRACKET"
    - SpecialCharacter.LEFT_SQUARE_BRACKET: "LSBRACKET"
    - SpecialCharacter.RIGHT_SQUARE_BRACKET: "RSBRACKET"
    """

    UNDERSCOPE = "UNDERSCOPE"
    ASTERISC = "ASTERISC"
    HYPHEN = "HYPHEN"
    LEFT_BRACKET = "LBRACKET"
    RIGHT_BRACKET = "RBRACKET"
    LEFT_SQUARE_BRACKET = "LSBRACKET"
    RIGHT_SQUARE_BRACKET = "RSBRACKET"

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)

def markdown_to_telegram_markdown(text: str) -> str:
    """
    Converts GitHub-flavored Markdown to Telegram-compatible MarkdownV2.

    : param text: (str) - input text in Markdown format.

    : return: (str) - output text in MarkDown2 format.
    """
    # Convert italic (*italic* -> _italic_), bold (**bold** -> *bold*)
    text = re.sub(r"(?<!\*)\*(.*?)\*(?!\*)", lambda m: f"{SpecialCharacter.UNDERSCOPE}{m.group(1)}{SpecialCharacter.UNDERSCOPE}", text)
    text = text.replace(f"{SpecialCharacter.UNDERSCOPE}{SpecialCharacter.UNDERSCOPE}", f"{SpecialCharacter.ASTERISC}")
    
    # Convert links ([text](url) -> Telegram-compatible Markdown)
    text = re.sub(r"\[(.*?)\]\((.*?)\)",
                  lambda m: f"{SpecialCharacter.LEFT_SQUARE_BRACKET}\
{m.group(1)}{SpecialCharacter.RIGHT_SQUARE_BRACKET}{SpecialCharacter.LEFT_BRACKET}{m.group(2)}{SpecialCharacter.RIGHT_BRACKET}", text)

    # Convert task lists (- [x] or - [ ] -> - item)
    text = re.sub(r"- \[(x| )\] (.*)", lambda m: f"{SpecialCharacter.HYPHEN} {m.group(2)}", text)

    # Convert headings (# Heading -> Bold text as Telegram does not support headings)
    text = re.sub(r"^(#+) (.*)", lambda match: f"{SpecialCharacter.ASTERISC}{match.group(2)}{SpecialCharacter.ASTERISC}", text, flags=re.MULTILINE)

    # Handle special symbols
    text = text.replace("~", "\\~").replace("<", "\\<").replace(">", "\\>").replace("#", "\\#").replace("+", "\\+").replace("-", "\\-").replace("`", "\\`")
    text = text.replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".", "\\.").replace("!", "\\!")
    text = text.replace("*", "\\*").replace("_", "\\_").replace("(", "\\(").replace(")", "\\)").replace("[", "\\[").replace("]", "\\]")

    # Handle formatting
    text = text.replace(SpecialCharacter.ASTERISC, "*").replace(SpecialCharacter.HYPHEN, "-").replace(SpecialCharacter.UNDERSCOPE, "_")
    text = text.replace(SpecialCharacter.LEFT_BRACKET, "(").replace(SpecialCharacter.RIGHT_BRACKET, ")")
    text = text.replace(SpecialCharacter.LEFT_SQUARE_BRACKET, "[").replace(SpecialCharacter.RIGHT_SQUARE_BRACKET, "]")

    return text