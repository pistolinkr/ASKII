#!/usr/bin/env python3
"""
ASCII Art Web Application
Web-based ASCII art generator and image converter
"""

from flask import Flask, render_template, request, jsonify
import os
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from ascii_art import AsciiArtRenderer
from ascii_converter import AsciiConverter
from ascii_3d import ASCII3DRenderer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize converters
renderer = AsciiArtRenderer()
converter = AsciiConverter(width=100)
renderer_3d = ASCII3DRenderer()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/generate-art', methods=['POST'])
def generate_art():
    """Generate ASCII art"""
    try:
        data = request.json
        art_type = data.get('type', 'banner')
        text = data.get('text', 'ASCII ART')
        size = data.get('size', 15)
        
        if art_type == 'banner':
            result = renderer.text_banner(text)
        elif art_type == 'wave':
            result = renderer.wave(size)
        elif art_type == 'circle':
            result = renderer.circle(size)
        elif art_type == 'spiral':
            result = renderer.spiral(size)
        elif art_type == 'heart':
            result = renderer.heart(size)
        elif art_type == 'box_text':
            result = renderer.box_text(text, size * 2)
        else:
            result = "Unknown art type"
        
        return jsonify({'success': True, 'ascii': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/convert-image', methods=['POST'])
def convert_image():
    """Convert image to ASCII"""
    try:
        data = request.json
        image_data = data.get('image')
        width = data.get('width', 100)
        detailed = data.get('detailed', False)
        invert = data.get('invert', False)
        
        # Decode base64 image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to grayscale
        image = image.convert('L')
        
        # Resize with aspect ratio
        aspect_ratio = image.height / image.width
        new_height = int(width * aspect_ratio * 0.55)
        image = image.resize((width, new_height))
        
        # Convert to ASCII
        conv = AsciiConverter(width=width, detailed=detailed, invert=invert)
        ascii_art = conv._pixels_to_ascii(np.array(image))
        
        return jsonify({'success': True, 'ascii': ascii_art})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/generate-3d', methods=['POST'])
def generate_3d():
    """Generate 3D ASCII object"""
    try:
        data = request.json
        obj_type = data.get('type', 'cube')
        size = data.get('size', 10)
        
        if obj_type == 'cube':
            result = renderer_3d.render_cube(size)
        elif obj_type == 'sphere':
            result = renderer_3d.render_sphere(size)
        elif obj_type == 'pyramid':
            result = renderer_3d.render_pyramid(size)
        elif obj_type == 'torus':
            result = renderer_3d.render_torus(size, size // 2)
        else:
            result = "Unknown object type"
        
        return jsonify({'success': True, 'ascii': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

