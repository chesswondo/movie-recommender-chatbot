import os
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    """Class for working with sentence transformer models from Hugging Face."""

    def __init__(self,
                 model_name: str,
                 cache_dir: str,
                 device: str,
                 allow_download: bool) -> None:
        """
        Initializes an instance of EmbeddingModel.

        : param model_name: (str) - name of the sentence transformer model.
        : param cache_dir: (str) - path to the directory where to store model weights.
        : param device: (str) - device for running the model.
        : param allow_download: (bool) - whether to download model weights if they are not available locally.

        : return: (None) - this function does not return any value.
        """
        
        # Check folder path
        if not allow_download and not os.path.exists(cache_dir):
            print(os.path.abspath(cache_dir))
            raise ValueError("Folder with model weights doesn't exist. \
                             Check specified folder path or change allow_download argument to True")
        
        # Use specified model and define the local cache directory
        self._embedding_model = SentenceTransformer(model_name, cache_folder=cache_dir).to(device)


    def encode(self,
               input_string: str) -> str:
        
        return self._embedding_model.encode(input_string)