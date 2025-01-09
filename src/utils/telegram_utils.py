import re
from enum import Enum

class SpecialSymbol(str, Enum):
    """
    Enumeration for some special symbols in telegram messages.

    Possible values:
    1. For telegram markdown characters:
        - SpecialSymbol.UNDERSCOPE: "UNDERSCOPE"
        - SpecialSymbol.ASTERISC: "ASTERISC"
        - SpecialSymbol.HYPHEN: "HYPHEN"
        - SpecialSymbol.LEFT_BRACKET: "LBRACKET"
        - SpecialSymbol.RIGHT_BRACKET: "RBRACKET"
        - SpecialSymbol.LEFT_SQUARE_BRACKET: "LSBRACKET"
        - SpecialSymbol.RIGHT_SQUARE_BRACKET: "RSBRACKET"
    2. Other symbols:
        - SpecialSymbol.START_CONTEXT: "--START--"
        - SpecialSymbol.END_CONTEXT: "--END--"
        - SpecialSymbol.USER: "USER"
        - SpecialSymbol.BOT: "BOT"
    """

    UNDERSCOPE = "UNDERSCOPE"
    ASTERISC = "ASTERISC"
    HYPHEN = "HYPHEN"
    LEFT_BRACKET = "LBRACKET"
    RIGHT_BRACKET = "RBRACKET"
    LEFT_SQUARE_BRACKET = "LSBRACKET"
    RIGHT_SQUARE_BRACKET = "RSBRACKET"

    START_CONTEXT = "--START--"
    END_CONTEXT = "--END--"
    USER = "USER"
    BOT = "BOT"

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
    text = re.sub(r"(?<!\*)\*(.*?)\*(?!\*)", lambda m: f"{SpecialSymbol.UNDERSCOPE.value}{m.group(1)}{SpecialSymbol.UNDERSCOPE.value}", text)
    text = text.replace(f"{SpecialSymbol.UNDERSCOPE.value}{SpecialSymbol.UNDERSCOPE.value}", f"{SpecialSymbol.ASTERISC.value}")
    
    # Convert links ([text](url) -> Telegram-compatible Markdown)
    text = re.sub(r"\[(.*?)\]\((.*?)\)",
                  lambda m: f"{SpecialSymbol.LEFT_SQUARE_BRACKET.value}{m.group(1)}{SpecialSymbol.RIGHT_SQUARE_BRACKET.value}"
                            f"{SpecialSymbol.LEFT_BRACKET.value}{m.group(2)}{SpecialSymbol.RIGHT_BRACKET.value}", text)

    # Convert task lists (- [x] or - [ ] -> - item)
    text = re.sub(r"- \[(x| )\] (.*)", lambda m: f"{SpecialSymbol.HYPHEN.value} {m.group(2)}", text)

    # Convert headings (# Heading -> Bold text as Telegram does not support headings)
    text = re.sub(r"^(#+) (.*)", lambda match: f"{SpecialSymbol.ASTERISC.value}{match.group(2)}{SpecialSymbol.ASTERISC.value}", text, flags=re.MULTILINE)

    # Handle special symbols
    text = text.replace("~", "\\~").replace("<", "\\<").replace(">", "\\>").replace("#", "\\#").replace("+", "\\+").replace("-", "\\-").replace("`", "\\`")
    text = text.replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".", "\\.").replace("!", "\\!")
    text = text.replace("*", "\\*").replace("_", "\\_").replace("(", "\\(").replace(")", "\\)").replace("[", "\\[").replace("]", "\\]")

    # Handle formatting
    text = text.replace(SpecialSymbol.ASTERISC.value, "*").replace(SpecialSymbol.HYPHEN.value, "-").replace(SpecialSymbol.UNDERSCOPE.value, "_")
    text = text.replace(SpecialSymbol.LEFT_BRACKET.value, "(").replace(SpecialSymbol.RIGHT_BRACKET.value, ")")
    text = text.replace(SpecialSymbol.LEFT_SQUARE_BRACKET.value, "[").replace(SpecialSymbol.RIGHT_SQUARE_BRACKET.value, "]")

    return text