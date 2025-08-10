from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from PIL import Image
import io
import base64
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/convert-image', methods=['POST'])
def convert_image():
    try:
        data = request.json
        image_data = data.get('image')
        width = data.get('width', 80)
        style = data.get('style', 'standard')
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert image to ASCII using OpenAI
        prompt = f"""Convert this image to ASCII art with width {width} characters. Style: {style}.
        Make it look artistic and detailed. Return only the ASCII art, no explanations."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ASCII artist. Convert images to beautiful ASCII art."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        ascii_art = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'ascii_art': ascii_art
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-text-art', methods=['POST'])
def generate_text_art():
    try:
        data = request.json
        text = data.get('text', '')
        style = data.get('style', 'block')
        
        prompt = f"""Create ASCII art for the text "{text}" in {style} style. 
        Make it large, artistic, and visually appealing. Return only the ASCII art."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ASCII artist specializing in text-to-ASCII conversion."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500,
            temperature=0.8
        )
        
        ascii_art = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'ascii_art': ascii_art
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-pattern', methods=['POST'])
def generate_pattern():
    try:
        data = request.json
        pattern_type = data.get('patternType', 'random')
        size = data.get('size', 20)
        
        prompt = f"""Generate a {pattern_type} ASCII pattern with size {size}x{size}. 
        Make it visually interesting and artistic. Return only the ASCII pattern."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at creating ASCII patterns and designs."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000,
            temperature=0.9
        )
        
        pattern = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'pattern': pattern
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze-ascii', methods=['POST'])
def analyze_ascii():
    try:
        data = request.json
        ascii_text = data.get('asciiText', '')
        
        prompt = f"""Analyze this ASCII art and provide detailed insights:
        
        {ascii_text}
        
        Please analyze:
        1. Visual complexity and artistic merit
        2. Character density and distribution
        3. Overall aesthetic appeal
        4. Technical characteristics
        
        Provide a comprehensive analysis."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ASCII art analyst and critic."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        analysis = response.choices[0].message.content
        
        # Calculate basic stats
        total_chars = len(ascii_text)
        unique_chars = len(set(ascii_text))
        lines = ascii_text.count('\n') + 1
        
        stats = {
            'total_characters': total_chars,
            'unique_characters': unique_chars,
            'lines': lines,
            'character_diversity': round(unique_chars / total_chars * 100, 2) if total_chars > 0 else 0
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
