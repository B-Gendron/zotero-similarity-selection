#!/usr/bin/env python3
"""
Convert selected papers CSV to BibTeX format for re-importing into Zotero.

Usage:
    python csv2bibtex.py -i data/selected_papers.csv -o data/selected_papers.bib
"""

import argparse
import pandas as pd
import re
import sys
from pathlib import Path


def clean_for_bibtex(text):
    """
    Clean text for BibTeX format.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text safe for BibTeX
    """
    if pd.isna(text) or text is None:
        return ""
    
    text = str(text)
    # Remove or escape problematic characters
    text = text.replace('{', '\\{').replace('}', '\\}')
    text = text.replace('%', '\\%')
    text = text.replace('&', '\\&')
    text = text.replace('_', '\\_')
    
    return text


def generate_citation_key(row, index):
    """
    Generate a unique citation key for the entry.
    
    Args:
        row: DataFrame row
        index: Row index for uniqueness
        
    Returns:
        Citation key string
    """
    # Try to extract first author's last name
    author = row.get('Author', '')
    year = row.get('Publication Year', row.get('Year', ''))
    
    if pd.notna(author) and author:
        # Extract first author's last name
        author = str(author)
        if ',' in author:
            # Format: "LastName, FirstName"
            last_name = author.split(',')[0].strip()
        elif ';' in author:
            # Multiple authors: "Author1; Author2"
            first_author = author.split(';')[0].strip()
            if ',' in first_author:
                last_name = first_author.split(',')[0].strip()
            else:
                # Format: "FirstName LastName"
                parts = first_author.split()
                last_name = parts[-1] if parts else 'Unknown'
        else:
            # Single name
            parts = author.split()
            last_name = parts[-1] if parts else author
        
        # Clean the last name for citation key
        last_name = re.sub(r'[^a-zA-Z]', '', last_name)
    else:
        last_name = "Unknown"
    
    # Add year if available
    if pd.notna(year) and year:
        year_str = str(year).strip()
        # Extract just the year number
        year_match = re.search(r'\d{4}', year_str)
        if year_match:
            year_str = year_match.group()
        key = f"{last_name}{year_str}"
    else:
        key = last_name
    
    # Add index to ensure uniqueness
    key = f"{key}_{index}"
    
    return key


def map_item_type(item_type):
    """
    Map Zotero item type to BibTeX entry type.
    
    Args:
        item_type: Zotero item type
        
    Returns:
        BibTeX entry type
    """
    if pd.isna(item_type):
        return 'article'
    
    item_type = str(item_type).lower()
    
    # Mapping from Zotero to BibTeX types
    type_mapping = {
        'journalarticle': 'article',
        'conferencepaper': 'inproceedings',
        'book': 'book',
        'booksection': 'incollection',
        'thesis': 'phdthesis',
        'report': 'techreport',
        'webpage': 'misc',
        'preprint': 'article',
        'manuscript': 'unpublished',
    }
    
    # Remove spaces and special characters
    item_type = re.sub(r'[^a-z]', '', item_type)
    
    return type_mapping.get(item_type, 'article')


def csv_to_bibtex(input_csv, output_bib):
    """
    Convert CSV file to BibTeX format.
    
    Args:
        input_csv: Path to input CSV file
        output_bib: Path to output BibTeX file
    """
    print(f"Reading CSV from: {input_csv}")
    df = pd.read_csv(input_csv)
    print(f"Found {len(df)} entries")
    
    # Common Zotero CSV column mappings
    column_mapping = {
        'Title': 'title',
        'Author': 'author',
        'Publication Year': 'year',
        'Year': 'year',
        'Abstract Note': 'abstract',
        'Abstract': 'abstract',
        'DOI': 'doi',
        'URL': 'url',
        'Publication Title': 'journal',
        'Journal': 'journal',
        'Publisher': 'publisher',
        'Volume': 'volume',
        'Issue': 'number',
        'Pages': 'pages',
        'Item Type': 'entry_type',
        'Book Title': 'booktitle',
        'Conference Name': 'booktitle',
        'Series': 'series',
        'Edition': 'edition',
        'Place': 'address',
        'ISBN': 'isbn',
        'ISSN': 'issn',
    }
    
    bibtex_entries = []
    
    for idx, row in df.iterrows():
        # Generate citation key
        cite_key = generate_citation_key(row, idx + 1)
        
        # Determine entry type
        item_type = row.get('Item Type', 'article')
        entry_type = map_item_type(item_type)
        
        # Start BibTeX entry
        entry_lines = [f"@{entry_type}{{{cite_key},"]
        
        # Add fields
        for csv_col, bib_field in column_mapping.items():
            if csv_col in row and pd.notna(row[csv_col]) and row[csv_col] != '':
                if bib_field == 'entry_type':
                    continue  # Already handled
                
                value = clean_for_bibtex(row[csv_col])
                
                # Special handling for author field
                if bib_field == 'author':
                    # Convert "Last, First; Last2, First2" to "Last, First and Last2, First2"
                    value = value.replace(';', ' and')
                
                # Special handling for year - extract just the year
                if bib_field == 'year':
                    year_match = re.search(r'\d{4}', str(value))
                    if year_match:
                        value = year_match.group()
                
                entry_lines.append(f"  {bib_field} = {{{value}}},")
        
        # Close entry
        entry_lines.append("}\n")
        
        bibtex_entries.append('\n'.join(entry_lines))
    
    # Write to file
    print(f"Writing BibTeX to: {output_bib}")
    with open(output_bib, 'w', encoding='utf-8') as f:
        f.write('\n'.join(bibtex_entries))
    
    print(f"✓ Successfully created BibTeX file with {len(bibtex_entries)} entries")
    print(f"\nTo import into Zotero:")
    print(f"  1. Open Zotero")
    print(f"  2. File → Import...")
    print(f"  3. Select: {output_bib}")
    print(f"  4. Choose import options")
    print(f"  5. Click 'Continue'")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert selected papers CSV to BibTeX format for Zotero import",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert selected papers to BibTeX
  python csv_to_bibtex.py -i data/selected_papers.csv -o data/selected_papers.bib
  
  # With custom input/output
  python csv_to_bibtex.py -i my_selection.csv -o my_papers.bib
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Path to input CSV file (from Zotero or main.py output)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Path to output BibTeX file (.bib)'
    )
    
    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_args()
    
    print("=" * 70)
    print("CSV TO BIBTEX CONVERTER")
    print("=" * 70)
    print()
    
    # Validate input
    if not Path(args.input).exists():
        print(f"✗ Error: Input file not found: {args.input}")
        sys.exit(1)
    
    # Create output directory if needed
    output_dir = Path(args.output).parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created output directory: {output_dir}")
    
    try:
        csv_to_bibtex(args.input, args.output)
        print("\n✓ Conversion completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()