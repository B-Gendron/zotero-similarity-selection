#!/usr/bin/env python3
"""
Main script for selecting relevant papers from Zotero library using semantic similarity.

Usage:
    python main.py --input data/zotero_library.csv --output data/selected_papers.csv
"""

import argparse
import os
import sys
from pathlib import Path

from src import (
    EmbeddingComputer,
    combine_title_abstract,
    PaperSelector,
    load_zotero_csv,
    load_reference_text,
    extract_title_abstract_columns,
    save_selected_papers,
    plot_similarity_distribution,
    validate_dataframe,
    create_output_directory
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Select relevant papers from Zotero library using semantic similarity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with auto-threshold
  python main.py -i data/library.csv -o data/selected.csv
  
  # With custom threshold and visualization
  python main.py -i data/library.csv -o data/selected.csv -t 0.3 -v
  
  # With custom reference file and statistics
  python main.py -i data/library.csv -o data/selected.csv -r my_reference.txt --stats
  
  # Using a different model
  python main.py -i data/library.csv -o data/selected.csv -m sentence-transformers/all-MiniLM-L6-v2
        """
    )
    
    # Required arguments
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Path to input CSV file from Zotero export'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Path to output CSV file for selected papers'
    )
    
    # Optional arguments
    parser.add_argument(
        '-r', '--reference',
        type=str,
        default='config/reference.txt',
        help='Path to reference text file (default: config/reference.txt)'
    )
    
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        default=None,
        help='Similarity threshold for selection (default: auto-computed as mean + 2*std)'
    )
    
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='sentence-transformers/all-mpnet-base-v2',
        help='Sentence transformer model name (default: all-mpnet-base-v2)'
    )
    
    parser.add_argument(
        '--threshold-method',
        type=str,
        choices=['mean_2std', 'mean_1std', 'median', 'percentile_75', 'percentile_90', 'custom'],
        default='mean_2std',
        help='Method for computing threshold (default: mean_2std)'
    )
    
    parser.add_argument(
        '-v', '--visualize',
        action='store_true',
        help='Generate similarity distribution plot'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Print detailed statistics about the selection'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=32,
        help='Batch size for encoding (default: 32)'
    )
    
    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_args()
    
    print("=" * 70)
    print("ZOTERO SIMILARITY SELECTION")
    print("=" * 70)
    print()
    
    # Validate inputs
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    if not os.path.exists(args.reference):
        print(f"Error: Reference file not found: {args.reference}")
        sys.exit(1)
    
    # Create output directory if needed
    create_output_directory(args.output)
    
    try:
        # Step 1: Load data
        print("Step 1: Loading data")
        print("-" * 70)
        df = load_zotero_csv(args.input)
        reference_text = load_reference_text(args.reference)
        
        # Step 2: Extract and validate columns
        print("\nStep 2: Extracting title and abstract columns")
        print("-" * 70)
        title_col, abstract_col = extract_title_abstract_columns(df)
        validate_dataframe(df, title_col, abstract_col)
        
        # Step 3: Combine titles and abstracts
        print("\nStep 3: Combining titles and abstracts")
        print("-" * 70)
        paper_texts = [
            combine_title_abstract(row[title_col], row[abstract_col])
            for _, row in df.iterrows()
        ]
        print(f"Created {len(paper_texts)} combined text representations")
        
        # Step 4: Initialize embedding computer
        print("\nStep 4: Initializing embedding model")
        print("-" * 70)
        embedder = EmbeddingComputer(model_name=args.model)
        
        # Step 5: Encode reference text
        print("\nStep 5: Encoding reference text")
        print("-" * 70)
        reference_embedding = embedder.encode_single(reference_text)
        print(f"Reference embedding shape: {reference_embedding.shape}")
        
        # Step 6: Encode papers
        print("\nStep 6: Encoding papers")
        print("-" * 70)
        paper_embeddings = embedder.encode_texts(
            paper_texts,
            show_progress=True,
            batch_size=args.batch_size
        )
        print(f"Paper embeddings shape: {paper_embeddings.shape}")
        
        # Step 7: Compute similarities
        print("\nStep 7: Computing similarities")
        print("-" * 70)
        selector = PaperSelector()
        similarities = selector.compute_similarities(paper_embeddings, reference_embedding)
        print(f"Computed {len(similarities)} similarity scores")
        
        # Step 8: Determine threshold
        print("\nStep 8: Determining selection threshold")
        print("-" * 70)
        if args.threshold is not None:
            threshold = selector.compute_threshold(method="custom", custom_threshold=args.threshold)
            print(f"Using custom threshold: {threshold:.4f}")
        else:
            threshold = selector.compute_threshold(method=args.threshold_method)
            print(f"Computed threshold ({args.threshold_method}): {threshold:.4f}")
        
        # Step 9: Select papers
        print("\nStep 9: Selecting papers")
        print("-" * 70)
        selected = selector.select_papers(threshold)
        n_selected = selected.sum()
        print(f"Selected {n_selected} papers ({100 * n_selected / len(df):.2f}%)")
        
        # Step 10: Print statistics if requested
        if args.stats:
            selector.print_statistics()
        
        # Step 11: Save results
        print("Step 10: Saving results")
        print("-" * 70)
        save_selected_papers(df, args.output, similarities, selected)
        
        # Step 12: Generate visualization if requested
        if args.visualize:
            print("\nStep 11: Generating visualization")
            print("-" * 70)
            plot_path = args.output.replace('.csv', '_distribution.png')
            plot_similarity_distribution(similarities, threshold, plot_path)
        
        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total papers processed:  {len(df):,}")
        print(f"Papers selected:         {n_selected:,} ({100 * n_selected / len(df):.2f}%)")
        print(f"Similarity threshold:    {threshold:.4f}")
        print(f"Output saved to:         {args.output}")
        if args.visualize:
            print(f"Visualization saved to:  {plot_path}")
        print("=" * 70)
        print("\n✓ Selection completed successfully!\n")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()