"""
Selection module for filtering papers based on semantic similarity.
"""

from typing import Tuple, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class PaperSelector:
    """
    Handles selection of papers based on similarity to a reference.
    """
    
    def __init__(self):
        """Initialize the paper selector."""
        self.similarities = None
        self.threshold = None
        
    def compute_similarities(self, paper_embeddings: np.ndarray, 
                            reference_embedding: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarities between papers and reference.
        
        Args:
            paper_embeddings: Array of shape (n_papers, embedding_dim)
            reference_embedding: Array of shape (embedding_dim,)
            
        Returns:
            Array of similarity scores of shape (n_papers,)
        """
        # Ensure reference embedding is 2D for sklearn
        if reference_embedding.ndim == 1:
            reference_embedding = reference_embedding.reshape(1, -1)
        
        # Compute cosine similarity
        similarities = cosine_similarity(paper_embeddings, reference_embedding)
        
        # Flatten to 1D array
        self.similarities = similarities.flatten()
        
        return self.similarities
    
    def compute_threshold(self, method: str = "mean_2std", 
                         custom_threshold: Optional[float] = None) -> float:
        """
        Compute or set the similarity threshold for selection.
        
        Args:
            method: Method for threshold computation:
                - "mean_2std": mean + 2 * std (default)
                - "mean_1std": mean + 1 * std
                - "median": median value
                - "percentile_75": 75th percentile
                - "percentile_90": 90th percentile
                - "custom": use custom_threshold value
            custom_threshold: Custom threshold value (used when method="custom")
            
        Returns:
            Computed threshold value
        """
        if self.similarities is None:
            raise ValueError("Must compute similarities first")
        
        if method == "custom":
            if custom_threshold is None:
                raise ValueError("custom_threshold must be provided when method='custom'")
            self.threshold = custom_threshold
        elif method == "mean_2std":
            mean = np.mean(self.similarities)
            std = np.std(self.similarities)
            self.threshold = mean + 2 * std
        elif method == "mean_1std":
            mean = np.mean(self.similarities)
            std = np.std(self.similarities)
            self.threshold = mean + 1 * std
        elif method == "median":
            self.threshold = np.median(self.similarities)
        elif method == "percentile_75":
            self.threshold = np.percentile(self.similarities, 75)
        elif method == "percentile_90":
            self.threshold = np.percentile(self.similarities, 90)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return self.threshold
    
    def select_papers(self, threshold: Optional[float] = None) -> np.ndarray:
        """
        Select papers above the similarity threshold.
        
        Args:
            threshold: Similarity threshold (uses self.threshold if None)
            
        Returns:
            Boolean array indicating which papers are selected
        """
        if self.similarities is None:
            raise ValueError("Must compute similarities first")
        
        if threshold is not None:
            self.threshold = threshold
        elif self.threshold is None:
            # Use default method if no threshold set
            self.compute_threshold(method="mean_2std")
        
        selected = self.similarities >= self.threshold
        
        return selected
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the similarity distribution.
        
        Returns:
            Dictionary with statistical measures
        """
        if self.similarities is None:
            raise ValueError("Must compute similarities first")
        
        stats = {
            "count": len(self.similarities),
            "mean": float(np.mean(self.similarities)),
            "std": float(np.std(self.similarities)),
            "median": float(np.median(self.similarities)),
            "min": float(np.min(self.similarities)),
            "max": float(np.max(self.similarities)),
            "q25": float(np.percentile(self.similarities, 25)),
            "q75": float(np.percentile(self.similarities, 75)),
            "q90": float(np.percentile(self.similarities, 90)),
            "q95": float(np.percentile(self.similarities, 95)),
        }
        
        if self.threshold is not None:
            selected_count = np.sum(self.similarities >= self.threshold)
            stats["threshold"] = float(self.threshold)
            stats["selected_count"] = int(selected_count)
            stats["selected_percentage"] = float(100 * selected_count / len(self.similarities))
        
        return stats
    
    def print_statistics(self):
        """Print formatted statistics about the similarity distribution."""
        stats = self.get_statistics()
        
        print("\n" + "=" * 60)
        print("SIMILARITY STATISTICS")
        print("=" * 60)
        print(f"Total papers:        {stats['count']:,}")
        print(f"\nDistribution:")
        print(f"  Mean:              {stats['mean']:.4f}")
        print(f"  Std:               {stats['std']:.4f}")
        print(f"  Median:            {stats['median']:.4f}")
        print(f"  Min:               {stats['min']:.4f}")
        print(f"  Max:               {stats['max']:.4f}")
        print(f"\nPercentiles:")
        print(f"  25th:              {stats['q25']:.4f}")
        print(f"  75th:              {stats['q75']:.4f}")
        print(f"  90th:              {stats['q90']:.4f}")
        print(f"  95th:              {stats['q95']:.4f}")
        
        if "threshold" in stats:
            print(f"\nSelection:")
            print(f"  Threshold:         {stats['threshold']:.4f}")
            print(f"  Selected papers:   {stats['selected_count']:,}")
            print(f"  Selection rate:    {stats['selected_percentage']:.2f}%")
        
        print("=" * 60 + "\n")