// ASCII AI Web Application JavaScript - Client Side Only
class ASCIIAI {
    constructor() {
        this.initializeEventListeners();
        this.setupAnimations();
    }

    initializeEventListeners() {
        // File input change event
        document.getElementById('imageInput').addEventListener('change', this.handleFileSelect.bind(this));
        
        // Real-time text preview
        document.getElementById('textInput').addEventListener('input', this.handleTextInput.bind(this));
        
        // Pattern size change
        document.getElementById('patternSize').addEventListener('change', this.handlePatternSizeChange.bind(this));
    }

    setupAnimations() {
        // Add entrance animations to sections
        const sections = document.querySelectorAll('.section');
        sections.forEach((section, index) => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                section.style.transition = 'all 0.6s ease';
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            // Show selected filename
            const fileLabel = document.querySelector('.file-label');
            fileLabel.textContent = file.name.length > 20 ? file.name.substring(0, 20) + '...' : file.name;
            
            // Preview image
            this.previewImage(file);
        }
    }

    handleTextInput(event) {
        const text = event.target.value;
        if (text.length > 0) {
            // Real-time character count
            this.updateCharacterCount(text);
        }
    }

    handlePatternSizeChange(event) {
        const size = parseInt(event.target.value);
        if (size > 30) {
            event.target.parentNode.classList.add('warning');
        } else {
            event.target.parentNode.classList.remove('warning');
        }
    }

    previewImage(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // Create preview element
            const preview = document.createElement('div');
            preview.className = 'image-preview';
            preview.innerHTML = `
                <img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 200px; border-radius: 8px;">
                <p style="margin-top: 10px; color: #00ccff; font-size: 0.9em;">이미지 미리보기</p>
            `;
            
            // Remove existing preview
            const existingPreview = document.querySelector('.image-preview');
            if (existingPreview) {
                existingPreview.remove();
            }
            
            // Add new preview
            const imageSection = document.querySelector('.section:first-child');
            imageSection.appendChild(preview);
        };
        reader.readAsDataURL(file);
    }

    updateCharacterCount(text) {
        // Update character count display
        const charCount = document.getElementById('charCount') || this.createCharCountElement();
        charCount.textContent = `문자 수: ${text.length}`;
    }

    createCharCountElement() {
        const textInput = document.getElementById('textInput');
        const charCount = document.createElement('div');
        charCount.id = 'charCount';
        charCount.style.cssText = 'color: #00ccff; font-size: 0.9em; margin-top: 5px;';
        textInput.parentNode.appendChild(charCount);
        return charCount;
    }

    async convertImage() {
        const file = document.getElementById('imageInput').files[0];
        if (!file) {
            this.showNotification('이미지 파일을 선택해주세요.', 'error');
            return;
        }

        const width = document.getElementById('width').value;
        const style = document.getElementById('style').value;
        
        this.showLoading('imageResult', '이미지를 ASCII로 변환 중...');
        
        try {
            const reader = new FileReader();
            reader.onload = async (e) => {
                const imageData = e.target.result;
                
                // Convert image to ASCII using canvas
                const asciiArt = await this.imageToAscii(imageData, parseInt(width), style);
                this.displayResult('imageResult', asciiArt, 'success');
                this.animateASCII(asciiArt, 'imageResult');
            };
            reader.readAsDataURL(file);
        } catch (error) {
            this.showNotification('오류가 발생했습니다: ' + error.message, 'error');
        }
    }

    async imageToAscii(imageData, width, style) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                
                // Calculate height maintaining aspect ratio
                const aspectRatio = img.height / img.width;
                const height = Math.floor(width * aspectRatio * 0.5); // Adjust for character aspect ratio
                
                canvas.width = width;
                canvas.height = height;
                
                // Draw and resize image
                ctx.drawImage(img, 0, 0, width, height);
                
                // Get image data
                const imageData = ctx.getImageData(0, 0, width, height);
                const data = imageData.data;
                
                // ASCII characters from dark to light
                const asciiChars = style === 'detailed' ? ' .:-=+*#%@' :
                                 style === 'blocks' ? ' █▓▒░ ' :
                                 style === 'minimal' ? ' .*#@' :
                                 ' .:-=+*#%@';
                
                let asciiArt = '';
                
                for (let y = 0; y < height; y++) {
                    for (let x = 0; x < width; x++) {
                        const index = (y * width + x) * 4;
                        const r = data[index];
                        const g = data[index + 1];
                        const b = data[index + 2];
                        
                        // Convert to grayscale
                        const gray = 0.299 * r + 0.587 * g + 0.114 * b;
                        
                        // Map to ASCII character
                        const charIndex = Math.floor((gray / 255) * (asciiChars.length - 1));
                        asciiArt += asciiChars[charIndex];
                    }
                    asciiArt += '\n';
                }
                
                resolve(asciiArt);
            };
            img.src = imageData;
        });
    }

    async convertText() {
        const text = document.getElementById('textInput').value.trim();
        if (!text) {
            this.showNotification('텍스트를 입력해주세요.', 'error');
            return;
        }

        const style = document.getElementById('textStyle').value;
        
        this.showLoading('textResult', 'ASCII 아트 생성 중...');
        
        try {
            const asciiArt = this.textToAscii(text, style);
            this.displayResult('textResult', asciiArt, 'success');
            this.animateASCII(asciiArt, 'textResult');
        } catch (error) {
            this.showNotification('생성 오류: ' + error.message, 'error');
        }
    }

    textToAscii(text, style) {
        const asciiFonts = {
            block: [
                ' ██████  █████  ███████ ██ ██████ ██ ████████ ',
                '██      ██   ██ ██      ██ ██   ██ ██       ██',
                '██      ███████ ███████ ██ ██   ██ ████████ ',
                '██      ██   ██ ██      ██ ██   ██ ██       ██',
                ' ██████ ██   ██ ███████ ██ ██████  ████████ '
            ],
            banner: [
                ' ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ',
                '█ ▄▄▄▄▄ █ ▄▄▄▄▄ █ ▄▄▄▄▄ █ ▄▄▄▄▄ █ ▄▄▄▄▄ █',
                '█ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █',
                '█▄▄▄▄▄▄█▄▄▄▄▄▄█▄▄▄▄▄▄█▄▄▄▄▄▄█▄▄▄▄▄▄█',
                ' ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ '
            ],
            simple: [
                ' ___    ___    ___    ___    ___    ___ ',
                '|   |  |   |  |   |  |   |  |   |  |   |',
                '|___|  |___|  |___|  |___|  |___|  |___|',
                ' ___    ___    ___    ___    ___    ___ '
            ]
        };

        const font = asciiFonts[style] || asciiFonts.simple;
        let result = '';
        
        for (let line of font) {
            result += line + '\n';
        }
        
        return result;
    }

    async generatePattern() {
        const type = document.getElementById('patternType').value;
        const size = parseInt(document.getElementById('patternSize').value);
        
        this.showLoading('patternResult', '패턴 생성 중...');
        
        try {
            const pattern = this.generateAsciiPattern(type, size);
            this.displayResult('patternResult', pattern, 'success');
            this.animatePattern(pattern, 'patternResult');
        } catch (error) {
            this.showNotification('생성 오류: ' + error.message, 'error');
        }
    }

    generateAsciiPattern(type, size) {
        const chars = ' .:-=+*#%@';
        let pattern = '';
        
        switch(type) {
            case 'geometric':
                for (let y = 0; y < size; y++) {
                    for (let x = 0; x < size; x++) {
                        if (x === y || x === size - 1 - y || x === 0 || x === size - 1 || y === 0 || y === size - 1) {
                            pattern += '#';
                        } else if (Math.abs(x - size/2) + Math.abs(y - size/2) < size/3) {
                            pattern += '*';
                        } else {
                            pattern += ' ';
                        }
                    }
                    pattern += '\n';
                }
                break;
                
            case 'fractal':
                for (let y = 0; y < size; y++) {
                    for (let x = 0; x < size; x++) {
                        const cx = (x - size/2) / (size/4);
                        const cy = (y - size/2) / (size/4);
                        const value = Math.sin(cx) * Math.cos(cy) * 5;
                        const charIndex = Math.floor((value + 5) / 10 * (chars.length - 1));
                        pattern += chars[Math.max(0, Math.min(chars.length - 1, charIndex))];
                    }
                    pattern += '\n';
                }
                break;
                
            default: // random
                for (let y = 0; y < size; y++) {
                    for (let x = 0; x < size; x++) {
                        const random = Math.random();
                        if (random < 0.1) pattern += '#';
                        else if (random < 0.3) pattern += '*';
                        else if (random < 0.6) pattern += '+';
                        else pattern += ' ';
                    }
                    pattern += '\n';
                }
        }
        
        return pattern;
    }

    async analyzeAscii() {
        const text = document.getElementById('analyzeInput').value.trim();
        if (!text) {
            this.showNotification('분석할 ASCII 텍스트를 입력해주세요.', 'error');
            return;
        }
        
        this.showLoading('analysisResult', 'ASCII 분석 중...');
        
        try {
            const analysis = this.analyzeAsciiText(text);
            const stats = this.calculateStats(text);
            
            this.displayResult('analysisResult', analysis, 'success');
            this.displayStats(stats);
        } catch (error) {
            this.showNotification('분석 오류: ' + error.message, 'error');
        }
    }

    analyzeAsciiText(text) {
        const lines = text.split('\n');
        const nonEmptyLines = lines.filter(line => line.trim().length > 0);
        
        let analysis = `ASCII 아트 분석 결과:\n\n`;
        analysis += `📊 기본 정보:\n`;
        analysis += `• 총 줄 수: ${lines.length}\n`;
        analysis += `• 비어있지 않은 줄: ${nonEmptyLines.length}\n`;
        analysis += `• 평균 줄 길이: ${Math.round(nonEmptyLines.reduce((sum, line) => sum + line.length, 0) / nonEmptyLines.length)}\n\n`;
        
        analysis += `🎨 시각적 특징:\n`;
        const charDensity = this.calculateCharacterDensity(text);
        analysis += `• 문자 밀도: ${charDensity.toFixed(2)}%\n`;
        
        const complexity = this.calculateComplexity(text);
        analysis += `• 복잡도 점수: ${complexity.toFixed(1)}/10\n`;
        
        return analysis;
    }

    calculateStats(text) {
        const totalChars = text.length;
        const uniqueChars = new Set(text.replace(/\s/g, '')).size;
        const lines = text.split('\n').length;
        const characterDiversity = totalChars > 0 ? (uniqueChars / totalChars * 100) : 0;
        
        return {
            total_characters: totalChars,
            unique_characters: uniqueChars,
            lines: lines,
            character_diversity: Math.round(characterDiversity * 100) / 100
        };
    }

    calculateCharacterDensity(text) {
        const nonWhitespace = text.replace(/\s/g, '').length;
        return (nonWhitespace / text.length) * 100;
    }

    calculateComplexity(text) {
        const uniqueChars = new Set(text.replace(/\s/g, '')).size;
        const lines = text.split('\n').length;
        const avgLineLength = text.length / lines;
        
        // Complexity based on unique characters, line count, and average line length
        return Math.min(10, (uniqueChars * 0.3 + lines * 0.2 + avgLineLength * 0.1));
    }

    showLoading(elementId, message) {
        const element = document.getElementById(elementId);
        element.innerHTML = `<div class="loading"></div> ${message}`;
        element.style.display = 'block';
        element.classList.remove('success', 'error');
    }

    displayResult(elementId, content, status) {
        const element = document.getElementById(elementId);
        element.innerHTML = `<pre class="result">${content}</pre>`;
        element.style.display = 'block';
        element.classList.remove('success', 'error');
        element.classList.add(status);
    }

    displayStats(stats) {
        const statsElement = document.getElementById('analysisStats');
        statsElement.innerHTML = `
            <div class="stat">
                <div class="stat-value">${stats.lines}</div>
                <div class="stat-label">줄 수</div>
            </div>
            <div class="stat">
                <div class="stat-value">${stats.total_characters}</div>
                <div class="stat-label">총 문자</div>
            </div>
            <div class="stat">
                <div class="stat-value">${stats.unique_characters}</div>
                <div class="stat-label">고유 문자</div>
            </div>
            <div class="stat">
                <div class="stat-value">${stats.character_diversity}%</div>
                <div class="stat-label">문자 다양성</div>
            </div>
        `;
        statsElement.style.display = 'grid';
    }

    animateASCII(asciiText, elementId) {
        const element = document.getElementById(elementId);
        const lines = asciiText.split('\n');
        let currentLine = 0;
        
        element.innerHTML = '';
        
        const animate = () => {
            if (currentLine < lines.length) {
                element.innerHTML += lines[currentLine] + '\n';
                element.scrollTop = element.scrollHeight;
                currentLine++;
                setTimeout(animate, 50);
            }
        };
        
        animate();
    }

    animatePattern(pattern, elementId) {
        const element = document.getElementById(elementId);
        const lines = pattern.split('\n');
        let currentLine = 0;
        
        element.innerHTML = '';
        
        const animate = () => {
            if (currentLine < lines.length) {
                element.innerHTML += lines[currentLine] + '\n';
                element.scrollTop = element.scrollHeight;
                currentLine++;
                setTimeout(animate, 30);
            }
        };
        
        animate();
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            background: ${type === 'error' ? '#ff4444' : type === 'success' ? '#00ff88' : '#00ccff'};
            color: #000;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            z-index: 1000;
            font-weight: bold;
            transform: translateX(400px);
            transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Global variables
let currentImage = null;
let asciiAI = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('ASCII AI Application Loaded');
    asciiAI = new ASCIIAI();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Image input change
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', handleImageUpload);
    }

    // File label click
    const fileLabel = document.querySelector('.file-label');
    if (fileLabel) {
        fileLabel.addEventListener('click', () => imageInput.click());
    }
}

// Handle image upload
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        currentImage = e.target.result;
        console.log('Image loaded successfully');
    };
    reader.readAsDataURL(file);
}

// Convert image to ASCII
async function convertImage() {
    if (asciiAI) {
        asciiAI.convertImage();
    }
}

// Generate ASCII art from text
async function convertText() {
    if (asciiAI) {
        asciiAI.convertText();
    }
}

// Generate ASCII pattern
async function generatePattern() {
    if (asciiAI) {
        asciiAI.generatePattern();
    }
}

// Analyze ASCII text
async function analyzeAscii() {
    if (asciiAI) {
        asciiAI.analyzeAscii();
    }
}

// Utility functions
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showMessage('클립보드에 복사되었습니다!', 'success');
    }).catch(() => {
        showMessage('복사에 실패했습니다.', 'error');
    });
}

// Download ASCII art
function downloadAscii(asciiText, filename = 'ascii-art.txt') {
    const blob = new Blob([asciiText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case '1':
                e.preventDefault();
                document.getElementById('imageInput').click();
                break;
            case '2':
                e.preventDefault();
                document.getElementById('textInput').focus();
                break;
            case '3':
                e.preventDefault();
                generatePattern();
                break;
            case '4':
                e.preventDefault();
                document.getElementById('analyzeInput').focus();
                break;
        }
    }
});
