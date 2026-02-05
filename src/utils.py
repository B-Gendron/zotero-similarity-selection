"""
Utility functions for I/O, visualization, and data processing.
"""

import os
from typing import Tuple, Optional, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_zotero_csv(filepath: str) -> pd.DataFrame:
    """
    Load Zotero library CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with Zotero library data
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    print(f"Loading Zotero library from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} papers")
    
    return df


def load_reference_text(filepath: str) -> str:
    """
    Load reference text from file.
    
    Args:
        filepath: Path to the text file
        
    Returns:
        Reference text as string
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Reference file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        raise ValueError(f"Reference file is empty: {filepath}")
    
    print(f"Loaded reference text from: {filepath}")
    print(f"Reference text length: {len(text)} characters")
    
    return text


def extract_title_abstract_columns(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Identify the title and abstract columns in the DataFrame.
    
    Args:
        df: DataFrame with Zotero data
        
    Returns:
        Tuple of (title_column_name, abstract_column_name)
    """
    # Common column names for title
    title_candidates = ['Title', 'title', 'Publication Title']
    title_col = None
    for candidate in title_candidates:
        if candidate in df.columns:
            title_col = candidate
            break
    
    if title_col is None:
        raise ValueError(f"Could not find title column. Available columns: {df.columns.tolist()}")
    
    # Common column names for abstract
    abstract_candidates = ['Abstract Note', 'Abstract', 'abstract', 'Summary']
    abstract_col = None
    for candidate in abstract_candidates:
        if candidate in df.columns:
            abstract_col = candidate
            break
    
    if abstract_col is None:
        raise ValueError(f"Could not find abstract column. Available columns: {df.columns.tolist()}")
    
    print(f"Using columns: Title='{title_col}', Abstract='{abstract_col}'")
    
    return title_col, abstract_col


def save_selected_papers(df: pd.DataFrame, output_path: str, 
                         similarities: np.ndarray, selected: np.ndarray):
    """
    Save selected papers to CSV file.
    
    Args:
        df: Original DataFrame
        output_path: Path to save the output CSV
        similarities: Array of similarity scores
        selected: Boolean array of selected papers
    """
    # Add similarity scores to dataframe
    df_output = df.copy()
    df_output['similarity_score'] = similarities
    
    # Filter to selected papers
    df_selected = df_output[selected].copy()
    
    # Sort by similarity score (descending)
    df_selected = df_selected.sort_values('similarity_score', ascending=False)
    
    # Save to CSV
    df_selected.to_csv(output_path, index=False)
    
    print(f"\nSaved {len(df_selected)} selected papers to: {output_path}")


def plot_similarity_distribution(similarities: np.ndarray, threshold: Optional[float] = None,
                                 output_path: Optional[str] = None):
    """
    Plot the distribution of similarity scores.
    
    Args:
        similarities: Array of similarity scores
        threshold: Threshold value to mark on the plot
        output_path: Path to save the plot (if None, display only)
    """
    plt.figure(figsize=(12, 6))
    
    # Create subplot layout
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(similarities, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0].axvline(np.mean(similarities), color='red', linestyle='--', 
                    linewidth=2, label=f'Mean: {np.mean(similarities):.3f}')
    
    if threshold is not None:
        axes[0].axvline(threshold, color='green', linestyle='--', 
                       linewidth=2, label=f'Threshold: {threshold:.3f}')
    
    axes[0].set_xlabel('Similarity Score', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].set_title('Distribution of Similarity Scores', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Box plot
    box = axes[1].boxplot(similarities, vert=True, patch_artist=True,
                          boxprops=dict(facecolor='lightblue', alpha=0.7))
    
    if threshold is not None:
        axes[1].axhline(threshold, color='green', linestyle='--', 
                       linewidth=2, label=f'Threshold: {threshold:.3f}')
        axes[1].legend()
    
    axes[1].set_ylabel('Similarity Score', fontsize=12)
    axes[1].set_title('Similarity Score Distribution', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved visualization to: {output_path}")
    
    plt.close()


def validate_dataframe(df: pd.DataFrame, title_col: str, abstract_col: str):
    """
    Validate that the DataFrame has the necessary data.
    
    Args:
        df: DataFrame to validate
        title_col: Name of title column
        abstract_col: Name of abstract column
    """
    if len(df) == 0:
        raise ValueError("DataFrame is empty")
    
    # Check for missing data
    missing_titles = df[title_col].isna().sum()
    missing_abstracts = df[abstract_col].isna().sum()
    
    if missing_titles == len(df):
        raise ValueError("All titles are missing")
    
    print(f"\nData validation:")
    print(f"  Papers with titles: {len(df) - missing_titles} / {len(df)}")
    print(f"  Papers with abstracts: {len(df) - missing_abstracts} / {len(df)}")
    
    if missing_titles > 0:
        print(f"  Warning: {missing_titles} papers missing titles")
    if missing_abstracts > 0:
        print(f"  Warning: {missing_abstracts} papers missing abstracts")


def create_output_directory(output_path: str):
    """
    Create output directory if it doesn't exist.
    
    Args:
        output_path: Path to output file
    """
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")