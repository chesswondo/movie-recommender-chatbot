from language_models.text_generation_llm import CustomLLM
from language_models.sentence_similarity_model import EmbeddingModel
from utils.dataset_utils import filter_dataframe
from utils.llm_utils import create_input_message, retrieve_json
from utils.embedding_utils import select_movies
from utils.common_utils import extract_between, load_config, set_device
from interface.window import ChatWindow
import pandas as pd
import tkinter as tk
from functools import partial

def generate_base_response(user_input: str,
                           main_config: dict,
                           chat_model: CustomLLM,
                           embedding_model: EmbeddingModel) -> str:

    input_message = create_input_message(user_input=user_input)
    messages = input_message['messages']
    parser = input_message['parser']

    print("Messages is", messages)
    model_response = chat_model(messages)
    final_response = retrieve_json(model_response=model_response,
                                   parser=parser)
    
    print("Final json response received!")
    print("Final response:", final_response)
    print(f"Filters:\nYear: {final_response['year']},\nGenre: {final_response['genre']}\n")

    movie_embeddings_df = pd.read_pickle(main_config["dataset_path"])
    filtered_embeddings = filter_dataframe(movie_embeddings_df,
                                    year=final_response['year'],
                                    genre=final_response['genre'])
    
    print("Filtered movie embeddings received!")
    
    selected_movies = select_movies(movie_df=filtered_embeddings,
                                    embedding_model=embedding_model,
                                    user_input=final_response['description'],
                                    top_n=main_config["n_movies_to_select"])
    
    print("Top movies selected successfully!")

    # Generate final response to user
    # Construct the prompt with retrieved movies
    movie_summaries = "\n\n".join([f"{row['title']}: {row['overview']}" for _, row in selected_movies.iterrows()])
    prompt = f"User query: {final_response['description']}\n\nIn this query, ignore all mentioned years and genres. \
Then, based on it, suggest only the best movie from the following list and very briefly describe your choice:\n\n{movie_summaries}. \
\n\nDon't make up queries. Do not add any additional information beyond the short main answer. Write 'End of response' after it. \n\nResponse:"

    print("Final prompt generated!")

    # Generate the recommendation
    response = chat_model(prompt)
    return extract_between(response, "Response:", "End of response")


def main():
    # Load configuration files
    main_config = load_config("../configs/main.json")
    chat_model_config = load_config("../configs/models/chat_model.json")
    embedding_model_config = load_config("../configs/models/embedding_model.json")

    # Initialize text generation model
    chat_model = CustomLLM(model_name=chat_model_config["model_name"],
                           cache_dir=chat_model_config["model_path"],
                           max_new_tokens=chat_model_config["max_new_tokens"],
                           task=chat_model_config["task"],
                           allow_download=chat_model_config["allow_download"],
                           load_in_8bit=chat_model_config["load_in_8bit"])
    
    print("Chat model initialized!")
    
    # Initialize sentence similarity model
    embedding_model = EmbeddingModel(model_name=embedding_model_config["model_name"],
                                     cache_dir=embedding_model_config["model_path"],
                                     device=set_device(embedding_model_config["device"]),
                                     allow_download=embedding_model_config["allow_download"])
    
    print("Sentence similarity model initialized!")

    # Partial function
    generate_response = partial(generate_base_response,
                           main_config=main_config,
                           chat_model=chat_model,
                           embedding_model=embedding_model)

    # Run main window loop
    root = tk.Tk()
    chat_window = ChatWindow(root=root, generate_answer=generate_response)
    root.mainloop()


if __name__ == "__main__":
    main()