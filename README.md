# ZSS: Zotero Similarity Selection
<p align="center">
  <img 
    src="https://github.com/user-attachments/assets/ee35c734-6384-4737-8139-3f4831dfa3ed"
    alt="zss-logo-2-upscaled"
    width="600"
  />
</p>

A tool for filtering and selecting relevant papers from large Zotero libraries using state-of-the-art sentence embeddings and semantic similarity. This tool has been developed with the assistance of Claude (see [AI Assistance Details](#ai-assistance-details) Section).

## Overview

This tool helps researchers to efficiently filter thousands of papers gathered in a `.csv` file (for instance exported from Zotero) by computing semantic similarity between paper titles/abstracts and a reference description of your research scope. The selection is then exported in `.csv` and can be further converted to BiBTeX to be imported in Zotero. 

## Features

- Computes semantic similarity between title/abstract of papers and a reference text using Sentence-BERT encoding (Reimers & Gurevych, 2019) and the `sentence-transformers` library (see [Models](#models) Section)
- Analyzes similarity score distributions to derive data-driven similarity thresholds (both automatic threshold estimation and manual threshold specification)
- Provides visualizations to facilitate interpretation of similarity scores and the choice of an appropriate thresholding strategy
- Converts `.csv` output files to `.bib` to support Zotero import (import of `.csv` files directly is currently not possible in Zotero)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/B-Gendron/zotero-similarity-selection.git
cd zotero-similarity-selection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. **Export your Zotero library** to CSV format (File → Export Library → CSV)

2. **Create a reference text file** describing your research scope:
```bash
nano config/reference.txt
```

3. **Run the selection tool**:
```bash
python main.py --input data/zotero_library.csv --output data/selected_papers.csv
```

## Usage

### Basic Usage

```bash
python main.py --input <input_csv> --output <output_csv>
```

### Advanced Options

```bash
python main.py \
  --input data/zotero_library.csv \
  --output data/selected_papers.csv \
  --reference config/reference.txt \
  --threshold 0.3 \
  --model sentence-transformers/all-mpnet-base-v2 \
  --visualize
```

### Arguments

- `--input`, `-i`: Path to input CSV file from Zotero export (required)
- `--output`, `-o`: Path to output CSV file for selected papers (required)
- `--reference`, `-r`: Path to reference text file (default: `config/reference.txt`)
- `--threshold`, `-t`: Similarity threshold for selection (default: auto-computed as mean + 2*std)
- `--model`, `-m`: Sentence transformer model name (default: `sentence-transformers/all-mpnet-base-v2`)
- `--visualize`, `-v`: Generate similarity distribution plot
- `--stats`: Print detailed statistics about the selection

## Project Structure

```
zotero-similarity-selection/
├── main.py                 # Run the app 
├── examples.py
├── examples.py
├── csv2bibtex.py           # Convert .csv file to .bib
├── main.py           
├── src/
│   ├── __init__.py
│   ├── embeddings.py       
│   ├── selection.py        # Selection of papers from Zotero
│   └── utils.py            
├── config/
│   └── reference.txt       # Reference paragraph for your research scope
├── data/                   # Directory to store Zotero exports
│   ├── .gitkeep
│   └── README.md
├── requirements.txt        
├── .gitignore
└── README.md
```

## How It Works

1. **Load Data**: Reads the Zotero CSV export and extracts titles and abstracts
2. **Encode Reference**: Computes sentence embeddings for your reference paragraph
3. **Encode Papers**: Computes embeddings for each paper's title + abstract
4. **Compute Similarity**: Computes cosine similarity between each paper and the reference
5. **Filter Papers**: Selects papers above the similarity threshold
6. **Export Results**: Saves selected papers to a new CSV file

## Similarity Threshold Selection

By default, the tool uses **mean + 2×std** as the threshold, which typically captures papers that are significantly more similar to your reference than average. You can:

- Let the tool auto-compute the threshold (recommended for first run)
- Specify a custom threshold with `--threshold`
- Use `--visualize` to see the distribution and then adjust your threshold accordingly

## Example Reference Text

Create a `config/reference.txt` file that explain the scope of your research topic, using relevant key words. Here is an example:

```
This research focuses on the application of machine learning techniques 
to climate change prediction, particularly deep learning models for 
temperature forecasting and extreme weather event detection. We are 
interested in methods that leverage satellite imagery, time-series analysis, 
and ensemble modeling approaches.
```

## CSV Format Requirements

The input CSV should contain at least these columns (standard Zotero export):
- `Title`: Paper title
- `Abstract Note` or `Abstract`: Paper abstract

Other columns will be preserved in the output.

## Output

The tool generates:
- A CSV file with selected papers (same format as input, plus `similarity_score` column)
- Optional: A visualization of the similarity distribution (PNG)
- Console output with statistics about the selection

## Re-importing to Zotero

Zotero doesn't support CSV import, but you can convert your selection to BibTeX format using the following script:

```bash
python csv_to_bibtex.py -i data/selected_papers.csv -o data/selected_papers.bib
```

Then in Zotero:
1. File → Import...
2. Select the `.bib` file
3. Choose import options
4. Click Continue

Your selected papers will be imported into a new collection!

## Tips

- **First run**: Use `--visualize --stats` to understand your similarity distribution
- **Adjust threshold**: If too many/few papers selected, adjust the threshold value
- **Multiple references**: For complex projects, combine multiple reference paragraphs
- **Model selection**: The default model balances quality and speed; try `all-MiniLM-L6-v2` for faster processing on large libraries

## Models

Recommended sentence transformer models:
- `sentence-transformers/all-mpnet-base-v2` (default): Best quality, slower
- `sentence-transformers/all-MiniLM-L6-v2`: Fast, good quality
- `sentence-transformers/multi-qa-mpnet-base-dot-v1`: Optimized for Q&A/semantic search

See [Sentence Transformers documentation](https://www.sbert.net/docs/pretrained_models.html) for more options.

## AI Assistance Details

### Model

Claude Sonnet 4.5

### Prompt

```
I want to select relevant papers from a zotero library with 
thousands of papers from an automatic extraction. The idea is 
the following:
* export all the library (in a csv format, I suppose)
* look at all the title+abstract of papers
* have a reference short paragraph that describes the scope 
of papers that interest me (for instance, here I can describe 
the research project for which I did this litterature review)
* compute SOTA sentence embeddings for all the paper title+abstract 
and for the reference paragraph
* export a csv file of the selected papers given a threshold 
on the similarity (to select the threshold, we can for instance 
look at the similarities distribution and keep +/- 2*std).

I created a folder called zotero-similarity-selection/ to do that. 
Please write all the needed code for that. I would like the project 
to be well structured, so please put the different things in some 
separate scripts, and make it easily reusable in similar context 
(argparse to enter the csv file of the exported library, somewhere 
to specify the reference paragraph in a named txt file, and anything 
else you find relevant). I really want something clean to make a nice 
github repository that is actually helpful.
```
