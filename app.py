from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import re
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ASCII character sets for different styles
ASCII_CHARS = {
    'standard': ' .:-=+*#%@',
    'detailed': ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$',
    'blocks': ' █▇▆▅▄▃▂▁',
    'minimal': ' .:;+=xX$&'
}

class ASCIIAI:
    def __init__(self):
        self.ascii_chars = ASCII_CHARS['standard']
    
    def image_to_ascii(self, image_data, width=100, style='standard'):
        """Convert image to ASCII art"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to grayscale
            gray_image = image.convert('L')
            
            # Resize image
            aspect_ratio = gray_image.height / gray_image.width
            height = int(width * aspect_ratio * 0.5)  # Adjust for character aspect ratio
            resized_image = gray_image.resize((width, height))
            
            # Convert pixels to ASCII
            pixels = np.array(resized_image)
            ascii_chars = ASCII_CHARS.get(style, ASCII_CHARS['standard'])
            
            ascii_art = []
            for row in pixels:
                line = ''.join([ascii_chars[pixel * len(ascii_chars) // 256] for pixel in row])
                ascii_art.append(line)
            
            return '\n'.join(ascii_art)
        except Exception as e:
            return f"Error converting image: {str(e)}"
    
    def text_to_ascii_art(self, text, style='block'):
        """Convert text to ASCII art"""
        if style == 'block':
            return self._create_block_text(text)
        elif style == 'banner':
            return self._create_banner_text(text)
        else:
            return self._create_simple_text(text)
    
    def _create_block_text(self, text):
        """Create block-style ASCII text"""
        blocks = {
            'A': [' ████ ', '██  ██', '██  ██', '██████', '██  ██'],
            'B': ['█████ ', '██  ██', '█████ ', '██  ██', '█████ '],
            'C': [' ████ ', '██   █', '██    ', '██   █', ' ████ '],
            'D': ['█████ ', '██  ██', '██  ██', '██  ██', '█████ '],
            'E': ['██████', '██    ', '█████ ', '██    ', '██████'],
            'F': ['██████', '██    ', '█████ ', '██    ', '██    '],
            'G': [' ████ ', '██   █', '██ ███', '██   █', ' ████ '],
            'H': ['██  ██', '██  ██', '██████', '██  ██', '██  ██'],
            'I': ['██████', '  ██  ', '  ██  ', '  ██  ', '██████'],
            'J': ['██████', '   ██ ', '   ██ ', '██ ██ ', ' ████ '],
            'K': ['██  ██', '██ ██ ', '████  ', '██ ██ ', '██  ██'],
            'L': ['██    ', '██    ', '██    ', '██    ', '██████'],
            'M': ['██  ██', '███████', '██ █ ██', '██   ██', '██   ██'],
            'N': ['██   ██', '████  ██', '██ ██ ██', '██  ████', '██   ██'],
            'O': [' ████ ', '██  ██', '██  ██', '██  ██', ' ████ '],
            'P': ['█████ ', '██  ██', '█████ ', '██    ', '██    '],
            'Q': [' ████ ', '██  ██', '██  ██', '██ ███', ' █████'],
            'R': ['█████ ', '██  ██', '█████ ', '██ ██ ', '██  ██'],
            'S': [' ████ ', '██   █', ' ████ ', '    ██', ' ████ '],
            'T': ['██████', '  ██  ', '  ██  ', '  ██  ', '  ██  '],
            'U': ['██  ██', '██  ██', '██  ██', '██  ██', ' ████ '],
            'V': ['██  ██', '██  ██', '██  ██', ' ██ ██ ', '  ██  '],
            'W': ['██   ██', '██   ██', '██ █ ██', '███████', '██  ██'],
            'X': ['██  ██', ' ██ ██ ', '  ██  ', ' ██ ██ ', '██  ██'],
            'Y': ['██  ██', ' ██ ██ ', '  ██  ', '  ██  ', '  ██  '],
            'Z': ['██████', '    ██', '  ██  ', '██    ', '██████']
        }
        
        result = []
        for i in range(5):
            line = ''
            for char in text.upper():
                if char in blocks:
                    line += blocks[char][i] + ' '
                else:
                    line += '      '
            result.append(line)
        
        return '\n'.join(result)
    
    def _create_banner_text(self, text):
        """Create banner-style ASCII text"""
        banner = f"""
╔{'═' * (len(text) + 2)}╗
║ {text} ║
╚{'═' * (len(text) + 2)}╝
"""
        return banner
    
    def _create_simple_text(self, text):
        """Create simple ASCII text"""
        return f"""
┌{'─' * (len(text) + 2)}┐
│ {text} │
└{'─' * (len(text) + 2)}┘
"""
    
    def generate_ascii_pattern(self, pattern_type='random', size=20):
        """Generate ASCII patterns"""
        if pattern_type == 'random':
            return self._generate_random_pattern(size)
        elif pattern_type == 'geometric':
            return self._generate_geometric_pattern(size)
        elif pattern_type == 'fractal':
            return self._generate_fractal_pattern(size)
        else:
            return self._generate_random_pattern(size)
    
    def _generate_random_pattern(self, size):
        """Generate random ASCII pattern"""
        chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        pattern = []
        for _ in range(size):
            line = ''.join(random.choice(chars) for _ in range(size))
            pattern.append(line)
        return '\n'.join(pattern)
    
    def _generate_geometric_pattern(self, size):
        """Generate geometric ASCII pattern"""
        pattern = []
        for i in range(size):
            line = ''
            for j in range(size):
                if i == j or i == size - 1 - j or i == size // 2 or j == size // 2:
                    line += '#'
                elif i < size // 2 and j < size // 2:
                    line += '/'
                elif i < size // 2 and j >= size // 2:
                    line += '\\'
                elif i >= size // 2 and j < size // 2:
                    line += '\\'
                else:
                    line += '/'
            pattern.append(line)
        return '\n'.join(pattern)
    
    def _generate_fractal_pattern(self, size):
        """Generate fractal-like ASCII pattern"""
        pattern = []
        for i in range(size):
            line = ''
            for j in range(size):
                x = (i - size // 2) / (size // 2)
                y = (j - size // 2) / (size // 2)
                if abs(x) < 0.1 or abs(y) < 0.1:
                    line += '#'
                elif abs(x + y) < 0.2 or abs(x - y) < 0.2:
                    line += '*'
                elif x*x + y*y < 0.5:
                    line += '+'
                else:
                    line += '.'
            pattern.append(line)
        return '\n'.join(pattern)
    
    def analyze_ascii_complexity(self, ascii_text):
        """Analyze complexity of ASCII text"""
        lines = ascii_text.split('\n')
        total_chars = sum(len(line) for line in lines)
        unique_chars = len(set(''.join(lines)))
        density = sum(1 for line in lines for char in line if char != ' ') / total_chars if total_chars > 0 else 0
        
        return {
            'total_lines': len(lines),
            'total_characters': total_chars,
            'unique_characters': unique_chars,
            'density': round(density, 3),
            'complexity_score': round((unique_chars / 10) * density * (len(lines) / 20), 3)
        }

# Initialize ASCII AI
ascii_ai = ASCIIAI()

@app.route('/')
def index():
    """Main page with HTML interface"""
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASCII AI - 아스키로 생각하는 AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace; 
            background: #1a1a1a; 
            color: #00ff00; 
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { font-size: 3em; margin-bottom: 10px; text-shadow: 0 0 10px #00ff00; }
        .header p { font-size: 1.2em; opacity: 0.8; }
        
        .section { 
            background: #2a2a2a; 
            border: 1px solid #00ff00; 
            border-radius: 10px; 
            padding: 20px; 
            margin-bottom: 30px;
            box-shadow: 0 0 20px rgba(0,255,0,0.3);
        }
        .section h2 { 
            color: #00ff00; 
            margin-bottom: 20px; 
            border-bottom: 2px solid #00ff00;
            padding-bottom: 10px;
        }
        
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .input-group input, .input-group select, .input-group textarea { 
            width: 100%; 
            padding: 10px; 
            background: #1a1a1a; 
            border: 1px solid #00ff00; 
            color: #00ff00; 
            border-radius: 5px;
            font-family: inherit;
        }
        .input-group textarea { height: 100px; resize: vertical; }
        
        .btn { 
            background: #00ff00; 
            color: #000; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: bold;
            transition: all 0.3s;
        }
        .btn:hover { background: #00cc00; transform: translateY(-2px); }
        
        .result { 
            background: #1a1a1a; 
            border: 1px solid #00ff00; 
            border-radius: 5px; 
            padding: 20px; 
            margin-top: 20px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.2;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .file-input { display: none; }
        .file-label { 
            display: inline-block; 
            padding: 10px 20px; 
            background: #333; 
            border: 1px solid #00ff00; 
            border-radius: 5px; 
            cursor: pointer;
            margin-right: 10px;
        }
        .file-label:hover { background: #444; }
        
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
            gap: 15px; 
            margin-top: 20px;
        }
        .stat { 
            background: #333; 
            padding: 15px; 
            border-radius: 5px; 
            text-align: center;
        }
        .stat-value { font-size: 1.5em; font-weight: bold; color: #00ff00; }
        .stat-label { font-size: 0.9em; opacity: 0.8; }
        
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ASCII AI</h1>
            <p>아스키로 생각하는 AI - Think in ASCII</p>
        </div>
        
        <div class="grid">
            <div class="section">
                <h2>🖼️ Image to ASCII</h2>
                <div class="input-group">
                    <label>Upload Image:</label>
                    <input type="file" id="imageInput" accept="image/*" class="file-input">
                    <label for="imageInput" class="file-label">Choose File</label>
                </div>
                <div class="input-group">
                    <label>Width (characters):</label>
                    <input type="number" id="width" value="80" min="20" max="200">
                </div>
                <div class="input-group">
                    <label>Style:</label>
                    <select id="style">
                        <option value="standard">Standard</option>
                        <option value="detailed">Detailed</option>
                        <option value="blocks">Blocks</option>
                        <option value="minimal">Minimal</option>
                    </select>
                </div>
                <button class="btn" onclick="convertImage()">Convert to ASCII</button>
                <div id="imageResult" class="result" style="display: none;"></div>
            </div>
            
            <div class="section">
                <h2>📝 Text to ASCII Art</h2>
                <div class="input-group">
                    <label>Text:</label>
                    <input type="text" id="textInput" placeholder="Enter text..." value="ASCII AI">
                </div>
                <div class="input-group">
                    <label>Style:</label>
                    <select id="textStyle">
                        <option value="block">Block</option>
                        <option value="banner">Banner</option>
                        <option value="simple">Simple</option>
                    </select>
                </div>
                <button class="btn" onclick="convertText()">Convert to ASCII Art</button>
                <div id="textResult" class="result" style="display: none;"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎨 ASCII Pattern Generator</h2>
            <div class="input-group">
                <label>Pattern Type:</label>
                <select id="patternType">
                    <option value="random">Random</option>
                    <option value="geometric">Geometric</option>
                    <option value="fractal">Fractal</option>
                </select>
            </div>
            <div class="input-group">
                <label>Size:</label>
                <input type="number" id="patternSize" value="20" min="10" max="50">
            </div>
            <button class="btn" onclick="generatePattern()">Generate Pattern</button>
            <div id="patternResult" class="result" style="display: none;"></div>
        </div>
        
        <div class="section">
            <h2>🔍 ASCII Analysis</h2>
            <div class="input-group">
                <label>ASCII Text to Analyze:</label>
                <textarea id="analyzeInput" placeholder="Paste ASCII text here..."></textarea>
            </div>
            <button class="btn" onclick="analyzeAscii()">Analyze</button>
            <div id="analysisResult" class="result" style="display: none;"></div>
            <div id="analysisStats" class="stats" style="display: none;"></div>
        </div>
    </div>

    <script>
        async function convertImage() {
            const file = document.getElementById('imageInput').files[0];
            if (!file) {
                alert('Please select an image file');
                return;
            }
            
            const reader = new FileReader();
            reader.onload = async function(e) {
                const imageData = e.target.result;
                const width = document.getElementById('width').value;
                const style = document.getElementById('style').value;
                
                try {
                    const response = await fetch('/api/image-to-ascii', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({image: imageData, width: parseInt(width), style: style})
                    });
                    
                    const result = await response.json();
                    if (result.success) {
                        document.getElementById('imageResult').textContent = result.ascii;
                        document.getElementById('imageResult').style.display = 'block';
                    } else {
                        alert('Error: ' + result.error);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            };
            reader.readAsDataURL(file);
        }
        
        async function convertText() {
            const text = document.getElementById('textInput').value;
            const style = document.getElementById('textStyle').value;
            
            try {
                const response = await fetch('/api/text-to-ascii', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text, style: style})
                });
                
                const result = await response.json();
                if (result.success) {
                    document.getElementById('textResult').textContent = result.ascii;
                    document.getElementById('textResult').style.display = 'block';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
        
        async function generatePattern() {
            const type = document.getElementById('patternType').value;
            const size = parseInt(document.getElementById('patternSize').value);
            
            try {
                const response = await fetch('/api/generate-pattern', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({type: type, size: size})
                });
                
                const result = await response.json();
                if (result.success) {
                    document.getElementById('patternResult').textContent = result.pattern;
                    document.getElementById('patternResult').style.display = 'block';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
        
        async function analyzeAscii() {
            const text = document.getElementById('analyzeInput').value;
            if (!text.trim()) {
                alert('Please enter some ASCII text to analyze');
                return;
            }
            
            try {
                const response = await fetch('/api/analyze-ascii', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                
                const result = await response.json();
                if (result.success) {
                    document.getElementById('analysisResult').textContent = result.analysis;
                    document.getElementById('analysisResult').style.display = 'block';
                    
                    // Display stats
                    const stats = result.stats;
                    document.getElementById('analysisStats').innerHTML = `
                        <div class="stat">
                            <div class="stat-value">${stats.total_lines}</div>
                            <div class="stat-label">Lines</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">${stats.total_characters}</div>
                            <div class="stat-label">Characters</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">${stats.unique_characters}</div>
                            <div class="stat-label">Unique Chars</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">${stats.complexity_score}</div>
                            <div class="stat-label">Complexity</div>
                        </div>
                    `;
                    document.getElementById('analysisStats').style.display = 'grid';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
    </script>
</body>
</html>
    '''
    return html

@app.route('/api/image-to-ascii', methods=['POST'])
def api_image_to_ascii():
    """API endpoint for image to ASCII conversion"""
    try:
        data = request.json
        image_data = data.get('image')
        width = data.get('width', 80)
        style = data.get('style', 'standard')
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image data provided'})
        
        ascii_art = ascii_ai.image_to_ascii(image_data, width, style)
        return jsonify({'success': True, 'ascii': ascii_art})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/text-to-ascii', methods=['POST'])
def api_text_to_ascii():
    """API endpoint for text to ASCII art conversion"""
    try:
        data = request.json
        text = data.get('text', '')
        style = data.get('style', 'block')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'})
        
        ascii_art = ascii_ai.text_to_ascii_art(text, style)
        return jsonify({'success': True, 'ascii': ascii_art})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/generate-pattern', methods=['POST'])
def api_generate_pattern():
    """API endpoint for ASCII pattern generation"""
    try:
        data = request.json
        pattern_type = data.get('type', 'random')
        size = data.get('size', 20)
        
        pattern = ascii_ai.generate_ascii_pattern(pattern_type, size)
        return jsonify({'success': True, 'pattern': pattern})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analyze-ascii', methods=['POST'])
def api_analyze_ascii():
    """API endpoint for ASCII text analysis"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'})
        
        stats = ascii_ai.analyze_ascii_complexity(text)
        analysis = f"ASCII Text Analysis:\n\n"
        analysis += f"Total Lines: {stats['total_lines']}\n"
        analysis += f"Total Characters: {stats['total_characters']}\n"
        analysis += f"Unique Characters: {stats['unique_characters']}\n"
        analysis += f"Density: {stats['density']}\n"
        analysis += f"Complexity Score: {stats['complexity_score']}\n"
        
        return jsonify({'success': True, 'analysis': analysis, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
