#!/usr/bin/env python3
"""
Example script demonstrating different ways to use the Zotero Similarity Selection tool.
"""

import subprocess
import os

# Example 1: Basic usage with auto-threshold
def example_basic():
    """Basic usage with automatic threshold computation."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Usage")
    print("="*70)
    
    cmd = [
        "python", "main.py",
        "-i", "data/zotero_library.csv",
        "-o", "data/selected_papers.csv"
    ]
    
    print("Command:", " ".join(cmd))
    print("\nThis will:")
    print("  - Use default reference text from config/reference.txt")
    print("  - Auto-compute threshold as mean + 2*std")
    print("  - Save selected papers to data/selected_papers.csv")
    

# Example 2: With visualization and statistics
def example_with_viz():
    """Usage with visualization and detailed statistics."""
    print("\n" + "="*70)
    print("EXAMPLE 2: With Visualization and Statistics")
    print("="*70)
    
    cmd = [
        "python", "main.py",
        "-i", "data/zotero_library.csv",
        "-o", "data/selected_papers.csv",
        "--visualize",
        "--stats"
    ]
    
    print("Command:", " ".join(cmd))
    print("\nThis will:")
    print("  - Generate a distribution plot (PNG)")
    print("  - Print detailed statistics")
    print("  - Help you understand the similarity distribution")


# Example 3: Custom threshold
def example_custom_threshold():
    """Usage with a custom similarity threshold."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom Threshold")
    print("="*70)
    
    cmd = [
        "python", "main.py",
        "-i", "data/zotero_library.csv",
        "-o", "data/selected_papers_strict.csv",
        "-t", "0.4",
        "--stats"
    ]
    
    print("Command:", " ".join(cmd))
    print("\nThis will:")
    print("  - Use a custom threshold of 0.4 (stricter selection)")
    print("  - Useful after reviewing the distribution from Example 2")


# Example 4: Different threshold methods
def example_threshold_methods():
    """Examples of different threshold computation methods."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Different Threshold Methods")
    print("="*70)
    
    methods = [
        ("mean_2std", "Mean + 2 × Std (default, ~95th percentile if normal)"),
        ("mean_1std", "Mean + 1 × Std (less strict, ~84th percentile)"),
        ("percentile_90", "90th percentile"),
        ("median", "Median (top 50%)"),
    ]
    
    for method, description in methods:
        print(f"\n{description}:")
        cmd = [
            "python", "main.py",
            "-i", "data/zotero_library.csv",
            "-o", f"data/selected_{method}.csv",
            "--threshold-method", method
        ]
        print("  Command:", " ".join(cmd))


# Example 5: Using a different model
def example_different_model():
    """Usage with a different sentence transformer model."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Different Model (Faster)")
    print("="*70)
    
    cmd = [
        "python", "main.py",
        "-i", "data/zotero_library.csv",
        "-o", "data/selected_papers.csv",
        "-m", "sentence-transformers/all-MiniLM-L6-v2",
        "--stats"
    ]
    
    print("Command:", " ".join(cmd))
    print("\nThis will:")
    print("  - Use a smaller, faster model")
    print("  - Good for very large libraries (10,000+ papers)")
    print("  - Slight trade-off in quality for speed")


# Example 6: Complete workflow
def example_complete_workflow():
    """Complete workflow with all options."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Complete Workflow")
    print("="*70)
    
    cmd = [
        "python", "main.py",
        "-i", "data/zotero_library.csv",
        "-o", "data/selected_papers_final.csv",
        "-r", "config/reference.txt",
        "-t", "0.35",
        "-m", "sentence-transformers/all-mpnet-base-v2",
        "--visualize",
        "--stats",
        "--batch-size", "64"
    ]
    
    print("Command:", " ".join(cmd))
    print("\nThis will:")
    print("  - Use custom reference text")
    print("  - Apply threshold of 0.35")
    print("  - Use best quality model")
    print("  - Generate visualization")
    print("  - Print detailed statistics")
    print("  - Process in larger batches for speed")


def main():
    """Display all examples."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "ZOTERO SIMILARITY SELECTION" + " "*26 + "║")
    print("║" + " "*22 + "EXAMPLE USAGE" + " "*33 + "║")
    print("╚" + "="*68 + "╝")
    
    example_basic()
    example_with_viz()
    example_custom_threshold()
    example_threshold_methods()
    example_different_model()
    example_complete_workflow()
    
    print("\n" + "="*70)
    print("TIPS")
    print("="*70)
    print("""
1. Start with Example 2 (--visualize --stats) to understand your data
2. Look at the distribution plot and statistics
3. Adjust the threshold based on what you see
4. For large libraries, consider using the MiniLM model (Example 5)
5. Edit config/reference.txt to match your research focus
    """)
    
    print("="*70)
    print("\nFor more information, see README.md")
    print()


if __name__ == "__main__":
    main()