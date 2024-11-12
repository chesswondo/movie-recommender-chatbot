from language_models.sentence_similarity_model import EmbeddingModel
import pandas as pd
import argparse
from utils.common_utils import load_config, set_device

def calculate_embeddings(input_data_path: str,
                         output_data_path: str,
                         embedding_model_config: dict,
                         device: str) -> None:

    try:
        movie_df = pd.read_csv(input_data_path)
    except Exception:
        print("Please, provide a correct path to .csv file as an input.")
        return

    # Initialize the model for sentence embeddings
    embedding_model = EmbeddingModel(model_name=embedding_model_config["model_name"],
                                     cache_dir=embedding_model_config["model_path"],
                                     device=device,
                                     allow_download=True)

    # Compute embeddings for all overviews
    try:
        movie_df['embeddings'] = movie_df['overview'].apply(lambda x: embedding_model.encode(x))
    except Exception:
        print("Make sure that your .csv file has 'overview' column.")
        return
    
    # Export new file with embeddings
    try:
        movie_df.to_pickle(output_data_path)
    except Exception:
        print("Please, provide a correct path to .pkl file as an output.")
        return
    
    print("File with calculated embeddings was successfully stored in", output_data_path)


def main():
    parser = argparse.ArgumentParser(description="Calculate embeddings for a dataset")
    parser.add_argument(
        "--input_file", help="Path to the dataset", required=False, default="../data/IMDB_cleaned.csv", dest="input_file"
    )
    parser.add_argument(
        "--output_file", help="Path to the output file", required=False, default="../data/IMDB_embeddings.pkl", dest="output_file"
    )
    parser.add_argument(
        "--device", help="Device for running the sentence transformer model", required=False, default=-1, dest="device"
    )
    parser.add_argument(
        "--allow_download", help="Allow to download model weights", required=False, default=True, dest="allow_download"
    )

    # Load configs
    embedding_model_config = load_config("../configs/models/embedding_model.json")

    # Parse user data
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    device = set_device(args.device) if args.device != -1 else set_device(embedding_model_config["device"])

    # Calculate the embeddings
    calculate_embeddings(input_data_path=input_file,
                         output_data_path=output_file,
                         embedding_model_config=embedding_model_config,
                         device=device)

if __name__ == "__main__":
    main()