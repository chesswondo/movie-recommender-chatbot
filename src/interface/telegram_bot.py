from telegram import Update
from telegram.ext import ContextTypes
from typing import Callable
from collections import deque

from utils.telegram_utils import SpecialSymbol, markdown_to_telegram_markdown 

class Telegram:
    """Class for telegram bot behavior."""

    def __init__(self, config: dict, generate_answer: Callable[[str], str]) -> None:
        """
        Initializes an instance of Telegram.

        : param config; (dict) - a telegram configuration file.
        : param generate_answer: (Callable[[str], str]) - answer generation function which takes string input and returns another string.

        : return: (None) - this function does not return any value.
        """
        self._config = config
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

        # Initialize user message history if it doesn't exist
        if "message_history" not in context.user_data:
            context.user_data["message_history"] = deque(maxlen=self._config["n_context_messages"])

        # Add the current user message to history
        context.user_data["message_history"].append((SpecialSymbol.USER.value, user_input))

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

        # Retrieve last 5 exchanges (user and bot)
        memory = list(context.user_data["message_history"])
        last_messages = ""
        for msg in memory[:-1]:
            last_messages += msg[0] + ": " + msg[1] + "\n"
        user_input = SpecialSymbol.START_CONTEXT.value + last_messages + SpecialSymbol.END_CONTEXT.value + user_input

        # Processing
        answer = self._generate_answer(user_input).strip()

        # Add bot's response to message history
        context.user_data["message_history"].append((SpecialSymbol.BOT.value, answer))

        # Format the response
        formatted_answer = markdown_to_telegram_markdown(answer)

        # Delete the temporary message
        await thinking_message.delete()

        # Send the final response as MarkdownV2
        try:
            await update.message.reply_text(formatted_answer, parse_mode="MarkdownV2")
        except Exception:
            await update.message.reply_text("An error occurred while sending the message. Please repeat your request.")

        # Remove the user from processing
        context.user_data["processing"].remove(user_id)

