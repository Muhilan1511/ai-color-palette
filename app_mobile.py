from flask import Flask, render_template, request, jsonify, send_file
import json
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename
from emotion_data import emotion_colors
from image_palette import extract_colors_from_image, match_emotion_to_palette
import io
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/emotions')
def get_emotions():
    """Get all emotions and their colors"""
    return jsonify(emotion_colors)

@app.route('/api/emotion/<emotion_name>')
def get_emotion(emotion_name):
    """Get specific emotion palette"""
    if emotion_name.lower() in emotion_colors:
        return jsonify({
            'emotion': emotion_name,
            'colors': emotion_colors[emotion_name.lower()]
        })
    return jsonify({'error': 'Emotion not found'}), 404

@app.route('/api/extract-palette', methods=['POST'])
def extract_palette():
    """Extract colors from uploaded image"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use PNG or JPG'}), 400
    
    try:
        # Read and save image
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract colors
        extracted_colors = extract_colors_from_image(filepath, num_colors=5)
        
        if not extracted_colors:
            return jsonify({'error': 'Failed to extract colors'}), 400
        
        # Match to emotion
        matched_emotion, score = match_emotion_to_palette(extracted_colors, emotion_colors)
        matched_palette = emotion_colors.get(matched_emotion, [])
        
        return jsonify({
            'success': True,
            'extracted_colors': extracted_colors,
            'matched_emotion': matched_emotion,
            'match_score': float(score),
            'matched_palette': matched_palette
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/api/export', methods=['POST'])
def export_data():
    """Export palette data in various formats"""
    data = request.json
    format_type = data.get('format', 'json')
    colors = data.get('colors', [])
    emotion = data.get('emotion', 'palette')
    
    if format_type == 'json':
        content = json.dumps({'emotion': emotion, 'colors': colors}, indent=2)
        filename = f"{emotion}.json"
        mime = 'application/json'
    
    elif format_type == 'csv':
        lines = ['Color']
        lines.extend(colors)
        content = '\n'.join(lines)
        filename = f"{emotion}.csv"
        mime = 'text/csv'
    
    elif format_type == 'css':
        content = ':root {\n'
        for i, color in enumerate(colors, 1):
            content += f'  --color-{i}: {color};\n'
        content += '}'
        filename = f"{emotion}.css"
        mime = 'text/css'
    
    else:
        content = f"{emotion.upper()}\n{'='*30}\n\n"
        for i, color in enumerate(colors, 1):
            content += f"Color {i}: {color}\n"
        filename = f"{emotion}.txt"
        mime = 'text/plain'
    
    return jsonify({
        'content': content,
        'filename': filename,
        'mime': mime
    })

@app.route('/api/qrcode')
def generate_qrcode():
    """Generate QR code for the app URL"""
    try:
        # Get the host from request headers
        host = request.host
        url = f"http://{host}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'qrcode': f'data:image/png;base64,{img_str}',
            'url': url
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
