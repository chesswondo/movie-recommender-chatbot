from telegram import Update
from telegram.ext import ContextTypes
from typing import Callable

class Telegram:
    """Class for telegram bot behavior."""

    def __init__(self, generate_answer: Callable[[str], str]) -> None:
        """
        Initializes an instance of Telegram.

        :param generate_answer: (Callable[[str], str]) - answer generation function which takes string input and returns another string.

        :return: (None) - this function does not return any value.
        """
        self._generate_answer = generate_answer

    # Start command (/start)
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Welcome to the Movie Recommender Bot! I can help you find a movie to watch based on your request.\n"
            "Just send me a description of what you want to watch."
        )

    # Help command (/help)
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "I can respond to the following commands:\n/start - Start the bot\n/help - Get help information"
        )

    # Handle text messages
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        user_input = update.message.text

        # Ignore other inputs from the same user during processing
        if user_id in context.user_data.get("processing", set()):
            await update.message.reply_text("I am still processing your previous request. Please wait.")
            return

        # Mark the user as being processed
        if "processing" not in context.user_data:
            context.user_data["processing"] = set()
        context.user_data["processing"].add(user_id)

        # Send the temporary message and store its ID
        thinking_message = await update.message.reply_text("Let me think about it...")

        # Processing
        answer = self._generate_answer(user_input).strip()

        # Format the response (convert **text** to *text* for MarkdownV2)
        formatted_answer = answer.replace("**", "*")
        
        # Escape other special characters in MarkdownV2
        formatted_answer = formatted_answer.replace("_", "\\_").replace("[", "\\[").replace("]", "\\]").replace("(", "\\(").replace(")", "\\)").replace("~", "\\~").replace("`", "\\`").replace(">", "\\>").replace("#", "\\#").replace("+", "\\+").replace("-", "\\-").replace("=", "\\=").replace("|", "\\|").replace("{", "\\{").replace("}", "\\}").replace(".", "\\.").replace("!", "\\!")

        # Delete the temporary message
        await thinking_message.delete()

        # Send the final response as MarkdownV2
        await update.message.reply_text(formatted_answer, parse_mode="MarkdownV2")

        # Remove the user from processing
        context.user_data["processing"].remove(user_id)

