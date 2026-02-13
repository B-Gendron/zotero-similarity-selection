# Web Interface

This folder provide all the material to run the web version of ZSS. Regarding the offered features, you can equally use terminal or web version of the app: they share the same core functionality. However, if you are not at ease with using terminal command and/or wish to use a pretty interface to run the code, you may enjoy to use the web version. 😁

## Quick Start

1. **Install dependencies** (including Flask):
```bash
pip install -r requirements.txt
```

2. **Start the web server**:
```bash
python web/app.py
```

3. **Open your browser**:
The URL would typically look like: `http://localhost:5000`, except if port 5000 is already used, in this case you would specify another port for the app:
```bash
python web/app.py --port 5001 # Use a different port (unused)
```

## Features

- 📤 **Drag & Drop Upload**: Easy CSV file upload
- ⚙️ **Interactive Configuration**: Set reference text and threshold options
- 📊 **Live Visualization**: See similarity distribution with interactive chart
- 📥 **Instant Download**: Get results in CSV or BibTeX format
- 🎨 **Modern UI**: Clean, minimalistic design
- 📱 **Responsive**: Works on desktop, tablet, and mobile

## Usage

### Step 1: Upload CSV
- Drag and drop your Zotero CSV export
- Or click to browse and select file

### Step 2: Configure
- **Reference Paragraph**: Describe your research scope
- **Threshold Method**: Choose how to filter papers
  - Auto (Mean + 2×SD) - Recommended
  - Lenient (Mean + 1×SD)
  - Top 10%, 25%, 50%
  - Custom threshold
- **Model**: Select embedding model
  - Best Quality (MPNet) - Slower, better results
  - Faster (MiniLM) - Faster, good results

### Step 3: Results
- View statistics and similarity distribution
- Download selected papers in CSV or BibTeX format
- Import BibTeX file directly into Zotero

## Architecture

```
web/
├── app.py                  # Flask application
├── templates/
│   ├── index.html          # Main UI template
│   └── about.html
└── static/
    ├── css/
    │   ├── style.css
    │   └── about.css      
    └── js/
        └── app.js 
```

## Terminal vs Web

You can equally use terminal or web version of the app: they share the same core functionality.


### TODO

- Fix the links in the About section
