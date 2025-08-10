// ASCII AI Web Application JavaScript
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
                
                const response = await fetch('/api/image-to-ascii', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({image: imageData, width: parseInt(width), style: style})
                });
                
                const result = await response.json();
                if (result.success) {
                    this.displayResult('imageResult', result.ascii, 'success');
                    this.animateASCII(result.ascii, 'imageResult');
                } else {
                    this.showNotification('변환 오류: ' + result.error, 'error');
                }
            };
            reader.readAsDataURL(file);
        } catch (error) {
            this.showNotification('오류가 발생했습니다: ' + error.message, 'error');
        }
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
            const response = await fetch('/api/text-to-ascii', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text, style: style})
            });
            
            const result = await response.json();
            if (result.success) {
                this.displayResult('textResult', result.ascii, 'success');
                this.animateASCII(result.ascii, 'textResult');
            } else {
                this.showNotification('생성 오류: ' + result.error, 'error');
            }
        } catch (error) {
            this.showNotification('오류가 발생했습니다: ' + error.message, 'error');
        }
    }

    async generatePattern() {
        const type = document.getElementById('patternType').value;
        const size = parseInt(document.getElementById('patternSize').value);
        
        this.showLoading('patternResult', '패턴 생성 중...');
        
        try {
            const response = await fetch('/api/generate-pattern', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: type, size: size})
            });
            
            const result = await response.json();
            if (result.success) {
                this.displayResult('patternResult', result.pattern, 'success');
                this.animatePattern(result.pattern, 'patternResult');
            } else {
                this.showNotification('생성 오류: ' + result.error, 'error');
            }
        } catch (error) {
            this.showNotification('오류가 발생했습니다: ' + error.message, 'error');
        }
    }

    async analyzeAscii() {
        const text = document.getElementById('analyzeInput').value.trim();
        if (!text) {
            this.showNotification('분석할 ASCII 텍스트를 입력해주세요.', 'error');
            return;
        }
        
        this.showLoading('analysisResult', 'ASCII 분석 중...');
        
        try {
            const response = await fetch('/api/analyze-ascii', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });
            
            const result = await response.json();
            if (result.success) {
                this.displayResult('analysisResult', result.analysis, 'success');
                this.displayStats(result.stats);
            } else {
                this.showNotification('분석 오류: ' + result.error, 'error');
            }
        } catch (error) {
            this.showNotification('오류가 발생했습니다: ' + error.message, 'error');
        }
    }

    showLoading(elementId, message) {
        const element = document.getElementById(elementId);
        element.innerHTML = `<div class="loading"></div> ${message}`;
        element.style.display = 'block';
        element.classList.remove('success', 'error');
    }

    displayResult(elementId, content, status) {
        const element = document.getElementById(elementId);
        element.textContent = content;
        element.style.display = 'block';
        element.classList.remove('success', 'error');
        element.classList.add(status);
    }

    displayStats(stats) {
        const statsElement = document.getElementById('analysisStats');
        statsElement.innerHTML = `
            <div class="stat">
                <div class="stat-value">${stats.total_lines}</div>
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
                <div class="stat-value">${stats.complexity_score}</div>
                <div class="stat-label">복잡도</div>
            </div>
        `;
        statsElement.style.display = 'grid';
    }

    animateASCII(asciiText, elementId) {
        const element = document.getElementById(elementId);
        const lines = asciiText.split('\n');
        let currentLine = 0;
        
        element.textContent = '';
        
        const animate = () => {
            if (currentLine < lines.length) {
                element.textContent += lines[currentLine] + '\n';
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
        
        element.textContent = '';
        
        const animate = () => {
            if (currentLine < lines.length) {
                element.textContent += lines[currentLine] + '\n';
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

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('ASCII AI Application Loaded');
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

// Convert image to ASCII using OpenAI API
async function convertImage() {
    if (!currentImage) {
        alert('이미지를 먼저 업로드해주세요.');
        return;
    }

    const width = document.getElementById('width').value;
    const style = document.getElementById('style').value;
    const resultDiv = document.getElementById('imageResult');

    // Show loading
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '<div class="loading"></div> 변환 중...';

    try {
        const response = await fetch('/api/convert-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: currentImage,
                width: parseInt(width),
                style: style
            })
        });

        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `<pre class="result">${data.ascii_art}</pre>`;
        } else {
            resultDiv.innerHTML = `<div class="error">오류: ${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = '<div class="error">네트워크 오류가 발생했습니다.</div>';
    }
}

// Generate ASCII art from text using OpenAI API
async function convertText() {
    const text = document.getElementById('textInput').value.trim();
    if (!text) {
        alert('텍스트를 입력해주세요.');
        return;
    }

    const style = document.getElementById('textStyle').value;
    const resultDiv = document.getElementById('textResult');

    // Show loading
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '<div class="loading"></div> 생성 중...';

    try {
        const response = await fetch('/api/generate-text-art', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                style: style
            })
        });

        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `<pre class="result">${data.ascii_art}</pre>`;
        } else {
            resultDiv.innerHTML = `<div class="error">오류: ${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = '<div class="error">네트워크 오류가 발생했습니다.</div>';
    }
}

// Generate ASCII pattern using OpenAI API
async function generatePattern() {
    const patternType = document.getElementById('patternType').value;
    const size = document.getElementById('patternSize').value;
    const resultDiv = document.getElementById('patternResult');

    // Show loading
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '<div class="loading"></div> 패턴 생성 중...';

    try {
        const response = await fetch('/api/generate-pattern', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                patternType: patternType,
                size: parseInt(size)
            })
        });

        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `<pre class="result">${data.pattern}</pre>`;
        } else {
            resultDiv.innerHTML = `<div class="error">오류: ${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = '<div class="error">네트워크 오류가 발생했습니다.</div>';
    }
}

// Analyze ASCII text using OpenAI API
async function analyzeAscii() {
    const asciiText = document.getElementById('analyzeInput').value.trim();
    if (!asciiText) {
        alert('분석할 ASCII 텍스트를 입력해주세요.');
        return;
    }

    const resultDiv = document.getElementById('analysisResult');
    const statsDiv = document.getElementById('analysisStats');

    // Show loading
    resultDiv.style.display = 'block';
    statsDiv.style.display = 'block';
    resultDiv.innerHTML = '<div class="loading"></div> 분석 중...';
    statsDiv.innerHTML = '';

    try {
        const response = await fetch('/api/analyze-ascii', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                asciiText: asciiText
            })
        });

        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `<div class="result">${data.analysis}</div>`;
            
            // Display stats
            const stats = data.stats;
            statsDiv.innerHTML = `
                <div class="stat">
                    <div class="stat-value">${stats.total_characters}</div>
                    <div class="stat-label">총 문자 수</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${stats.unique_characters}</div>
                    <div class="stat-label">고유 문자</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${stats.lines}</div>
                    <div class="stat-label">줄 수</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${stats.character_diversity}%</div>
                    <div class="stat-label">문자 다양성</div>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `<div class="error">오류: ${data.error}</div>`;
            statsDiv.style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = '<div class="error">네트워크 오류가 발생했습니다.</div>';
        statsDiv.style.display = 'none';
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
