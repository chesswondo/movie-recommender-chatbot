from language_models.text_generation_llm import CustomLLM
from language_models.sentence_similarity_model import EmbeddingModel
from utils.dataset_utils import filter_dataframe
from utils.llm_utils import create_input_message, retrieve_json
from utils.embedding_utils import select_movies
from utils.common_utils import extract_between
from interface.window import ChatWindow
import pandas as pd
import tkinter as tk

def generate_response(user_input: str):

    # Initialize text generation model
    chat_model = CustomLLM(model_name="microsoft/Phi-3.5-mini-instruct",
                           cache_dir="models/Phi-3.5-mini-instruct",
                           max_new_tokens=128,
                           device="cuda",
                           task="text-generation")
    
    print("Chat model initialized!")

    input_message = create_input_message(user_input=user_input)
    messages = input_message['messages']
    parser = input_message['parser']

    model_response = chat_model(messages)
    final_response = retrieve_json(model_response=model_response,
                                   parser=parser)
    
    print("Final json response received!")
    
    # Initialize sentence similarity model
    embedding_model = EmbeddingModel(model_name="all-mpnet-base-v2",
                                     cache_dir="models/all-mpnet-base-v2",
                                     device="cpu")
    
    print("Sentence similarity model initialized!")
    print("Final response:", final_response)
    print(f"Filters:\nYear: {final_response['year']},\nGenre: {final_response['genre']}\n")

    movie_embeddings_df = pd.read_pickle('datasets/IMDB_embeddings.pkl')
    filtered_embeddings = filter_dataframe(movie_embeddings_df,
                                    year=final_response['year'],
                                    genre=final_response['genre'])
    
    print("Filtered movie embeddings received!")
    
    selected_movies = select_movies(movie_df=filtered_embeddings,
                                    embedding_model=embedding_model,
                                    user_input=final_response['description'],
                                    top_n=5)
    
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
    #user_input = "I wanna watch some comedy movies about animals"
    root = tk.Tk()
    chat_window = ChatWindow(root=root, generate_answer=generate_response)
    root.mainloop()


if __name__ == "__main__":
    main()