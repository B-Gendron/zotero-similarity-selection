"""
Embeddings module for computing sentence embeddings using Sentence Transformers.
"""

from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


class EmbeddingComputer:
    """
    Handles computation of sentence embeddings using pre-trained models.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        """
        Initialize the embedding computer with a specific model.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        
    def encode_texts(self, texts: List[str], show_progress: bool = True, 
                     batch_size: int = 32) -> np.ndarray:
        """
        Encode a list of texts into embeddings.
        
        Args:
            texts: List of text strings to encode
            show_progress: Whether to show a progress bar
            batch_size: Batch size for encoding
            
        Returns:
            numpy array of shape (n_texts, embedding_dim)
        """
        if not texts:
            raise ValueError("Empty text list provided")
            
        # Clean texts: replace None with empty string
        cleaned_texts = [str(text) if text is not None else "" for text in texts]
        
        print(f"Encoding {len(cleaned_texts)} texts...")
        embeddings = self.model.encode(
            cleaned_texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def encode_single(self, text: str) -> np.ndarray:
        """
        Encode a single text into an embedding.
        
        Args:
            text: Text string to encode
            
        Returns:
            numpy array of shape (embedding_dim,)
        """
        if text is None:
            text = ""
        
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False
        )
        
        return embedding


def combine_title_abstract(title: str, abstract: str, 
                           separator: str = " [SEP] ") -> str:
    """
    Combine title and abstract into a single text for embedding.
    
    Args:
        title: Paper title
        abstract: Paper abstract
        separator: Separator between title and abstract
        
    Returns:
        Combined text string
    """
    title = str(title) if title is not None else ""
    abstract = str(abstract) if abstract is not None else ""
    
    # Remove extra whitespace
    title = " ".join(title.split())
    abstract = " ".join(abstract.split())
    
    if title and abstract:
        return f"{title}{separator}{abstract}"
    elif title:
        return title
    elif abstract:
        return abstract
    else:
        return ""