# Zotero Similarity Selection

A tool for filtering and selecting relevant papers from large Zotero libraries using state-of-the-art sentence embeddings and semantic similarity. This tool has been developed with the assistance of Claude (more details in AI Assistance Details section).

## Overview

This tool helps researchers efficiently filter thousands of papers exported from Zotero by computing semantic similarity between paper titles/abstracts and a reference description of your research scope.

## Features

- 🔍 **Semantic Similarity**: Uses state-of-the-art sentence embeddings (Sentence-BERT)
- 📊 **Statistical Thresholding**: Automatically suggests similarity thresholds based on distribution statistics
- 🎯 **Flexible Filtering**: Customize similarity thresholds or use automatic recommendations
- 📁 **Clean Structure**: Modular, reusable code ready for different projects
- 📈 **Visualization**: Generate distribution plots to understand your data

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/zotero-similarity-selection.git
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
# Edit config/reference.txt with your research description
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
4. **Calculate Similarity**: Computes cosine similarity between each paper and the reference
5. **Filter Papers**: Selects papers above the similarity threshold
6. **Export Results**: Saves selected papers to a new CSV file

## Similarity Threshold Selection

By default, the tool uses **mean + 2×std** as the threshold, which typically captures papers that are significantly more similar to your reference than average. You can:

- Let the tool auto-compute the threshold (recommended for first run)
- Specify a custom threshold with `--threshold`
- Use `--visualize` to see the distribution and adjust accordingly

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