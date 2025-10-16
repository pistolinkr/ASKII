#!/usr/bin/env python3
"""
ASCII Art Web Application
Web-based ASCII art generator and image converter
"""

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/generate-art', methods=['POST'])
def generate_art():
    """Generate ASCII art (client-side processing)"""
    try:
        # ASCII art generation is now handled entirely on the client side
        return jsonify({'success': True, 'message': 'Client-side processing enabled'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/convert-image', methods=['POST'])
def convert_image():
    """Convert image to ASCII (client-side processing)"""
    try:
        # Image conversion is now handled entirely on the client side
        # This endpoint is kept for compatibility but doesn't do server-side processing
        return jsonify({'success': True, 'message': 'Client-side processing enabled'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/generate-3d', methods=['POST'])
def generate_3d():
    """Generate 3D ASCII object (client-side processing)"""
    try:
        # 3D ASCII generation is now handled entirely on the client side
        return jsonify({'success': True, 'message': 'Client-side processing enabled'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5001)

