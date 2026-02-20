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

This tool helps researchers efficiently filter thousands of papers from a .csv file (e.g., exported from Zotero) by computing semantic similarity between paper titles/abstracts and a reference description of the research scope. The selected papers are exported as a .csv file and can be converted to BibTeX for import into Zotero.

You can use the tool either in its [web](#quick-start-web-version) or [terminal](#quick-start-terminal-version) version.

## Features

- Computes semantic similarity between title/abstract of papers and a reference text using Sentence-BERT encoding (Reimers & Gurevych, 2019) and the `sentence-transformers` library (see [Models](#models) Section)
- Analyzes similarity score distributions to derive data-driven similarity thresholds (both automatic threshold estimation and manual threshold specification)
- Provides visualizations to facilitate interpretation of similarity scores and the choice of an appropriate thresholding strategy
- Converts `.csv` output files to `.bib` to support Zotero import (import of `.csv` files directly is currently not possible in Zotero)

## Installation

Clone this repository and install dependencies:
```bash
git clone https://github.com/B-Gendron/zotero-similarity-selection.git
cd zotero-similarity-selection
pip install -r requirements.txt
```

## Quick Start (Web Version)

1. Export your Zotero library to CSV format (File → Export Library → CSV)

2. Run the web application:
```bash
python web/app.py
```

3. Open in browser

The default URL is `http://localhost:5000`, which means it will fail if port 5000 is already used on your computer. In this case, run the app again while specifying another port:
```bash
python web/app.py --port 5001
```

Once in the app, you simply have to drag and drop the .csv export of your Zotero library, write a reference description and specify your options to compute similarities. You can export the result in .csv or .bib format. 

## Quick Start (Terminal Version)

1. Export your Zotero library to CSV format (File → Export Library → CSV)

2. Write your reference description in the dedicated file:
```bash
nano config/reference.txt
```

3. Compute similarities and export the result in a .csv file:
```bash
python main.py --input data/zotero_library.csv --output data/selected_papers.csv
```

4. (Optional) Convert exported .csv to .bib

This step is necessary if you want to re-import to Zotero, since it doesn't support CSV import. Convert your .csv output file to a .bib file with:
```bash
python csv_to_bibtex.py -i data/selected_papers.csv -o data/selected_papers.bib
```

## Usage (Terminal Version)

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
├── main.py                 # Run the app (terminal version)
├── examples.py
├── csv2bibtex.py           # Convert .csv file to .bib
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
├── web/
│   ├── app.py              # Run the app (web version)
│   ├── templates/
│   │   ├── index.html      # Main UI template
│   │   └── about.html
│   └── static/
│       ├── css/
│       │   ├── style.css
│       │   └── about.css
│       └── js/
│           └── app.js
├── requirements.txt
├── .gitignore
└── README.md
```
## Similarity Threshold Selection

By default, the tool uses **mean + 2×std** as the threshold, which typically captures papers that are significantly more similar to your reference than average. You can:

- Let the tool auto-compute the threshold (recommended for first run)
- Specify a custom threshold with `--threshold`
- Use `--visualize` to see the distribution and then adjust your threshold accordingly

## CSV Format Requirements

The input CSV should contain at least `Title` and `Abstract` columns (that are always present in a standard Zotero export). Other columns will be preserved in the output.

## Re-importing to Zotero

Once you have your output in a .bib format, you can import it to Zotero via the following steps:
1. Go to File → Import...
2. Select the `.bib` file
3. Choose import options
4. Click Continue

## Models

The sentence transformer models used in this app are the following:
- `sentence-transformers/all-mpnet-base-v2` (default): Best quality, slower
- `sentence-transformers/all-MiniLM-L6-v2`: Fast, good quality

See [Sentence Transformers documentation](https://www.sbert.net/docs/pretrained_models.html) for more options.

## AI Assistance Details

### Model

Claude Sonnet 4.5

### Prompt for Creating the App

```
I want to select relevant papers from a zotero library with thousands of papers from an automatic extraction. The idea is the following:
* export all the library (in a csv format, I suppose)
* look at all the title+abstract of papers
* have a reference short paragraph that describes the scope of papers that interest me (for instance, here I can describe the research project for which I did this litterature review)
* compute SOTA sentence embeddings for all the paper title+abstract and for the reference paragraph
* export a csv file of the selected papers given a threshold on the similarity (to select the threshold, we can for instance look at the similarities distribution and keep +/- 2*std).

I created a folder called zotero-similarity-selection/ to do that. Please write all the needed code for that. I would like the project to be well structured, so please put the different things in some separate scripts, and make it easily reusable in similar context (argparse to enter the csv file of the exported library, somewhere to specify the reference paragraph in a named txt file, and anything else you find relevant). I really want something clean to make a nice github repository that is actually helpful.
```
### Prompt for Developing the Web Version

```
I would like to create a simple, modern and minimalistic web interface for this app. As much as possible, put all the web utils in separated folders so the the app is still runnable from the terminal without issue.
```