# Data Directory

This directory is for storing input and output CSV files.

## Structure

- `*.csv` files are gitignored to avoid committing large data files
- Place your Zotero library export here (e.g., `zotero_library.csv`)
- Output files will be saved here by default

## Zotero Export Instructions

1. Open Zotero
2. Select your library or collection
3. Go to **File → Export Library...**
4. Choose format: **CSV**
5. Check options:
   - ✓ Include notes (to get abstracts)
   - ✓ Export files (optional)
6. Save to this directory

## Required CSV Columns

The exported CSV should contain at least:
- `Title` (or similar: title, Publication Title)
- `Abstract Note` (or similar: Abstract, abstract, Summary)

Other columns will be preserved in the output file.