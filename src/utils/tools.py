import pandas as pd
from transformers.agents import Tool
from language_models.sentence_similarity_model import EmbeddingModel
from utils.embedding_utils import select_movies
import json

class MovieRetrieverTool(Tool):
    name = "movie_retriever"
    description = (
        "It always must be used when user asks for a movie to watch. Retrieves some movies from the IMDB database that have the closest embeddings to the input query."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be semantically close to your target movies descriptions. Use the affirmative form rather than a question.",
        }},
    output_type = "string"

    def __init__(self, movie_db: pd.DataFrame,
                 embedding_model: EmbeddingModel,
                 top_n: int) -> None:
        
        self._movie_db = movie_db
        self._embedding_model = embedding_model
        self._top_n = top_n
        
    def forward(self, query: str) -> str:

        print("\nMOVIE RETRIEVER CALLED\n")
        
        assert isinstance(query, str), "Your search query must be a string"
        movies = select_movies(movie_df=self._movie_db,
                               embedding_model=self._embedding_model,
                               user_input=query,
                               top_n=self._top_n)
        
        movie_summaries = "\n\n".join([f"{row['title']}: {row['overview']}" for _, row in movies.iterrows()])
        return movie_summaries
    
class PostprocessingTool(Tool):
    name = "movie_postprocessing"
    description = (
        "Selects the most appropriate movie from a list with descriptions retrieved by the movie_retriever tool. \
        Takes the retrieved movies with their descriptions and user query as input and outputs a single selected movie. Always used after getting a list of movies."
    )

    inputs = {
        "user_query": {
            "type": "string",
            "description": "The query to perform. It must be a single string and be semantically close to the target movies descriptions. \
                Use the affirmative form rather than a question.",
        },
        "retrieved_movies": {
            "type": "string",
            "description": "It must be a single string which contains a list of retrieved movies and their descriptions. \
            After every movie it MUST be a brief description of what happens in this movie. \
            This string should not contain any additional information. Do not use your own observations, use only information from the tool you've got before."
        }},
    output_type = "string"
    
    def __init__(self, prompt_template: str):
        """
        Initializes the postprocessing tool with a template.

        :param prompt_template: (str) - Template for the final prompt.
        """
        self._template = prompt_template

    def forward(self, user_query: str, retrieved_movies: str) -> str:
        """
        Applies postprocessing to the retrieved information.

        :param retrieved_movies: (str) - The raw information retrieved by the tool.
        :param user_query: (str) - The original user query for context.
        
        :return: (str) - The final formatted response.
        """
        print("\nMOVIE POSTPROCESSING CALLED\n")
        final_response = self._template.format(retrieved_info=retrieved_movies, user_query=user_query)
        return json.dumps({"final_response": final_response})
