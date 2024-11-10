import pandas as pd
import numpy as np
import hnswlib  # for vector search
from language_models.sentence_similarity_model import EmbeddingModel

def select_movies(movie_df: pd.DataFrame,
                  embedding_model: EmbeddingModel,
                  user_input: str,
                  top_n: int):

    movie_embeddings = np.vstack(movie_df['embeddings'].values)

    # Create an HNSW index for efficient similarity search
    dimension = movie_embeddings.shape[1]  # Dimension of embeddings
    num_elements = movie_embeddings.shape[0]  # Number of items to index

    # Initialize HNSWLib index
    hnsw_index = hnswlib.Index(space='cosine', dim=dimension)
    hnsw_index.init_index(max_elements=num_elements, ef_construction=100, M=16)

    # Add the movie embeddings to the HNSW index
    hnsw_index.add_items(movie_embeddings)

    # Calculate embeddings from user input
    user_embedding = embedding_model.encode(user_input)

    # Retrieve top-k similar movies based on cosine similarity
    labels, distances = hnsw_index.knn_query(np.array([user_embedding]), k=top_n)

    # Fetch selected movies based on returned indices
    selected_movies = movie_df.iloc[labels[0]]
    
    return selected_movies