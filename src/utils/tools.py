import pandas as pd
from transformers.agents import Tool

from language_models.sentence_similarity_model import EmbeddingModel
from language_models.text_generation_llm import CustomLLM
from utils.embedding_utils import select_movies

class MovieRetrieverTool(Tool):
    name = "movie_retriever"
    description = "It always must be used when user asks for a movie to watch. Retrieves some movies from the IMDB database that have the closest embeddings to the input query."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. It should only contain information from user's query and be semantically close to your target movies descriptions. \
Use the affirmative form rather than a question."
        }}
    output_type = "string"

    def __init__(self,
                 movie_db: pd.DataFrame,
                 embedding_model: EmbeddingModel,
                 top_n: int,
                 **kwargs) -> None:
        """
        Initializes the movie retriever tool.

        : param movie_db: (pd.DataFrame) - a database with information about different movies.
        : param embedding_model: (EmbeddingModel) - a sentence similarity model.
        : param top_n: (int) - number of movies to return.

        : return: (None) - this function does not return any value.
        """        
        super().__init__(**kwargs)
        self._movie_db = movie_db
        self._embedding_model = embedding_model
        self._top_n = top_n
        
    def forward(self, query: str) -> str:
        """
        Retrieves some of the most similar movies to the input query.

        : param query: (str) - an original user query to compare with.
        
        : return: (str) - a list of movies with some additional information.
        """
        print("\nMOVIE RETRIEVER CALLED\n")
        
        assert isinstance(query, str), "Your search query must be a string"
        movies = select_movies(movie_df=self._movie_db,
                               embedding_model=self._embedding_model,
                               user_input=query,
                               top_n=self._top_n)
        
        movie_summaries = "\n\n".join([f"Movie title: {row['title']}, director: {row['director']}, year: {row['year']}, \
rating: {row['rating']}, genres: {row['genres']}, description: {row['overview']}, link: {'imdb.com'+row['path']}" for _, row in movies.iterrows()])
        
        return movie_summaries
    

class PostprocessingTool(Tool):
    name = "movie_postprocessing"
    description = "Selects the most appropriate movies from a list with descriptions and other information retrieved by the movie_retriever tool. \
Takes the retrieved movies with information about them and user query as input, and outputs a final recommendation. Always use it when you have a raw list of possible movies. \
If you decide to use this tool, always immediately use its result as an argument in final_answer tool, do not take intermediate steps, it's important."

    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. It should only contain information from user's query, must be a single string and be \
semantically close to the target movies descriptions. Use the affirmative form rather than a question."
        },
        "retrieved_movies": {
            "type": "string",
            "description": "It must be a single string which contains a list of retrieved movies and information about them. \
After every movie it MUST be a brief description of what happens in this movie, and other information. \
Do not use your own observations, use only information from the tool you've got before."
        }}
    output_type = "string"
    
    def __init__(self,
                 prompt_template: str,
                 llm_engine: CustomLLM,
                 **kwargs) -> None:
        """
        Initializes the postprocessing tool with a prompt.

        : param prompt_template: (str) - a template for the final prompt.
        : param llm_engine: (CustomLLM) - a language model to apply postprocessing.

        : return: (None) - this function does not return any value.
        """
        super().__init__(**kwargs)
        self._template = prompt_template
        self._llm_engine = llm_engine

    def forward(self, query: str, retrieved_movies: str) -> str:
        """
        Applies postprocessing to the retrieved information.

        : param query: (str) - an original user query for context.
        : param retrieved_movies: (str) - raw information retrieved by the tool.
        
        : return: (str) - a final formatted response.
        """
        print("\nMOVIE POSTPROCESSING CALLED\n")

        final_response = self._template.format(retrieved_movies=retrieved_movies, user_query=query)
        return self._llm_engine(final_response)
    
