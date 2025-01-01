from language_models.text_generation_llm import CustomLLM
from language_models.sentence_similarity_model import EmbeddingModel
from interface.telegram_bot import Telegram
from utils.tools import MovieRetrieverTool, PostprocessingTool
from utils.common_utils import load_config, set_device
from utils.llm_utils import base_agent_run
from interface.window import ChatWindow
from transformers import ReactCodeAgent
from telegram.ext import CommandHandler, MessageHandler, filters, Application
import pandas as pd
import tkinter as tk
from functools import partial
from dotenv import load_dotenv
import os

def main():
    # Load configuration files
    main_config = load_config("../configs/main.json")
    chat_model_config = load_config("../configs/models/chat_model.json")
    embedding_model_config = load_config("../configs/models/embedding_model.json")

    # Initialize text generation model
    chat_model = CustomLLM(model_name=chat_model_config["model_name"])
    
    print("Chat model initialized!")
    
    # Initialize sentence similarity model
    embedding_model = EmbeddingModel(model_name=embedding_model_config["model_name"],
                                     cache_dir=embedding_model_config["model_path"],
                                     device=set_device(embedding_model_config["device"]),
                                     allow_download=embedding_model_config["allow_download"])
    
    print("Sentence similarity model initialized!")

    # Read precalculated embeddings
    movie_embeddings_df = pd.read_pickle(main_config["dataset_path"])
    
    # Initialize tool for movie retrieving
    movie_retriever_tool = MovieRetrieverTool(movie_db=movie_embeddings_df,
                                              embedding_model=embedding_model,
                                              top_n=main_config["n_movies_to_select"])
    
    # Initialize a prompt for movie postprocessing and the corresponding tool
    prompt = "User query: {user_query}\n\nFirst, analyze this query. \
Then, based on it, suggest the most appropriate movie from the following list and very briefly describe your choice for the user:\n\n{retrieved_movies}. \
\n\nDon't dublicate the user's query, respond in a polite tone, keeping the conversation going, and in the end ask if there is anything else needed.\n\nResponse:"
    movie_postprocessing_tool = PostprocessingTool(prompt_template=prompt, llm_engine=chat_model)

    # Initialize the main agent and a corresponding running function
    agent = ReactCodeAgent(tools=[movie_retriever_tool, movie_postprocessing_tool], llm_engine=chat_model, verbose=2)
    agent_run = partial(base_agent_run,
                        agent=agent)
    
    # Run telegram bot or local window UI
    if main_config["run_as_telegram_bot"]:
        
        # Specify the path to the .env file and extract its content
        load_dotenv(dotenv_path="../configs/.env")
        API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
        WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")

        # Build the telegram bot
        telegram_bot = Telegram(generate_answer=agent_run)
        application = Application.builder().token(API_TOKEN).build()
        application.add_handler(CommandHandler('start', telegram_bot.start))
        application.add_handler(CommandHandler('help', telegram_bot.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_bot.handle_text))

        # Configure webhook
        application.run_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path=f"{API_TOKEN}",
            webhook_url=f"{WEBHOOK_URL}/{API_TOKEN}"
        )

    else:
        root = tk.Tk()
        chat_window = ChatWindow(root=root, generate_answer=agent_run)
        root.mainloop()


if __name__ == "__main__":
    main()