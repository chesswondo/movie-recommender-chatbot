import os
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self,
                 model_name: str,
                 cache_dir: str,
                 device: str,
                 allow_download: bool=False) -> None:
        
        # Check folder path
        if not allow_download and not os.path.exists(cache_dir):
            print(os.path.abspath(cache_dir))
            raise ValueError("Folder with model weights doesn't exist. \
                             Check specified folder path or change allow_download argument to True")
        
        # Specify the local folder for the model weights and device for the model to run on
        self._cache_dir = cache_dir
        self._device = device

        # Use specified model and define the local cache directory
        self._embedding_model = SentenceTransformer(model_name, cache_folder=cache_dir).to(device)


    def encode(self,
               input_string: str) -> str:
        
        return self._embedding_model.encode(input_string)