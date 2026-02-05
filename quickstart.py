#!/usr/bin/env python3
"""
Quick start script to test the tool with example data.

This script runs the tool on the example CSV to verify everything is working.
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed."""
    print("Checking dependencies...")
    try:
        import sentence_transformers
        import pandas
        import numpy
        import sklearn
        import matplotlib
        print("✓ All dependencies installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False

def run_example():
    """Run the tool on example data."""
    print("\n" + "="*70)
    print("RUNNING QUICK START EXAMPLE")
    print("="*70 + "\n")
    
    cmd = [
        sys.executable, "main.py",
        "-i", "data/example_library.csv",
        "-o", "data/example_output.csv",
        "--visualize",
        "--stats"
    ]
    
    print("Running command:")
    print("  " + " ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "="*70)
        print("✓ Quick start completed successfully!")
        print("="*70)
        print("\nNext steps:")
        print("1. Check data/example_output.csv to see the results")
        print("2. View the distribution plot (PNG file)")
        print("3. Edit config/reference.txt with your research description")
        print("4. Export your Zotero library to CSV")
        print("5. Run: python main.py -i your_library.csv -o output.csv")
        print()
    else:
        print("\n✗ Quick start failed. Please check the error messages above.")
        sys.exit(1)

def main():
    """Main function."""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*10 + "ZOTERO SIMILARITY SELECTION - QUICK START" + " "*17 + "║")
    print("╚" + "="*68 + "╝\n")
    
    if not check_dependencies():
        sys.exit(1)
    
    print("\nThis will run the tool on example data to verify everything works.")
    response = input("\nContinue? [Y/n]: ").strip().lower()
    
    if response in ['', 'y', 'yes']:
        run_example()
    else:
        print("Quick start cancelled.")

if __name__ == "__main__":
    main()