// Main JavaScript for Zotero Similarity Selection Web Interface

let chart = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeUpload();
    initializeForm();
    initializeButtons();
});

// Upload handling
function initializeUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File selected
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

async function handleFile(file) {
    if (!file.name.endsWith('.csv')) {
        showError('Please upload a CSV file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading('Uploading and validating file...');
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        // Update UI
        document.getElementById('file-name-text').textContent = data.filename;
        document.getElementById('paper-count').textContent = `${data.paper_count.toLocaleString()} papers`;
        document.getElementById('file-info').style.display = 'block';
        document.getElementById('upload-area').style.display = 'none';
        
        // Show next section
        document.getElementById('config-section').style.display = 'block';
        document.getElementById('config-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        hideLoading();
        
    } catch (error) {
        hideLoading();
        showError(error.message);
    }
}

// Form handling
function initializeForm() {
    const thresholdMethod = document.getElementById('threshold-method');
    const customThresholdGroup = document.getElementById('custom-threshold-group');
    
    thresholdMethod.addEventListener('change', (e) => {
        if (e.target.value === 'custom') {
            customThresholdGroup.style.display = 'block';
        } else {
            customThresholdGroup.style.display = 'none';
        }
    });
}

// Button handling
function initializeButtons() {
    document.getElementById('process-btn').addEventListener('click', processPapers);
    document.getElementById('download-csv').addEventListener('click', () => downloadFile('csv'));
    document.getElementById('download-bib').addEventListener('click', () => downloadFile('bib'));
    document.getElementById('start-over').addEventListener('click', startOver);
}

async function processPapers() {
    const referenceText = document.getElementById('reference-text').value.trim();
    
    if (!referenceText) {
        showError('Please enter a reference paragraph');
        return;
    }
    
    const thresholdMethod = document.getElementById('threshold-method').value;
    const customThreshold = thresholdMethod === 'custom' 
        ? parseFloat(document.getElementById('custom-threshold').value)
        : null;
    const model = document.getElementById('model-select').value;
    
    // Calculate expected time (0.01 seconds per paper)
    const paperCount = parseInt(document.getElementById('paper-count').textContent.replace(/[^\d]/g, ''));
    const expectedSeconds = Math.ceil(paperCount * 0.01);
    const timeMessage = expectedSeconds < 60 
        ? `${expectedSeconds} seconds`
        : `${Math.ceil(expectedSeconds / 60)} minute${Math.ceil(expectedSeconds / 60) > 1 ? 's' : ''}`;
    
    showLoading(`Processing papers...<br><small>This should take approximately ${timeMessage}</small>`);
    
    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                reference_text: referenceText,
                threshold_method: thresholdMethod,
                custom_threshold: customThreshold,
                model: model
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Processing failed');
        }
        
        // Display results
        displayResults(data);
        
        // Show results section
        document.getElementById('results-section').style.display = 'block';
        document.getElementById('results-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        hideLoading();
        
    } catch (error) {
        hideLoading();
        showError(error.message);
    }
}

function displayResults(data) {
    // Update statistics
    document.getElementById('stat-total').textContent = data.total_count.toLocaleString();
    document.getElementById('stat-selected').textContent = data.selected_count.toLocaleString();
    document.getElementById('stat-percentage').textContent = data.stats.selected_percentage.toFixed(1) + '%';
    document.getElementById('stat-threshold').textContent = data.threshold.toFixed(3);
    
    // Create histogram
    createHistogram(data.similarities, data.threshold);
}

function createHistogram(similarities, threshold) {
    const canvas = document.getElementById('similarity-chart');
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if any
    if (chart) {
        chart.destroy();
    }
    
    // Create histogram bins
    const bins = 50;
    const min = Math.min(...similarities);
    const max = Math.max(...similarities);
    const binWidth = (max - min) / bins;
    
    const histogram = new Array(bins).fill(0);
    const labels = [];
    
    for (let i = 0; i < bins; i++) {
        labels.push((min + i * binWidth).toFixed(2));
    }
    
    similarities.forEach(sim => {
        const binIndex = Math.min(Math.floor((sim - min) / binWidth), bins - 1);
        histogram[binIndex]++;
    });
    
    // Create chart
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Papers',
                data: histogram,
                backgroundColor: function(context) {
                    const value = parseFloat(labels[context.dataIndex]);
                    return value >= threshold ? 'rgba(37, 99, 235, 0.8)' : 'rgba(148, 163, 184, 0.5)';
                },
                borderColor: function(context) {
                    const value = parseFloat(labels[context.dataIndex]);
                    return value >= threshold ? 'rgba(37, 99, 235, 1)' : 'rgba(148, 163, 184, 0.8)';
                },
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            const idx = context[0].dataIndex;
                            const start = parseFloat(labels[idx]);
                            const end = start + binWidth;
                            return `Similarity: ${start.toFixed(2)} - ${end.toFixed(2)}`;
                        },
                        label: function(context) {
                            return `Papers: ${context.parsed.y}`;
                        }
                    }
                },
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            xMin: threshold,
                            xMax: threshold,
                            borderColor: 'rgb(16, 185, 129)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: `Threshold: ${threshold.toFixed(3)}`,
                                position: 'start'
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Similarity Score'
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Number of Papers'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function downloadFile(fileType) {
    window.location.href = `/download/${fileType}`;
}

function startOver() {
    // Reset UI
    document.getElementById('upload-area').style.display = 'block';
    document.getElementById('file-info').style.display = 'none';
    document.getElementById('config-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'none';
    
    // Reset form
    document.getElementById('reference-text').value = '';
    document.getElementById('threshold-method').value = 'mean_2std';
    document.getElementById('custom-threshold-group').style.display = 'none';
    document.getElementById('file-input').value = '';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// UI helpers
function showLoading(message) {
    const overlay = document.getElementById('loading-overlay');
    const text = document.getElementById('loading-text');
    text.innerHTML = message;
    overlay.style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    errorText.textContent = message;
    errorDiv.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// About link
document.getElementById('about-link').addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = '/about';
});
