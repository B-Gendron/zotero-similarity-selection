"""
Zotero Similarity Selection package.
"""

from .embeddings import EmbeddingComputer, combine_title_abstract
from .selection import PaperSelector
from .utils import (
    load_zotero_csv,
    load_reference_text,
    extract_title_abstract_columns,
    save_selected_papers,
    plot_similarity_distribution,
    validate_dataframe,
    create_output_directory
)

__version__ = "1.0.0"
__all__ = [
    "EmbeddingComputer",
    "combine_title_abstract",
    "PaperSelector",
    "load_zotero_csv",
    "load_reference_text",
    "extract_title_abstract_columns",
    "save_selected_papers",
    "plot_similarity_distribution",
    "validate_dataframe",
    "create_output_directory",
]