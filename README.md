# Movie Recommender Chatbot

## About
Here is an implementation of chatbot which can recommend you a movie based on your query.

Currently it uses Microsoft's [Phi-3.5-mini-instruct](https://huggingface.co/microsoft/Phi-3.5-mini-instruct) as a main model for text generation.
On average it takes from 30 seconds to a minute to get a response on a single RTX 4080 using 8-bit quantization.

Model takes your input, retrieves all important information, such as description, genres and so on, and then selects some movies
from Kaggle IMDB dataset using RAG (Retrieval Augmented Generation), finally giving you a short recommendation.

As a sentence transformer model currently we use [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2).
If you want to use an another model, don't forget to recalculate all embeddings in the dataset.

## Installation
