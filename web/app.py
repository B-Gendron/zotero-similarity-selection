#!/usr/bin/env python3
"""
Web interface for Zotero Similarity Selection.

This provides a user-friendly web UI while keeping the CLI functionality intact.
Run with: python web/app.py
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, session, Response
import json
from werkzeug.utils import secure_filename
import tempfile
import uuid

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import (
    EmbeddingComputer,
    combine_title_abstract,
    PaperSelector,
    load_zotero_csv,
    extract_title_abstract_columns,
    save_selected_papers,
    validate_dataframe,
)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
        file.save(filepath)
        
        # Load and validate CSV
        df = load_zotero_csv(filepath)
        title_col, abstract_col = extract_title_abstract_columns(df)
        validate_dataframe(df, title_col, abstract_col)
        
        # Store info in session
        session['csv_path'] = filepath
        session['csv_filename'] = filename
        session['paper_count'] = len(df)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'paper_count': len(df),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/process', methods=['POST'])
def process_papers():
    """Process papers with the given reference text and threshold."""
    try:
        data = request.json
        reference_text = data.get('reference_text', '').strip()
        threshold_method = data.get('threshold_method', 'mean_2std')
        custom_threshold = data.get('custom_threshold', None)
        model_name = data.get('model', 'sentence-transformers/all-mpnet-base-v2')
        
        if not reference_text:
            return jsonify({'error': 'Reference text is required'}), 400
        
        if 'csv_path' not in session:
            return jsonify({'error': 'No CSV file uploaded'}), 400
        
        csv_path = session['csv_path']
        session_id = session['session_id']
        
        # Load data
        df = load_zotero_csv(csv_path)
        title_col, abstract_col = extract_title_abstract_columns(df)
        
        # Combine titles and abstracts
        paper_texts = [
            combine_title_abstract(row[title_col], row[abstract_col])
            for _, row in df.iterrows()
        ]
        
        # Initialize embedder
        embedder = EmbeddingComputer(model_name=model_name)
        
        # Encode reference
        reference_embedding = embedder.encode_single(reference_text)
        
        # Encode papers
        paper_embeddings = embedder.encode_texts(
            paper_texts,
            show_progress=False,
            batch_size=32
        )
        
        # Compute similarities
        selector = PaperSelector()
        similarities = selector.compute_similarities(paper_embeddings, reference_embedding)
        
        # Determine threshold
        if custom_threshold is not None:
            threshold = selector.compute_threshold(method="custom", custom_threshold=custom_threshold)
        else:
            threshold = selector.compute_threshold(method=threshold_method)
        
        # Select papers
        selected = selector.select_papers(threshold)
        
        # Get statistics
        stats = selector.get_statistics()
        
        # Save selected papers
        output_csv = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_selected.csv")
        output_bib = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_selected.bib")
        
        save_selected_papers(df, output_csv, similarities, selected)
        
        # Store paths in session
        session['output_csv'] = output_csv
        session['output_bib'] = output_bib
        
        # Get similarity distribution for visualization
        similarity_list = similarities.tolist()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'similarities': similarity_list,
            'threshold': float(threshold),
            'selected_count': int(selected.sum()),
            'total_count': len(df)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/download/<file_type>')
def download_file(file_type):
    """Download the selected papers in CSV or BibTeX format."""
    try:
        if 'output_csv' not in session:
            return jsonify({'error': 'No output file available'}), 400
            
        csv_path = session['output_csv']
        
        if file_type == 'csv':
            filepath = csv_path
            mimetype = 'text/csv'
            filename = 'selected_papers.csv'
            
        elif file_type == 'bib':
            # Always convert CSV to BibTeX on-the-fly
            bib_path = session['output_bib']
            
            # Import the conversion functions
            parent_dir = Path(__file__).parent.parent
            sys.path.insert(0, str(parent_dir))
            
            try:
                import csv2bibtex as c2b
                c2b.csv_to_bibtex(csv_path, bib_path)
            except Exception as e:
                return jsonify({'error': f'BibTeX conversion failed: {str(e)}'}), 500
            
            filepath = bib_path
            mimetype = 'application/x-bibtex'
            filename = 'selected_papers.bib'
            
        else:
            return jsonify({'error': 'Invalid file type'}), 400
        
        return send_file(
            filepath,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

@app.route('/about')
def about():
    """Render the about page with README content."""
    try:
        import markdown
        
        # Read the main README file
        readme_path = Path(__file__).parent.parent / 'README.md'
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_text = f.read()
        
        # Convert markdown to HTML with extra extensions
        readme_html = markdown.markdown(
            readme_text,
            extensions=['fenced_code', 'tables', 'nl2br', 'toc', 'attr_list']
        )
        
        return render_template('about.html', readme_html=readme_html)
        
    except Exception as e:
        return render_template('about.html', readme_html=f"<p>Error loading README: {str(e)}</p>")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("ZOTERO SIMILARITY SELECTION - WEB INTERFACE")
    print("="*70)
    print("\nStarting web server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
