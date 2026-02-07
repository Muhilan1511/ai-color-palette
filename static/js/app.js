// Global variables
let allEmotions = {};
let currentExtractedColors = [];
let currentExtractedEmotion = '';
let currentExtractedScore = 0;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadAllEmotions();
    setupUploadArea();
    setupEmotionSelect();
    setupQRCodeTab();
});

// Load all emotions
async function loadAllEmotions() {
    try {
        const response = await fetch('/api/emotions');
        allEmotions = await response.json();
        displayAllPalettes();
        populateEmotionSelect();
    } catch (error) {
        console.error('Error loading emotions:', error);
    }
}

// Display all palettes
function displayAllPalettes() {
    const container = document.getElementById('allPalettes');
    container.innerHTML = '';

    Object.entries(allEmotions).forEach(([emotion, colors]) => {
        const card = createPaletteCard(emotion, colors);
        container.appendChild(card);
    });
}

// Create palette card
function createPaletteCard(emotion, colors) {
    const card = document.createElement('div');
    card.className = 'palette-card fade-in';
    
    let colorHtml = '';
    colors.forEach(color => {
        colorHtml += `<div class="color-box" style="background-color: ${color};" title="${color}"></div>`;
    });

    card.innerHTML = `
        <div class="palette-card-title">${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</div>
        <div class="palette-colors">
            ${colorHtml}
        </div>
    `;

    card.addEventListener('click', () => {
        selectEmotion(emotion);
    });

    return card;
}

// Populate emotion select dropdown
function populateEmotionSelect() {
    const select = document.getElementById('emotionSelect');
    select.innerHTML = '<option value="">Choose an emotion...</option>';
    
    Object.keys(allEmotions).forEach(emotion => {
        const option = document.createElement('option');
        option.value = emotion;
        option.textContent = emotion.charAt(0).toUpperCase() + emotion.slice(1);
        select.appendChild(option);
    });
}

// Setup emotion select
function setupEmotionSelect() {
    document.getElementById('emotionSelect').addEventListener('change', (e) => {
        if (e.target.value) {
            selectEmotion(e.target.value);
        }
    });
}

// Select emotion
function selectEmotion(emotion) {
    const colors = allEmotions[emotion];
    const container = document.getElementById('selectedEmotionPalette');
    
    let colorHtml = '';
    colors.forEach(color => {
        colorHtml += `
            <div class="d-flex align-items-center mb-2 p-2 rounded" style="background: #f8f9fa;">
                <div class="color-box" style="background-color: ${color}; width: 60px; height: 60px; margin-right: 1rem;"></div>
                <div>
                    <span style="font-weight: 600; font-size: 0.9rem;">${color}</span>
                </div>
            </div>
        `;
    });

    container.innerHTML = `
        <div class="mt-3">
            <h3>${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</h3>
            ${colorHtml}
            <div class="export-buttons mt-4">
                <button class="btn btn-sm btn-primary me-2" onclick="exportEmotion('${emotion}', 'json')">📥 JSON</button>
                <button class="btn btn-sm btn-secondary me-2" onclick="exportEmotion('${emotion}', 'csv')">📄 CSV</button>
                <button class="btn btn-sm btn-info" onclick="exportEmotion('${emotion}', 'css')">🎨 CSS</button>
            </div>
        </div>
    `;
}

// Setup upload area
function setupUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');

    uploadArea.addEventListener('click', () => imageInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--secondary-color)';
        uploadArea.style.background = 'rgba(45, 106, 79, 0.1)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.background = 'rgba(45, 106, 79, 0.05)';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.background = 'rgba(45, 106, 79, 0.05)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageSelect(files[0]);
        }
    });

    imageInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageSelect(e.target.files[0]);
        }
    });
}

// Handle image selection
function handleImageSelect(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('uploadArea').classList.add('d-none');
        document.getElementById('uploadedImage').classList.remove('d-none');
        document.getElementById('extractedResults').classList.add('d-none');
        
        const preview = document.getElementById('previewImage');
        preview.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

// Extract colors from image
document.addEventListener('DOMContentLoaded', () => {
    const extractBtn = document.getElementById('extractBtn');
    if (extractBtn) {
        extractBtn.addEventListener('click', extractColors);
    }
});

async function extractColors() {
    const imageInput = document.getElementById('imageInput');
    const file = imageInput.files[0];

    if (!file) {
        alert('Please select an image');
        return;
    }

    document.getElementById('loadingSpinner').classList.remove('d-none');
    document.getElementById('extractBtn').disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/extract-palette', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            currentExtractedColors = data.extracted_colors;
            currentExtractedEmotion = data.matched_emotion;
            currentExtractedScore = data.match_score;

            displayExtractedResults(data);
        } else {
            alert('Error: ' + (data.error || 'Failed to extract colors'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error extracting colors');
    } finally {
        document.getElementById('loadingSpinner').classList.add('d-none');
        document.getElementById('extractBtn').disabled = false;
    }
}

// Display extracted results
function displayExtractedResults(data) {
    const resultsDiv = document.getElementById('extractedResults');
    
    // Display extracted colors
    let extractedHtml = '';
    data.extracted_colors.forEach(color => {
        extractedHtml += `
            <div class="d-flex align-items-center mb-2 p-2 rounded" style="background: #f8f9fa;">
                <div class="color-box" style="background-color: ${color}; width: 50px; height: 50px; margin-right: 1rem;"></div>
                <span style="font-weight: 600;">${color}</span>
            </div>
        `;
    });
    document.getElementById('extractedPalette').innerHTML = extractedHtml;

    // Display matched emotion
    const matchPercent = (data.match_score * 100).toFixed(2);
    document.getElementById('matchedEmotion').innerHTML = 
        `<strong>${data.matched_emotion.toUpperCase()}</strong> (${matchPercent}% match)`;

    // Display matched palette
    let matchedHtml = '';
    data.matched_palette.forEach(color => {
        matchedHtml += `
            <div class="d-flex align-items-center mb-2 p-2 rounded" style="background: #f8f9fa;">
                <div class="color-box" style="background-color: ${color}; width: 50px; height: 50px; margin-right: 1rem;"></div>
                <span>${color}</span>
            </div>
        `;
    });
    document.getElementById('matchedPalette').innerHTML = matchedHtml;

    resultsDiv.classList.remove('d-none');
}

// Export functions
async function exportAll(format) {
    let colors = [];
    for (let emotion of Object.values(allEmotions)) {
        colors.push(...emotion);
    }
    
    await exportData(colors, 'all_palettes', format);
}

async function exportEmotion(emotion, format) {
    const colors = allEmotions[emotion];
    await exportData(colors, emotion, format);
}

async function exportExtracted(format) {
    await exportData(currentExtractedColors, 'extracted_palette', format);
}

async function exportData(colors, filename, format) {
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                colors: colors,
                format: format,
                emotion: filename
            })
        });

        const data = await response.json();
        
        // Create download
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data.content));
        element.setAttribute('download', data.filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    } catch (error) {
        console.error('Export error:', error);
        alert('Error exporting file');
    }
}

// Setup QR Code Tab
function setupQRCodeTab() {
    const qrcodeTab = document.getElementById('qrcode-tab');
    if (qrcodeTab) {
        qrcodeTab.addEventListener('click', loadQRCode);
    }
}

// Load QR Code
async function loadQRCode() {
    const container = document.getElementById('qrcodeContainer');
    
    try {
        const response = await fetch('/api/qrcode');
        const data = await response.json();
        
        if (data.success) {
            container.innerHTML = `
                <div class="qrcode-display">
                    <img src="${data.qrcode}" alt="QR Code" class="qrcode-img">
                    <p class="mt-3"><strong>Access URL:</strong></p>
                    <p class="qrcode-url">${data.url}</p>
                    <button class="btn btn-primary mt-3" onclick="copyToClipboard('${data.url}')">📋 Copy URL</button>
                </div>
            `;
        } else {
            container.innerHTML = '<p class="text-danger">Error generating QR code</p>';
        }
    } catch (error) {
        console.error('QR code error:', error);
        container.innerHTML = '<p class="text-danger">Error loading QR code</p>';
    }
}

// Copy to Clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('URL copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}
