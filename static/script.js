// Theme detection and handling
function updateTheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
}

// Listen for theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateTheme);

// Initialize theme on load
document.addEventListener('DOMContentLoaded', updateTheme);

// Camera variables
let cameraStream = null;
let cameraInterval = null;
let isCameraRunning = false;

// Tab switching
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.dataset.tab;
        
        // Stop camera when switching tabs
        if (isCameraRunning) {
            stopCamera();
        }
        
        // Update buttons
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');
        
        // Update content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// Range slider value updates
document.getElementById('cameraWidth').addEventListener('input', (e) => {
    document.getElementById('cameraWidthValue').textContent = e.target.value;
});

document.getElementById('cameraFPS').addEventListener('input', (e) => {
    document.getElementById('cameraFPSValue').textContent = e.target.value;
});

document.getElementById('imageWidth').addEventListener('input', (e) => {
    document.getElementById('imageWidthValue').textContent = e.target.value;
});

document.getElementById('objSize').addEventListener('input', (e) => {
    document.getElementById('objSizeValue').textContent = e.target.value;
});

// Camera Functions
async function startCamera() {
    try {
        const video = document.getElementById('cameraVideo');
        const canvas = document.getElementById('cameraCanvas');
        const display = document.getElementById('cameraDisplay');
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');
        
        // Request camera access
        cameraStream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user' // Front camera
            } 
        });
        
        video.srcObject = cameraStream;
        video.play();
        
        // Update UI
        isCameraRunning = true;
        statusDot.classList.add('active');
        statusText.textContent = 'Camera On';
        document.getElementById('toggleCameraBtn').textContent = 'Pause Camera';
        document.getElementById('toggleCameraBtn').classList.remove('btn-primary');
        document.getElementById('toggleCameraBtn').classList.add('btn-warning');
        document.getElementById('captureFrameBtn').disabled = false;
        
        // Start ASCII conversion loop
        startASCIILoop();
        
    } catch (error) {
        console.error('Error accessing camera:', error);
        showNotification('Camera access denied or not available');
    }
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    
    if (cameraInterval) {
        clearInterval(cameraInterval);
        cameraInterval = null;
    }
    
    // Update UI
    isCameraRunning = false;
    document.querySelector('.status-dot').classList.remove('active');
    document.querySelector('.status-text').textContent = 'Camera Off';
    document.getElementById('toggleCameraBtn').textContent = 'Resume Camera';
    document.getElementById('toggleCameraBtn').classList.remove('btn-warning');
    document.getElementById('toggleCameraBtn').classList.add('btn-primary');
    document.getElementById('captureFrameBtn').disabled = true;
    
    // Hide video and canvas
    document.getElementById('cameraVideo').style.display = 'none';
    document.getElementById('cameraCanvas').style.display = 'none';
}

function startASCIILoop() {
    const video = document.getElementById('cameraVideo');
    const canvas = document.getElementById('cameraCanvas');
    const display = document.getElementById('cameraDisplay');
    const ctx = canvas.getContext('2d');
    
    const updateASCII = () => {
        if (!isCameraRunning) return;
        
        const width = parseInt(document.getElementById('cameraWidth').value);
        const detailed = document.getElementById('detailedCameraChars').checked;
        const invert = document.getElementById('invertCameraColors').checked;
        const mirror = document.getElementById('mirrorCamera').checked;
        const colorMode = document.getElementById('colorMode').value;
        
        // Set canvas size
        canvas.width = width;
        canvas.height = Math.floor(width * video.videoHeight / video.videoWidth * 0.55);
        
        // Draw video frame to canvas
        ctx.save();
        if (mirror) {
            ctx.scale(-1, 1);
            ctx.translate(-canvas.width, 0);
        }
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Apply color filters
        applyColorFilter(ctx, canvas.width, canvas.height, colorMode);
        
        ctx.restore();
        
        // Get image data and convert to ASCII
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const ascii = convertImageDataToASCII(imageData, width, detailed, invert);
        
        display.textContent = ascii;
    };
    
    const fps = parseInt(document.getElementById('cameraFPS').value);
    cameraInterval = setInterval(updateASCII, 1000 / fps);
}

function convertImageDataToASCII(imageData, width, detailed, invert) {
    const chars = detailed ? 
        ['$', '@', 'B', '%', '8', '&', 'W', 'M', '#', '*', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', 'Z', 'O', '0', 'Q', 'L', 'C', 'J', 'U', 'Y', 'X', 'z', 'c', 'v', 'u', 'n', 'x', 'r', 'j', 'f', 't', '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']', '?', '-', '_', '+', '~', '<', '>', 'i', '!', 'l', 'I', ';', ':', ',', '"', '^', '`', "'", '.', ' '] :
        ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' '];
    
    const charSet = invert ? chars.reverse() : chars;
    const data = imageData.data;
    const asciiLines = [];
    
    for (let y = 0; y < imageData.height; y += 2) { // Skip every other row for better aspect ratio
        let line = '';
        for (let x = 0; x < imageData.width; x++) {
            const index = (y * imageData.width + x) * 4;
            const r = data[index];
            const g = data[index + 1];
            const b = data[index + 2];
            
            // Convert RGB to grayscale
            const gray = Math.floor((r + g + b) / 3);
            const charIndex = Math.floor((gray / 255) * (charSet.length - 1));
            line += charSet[charIndex];
        }
        asciiLines.push(line);
    }
    
    return asciiLines.join('\n');
}

function applyColorFilter(ctx, width, height, colorMode) {
    const imageData = ctx.getImageData(0, 0, width, height);
    const data = imageData.data;
    
    for (let i = 0; i < data.length; i += 4) {
        let r = data[i];
        let g = data[i + 1];
        let b = data[i + 2];
        
        switch (colorMode) {
            case 'grayscale':
                const gray = (r + g + b) / 3;
                data[i] = gray;
                data[i + 1] = gray;
                data[i + 2] = gray;
                break;
                
            case 'red':
                data[i] = r;
                data[i + 1] = r * 0.3;
                data[i + 2] = r * 0.3;
                break;
                
            case 'green':
                data[i] = g * 0.3;
                data[i + 1] = g;
                data[i + 2] = g * 0.3;
                break;
                
            case 'blue':
                data[i] = b * 0.3;
                data[i + 1] = b * 0.3;
                data[i + 2] = b;
                break;
                
            case 'sepia':
                const sepiaR = Math.min(255, (r * 0.393) + (g * 0.769) + (b * 0.189));
                const sepiaG = Math.min(255, (r * 0.349) + (g * 0.686) + (b * 0.168));
                const sepiaB = Math.min(255, (r * 0.272) + (g * 0.534) + (b * 0.131));
                data[i] = sepiaR;
                data[i + 1] = sepiaG;
                data[i + 2] = sepiaB;
                break;
                
            case 'negative':
                data[i] = 255 - r;
                data[i + 1] = 255 - g;
                data[i + 2] = 255 - b;
                break;
        }
    }
    
    ctx.putImageData(imageData, 0, 0);
}

function captureFrame() {
    if (!isCameraRunning) return;
    
    const display = document.getElementById('cameraDisplay');
    const text = display.textContent;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Frame captured and copied to clipboard!');
    });
}

// Toggle Camera Function
function toggleCamera() {
    if (isCameraRunning) {
        stopCamera();
    } else {
        startCamera();
    }
}

// Camera Event Listeners
document.getElementById('toggleCameraBtn').addEventListener('click', toggleCamera);
document.getElementById('captureFrameBtn').addEventListener('click', captureFrame);

// File upload
let selectedImage = null;

document.getElementById('imageInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('convertBtn').disabled = false;
        
        const reader = new FileReader();
        reader.onload = (event) => {
            selectedImage = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// Convert Image
document.getElementById('convertBtn').addEventListener('click', async () => {
    if (!selectedImage) return;
    
    const width = parseInt(document.getElementById('imageWidth').value);
    const detailed = document.getElementById('detailedChars').checked;
    const invert = document.getElementById('invertColors').checked;
    
    const button = document.getElementById('convertBtn');
    const display = document.getElementById('imageDisplay');
    
    button.classList.add('loading');
    button.disabled = true;
    
    try {
        const response = await fetch('/api/convert-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                image: selectedImage, 
                width: width, 
                detailed: detailed,
                invert: invert
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            display.textContent = data.ascii;
        } else {
            display.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        display.textContent = `Error: ${error.message}`;
    } finally {
        button.classList.remove('loading');
        button.disabled = false;
    }
});

// Copy Image ASCII
document.getElementById('copyImageBtn').addEventListener('click', () => {
    const text = document.getElementById('imageDisplay').textContent;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!');
    });
});

// Generate 3D
document.getElementById('generate3DBtn').addEventListener('click', async () => {
    const objType = document.querySelector('input[name="objType"]:checked').value;
    const size = parseInt(document.getElementById('objSize').value);
    
    const button = document.getElementById('generate3DBtn');
    const display = document.getElementById('display3D');
    
    button.classList.add('loading');
    button.disabled = true;
    
    try {
        const response = await fetch('/api/generate-3d', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ type: objType, size: size })
        });
        
        const data = await response.json();
        
        if (data.success) {
            display.textContent = data.ascii;
        } else {
            display.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        display.textContent = `Error: ${error.message}`;
    } finally {
        button.classList.remove('loading');
        button.disabled = false;
    }
});

// Copy 3D ASCII
document.getElementById('copy3DBtn').addEventListener('click', () => {
    const text = document.getElementById('display3D').textContent;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!');
    });
});

// Notification function
function showNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #34c759;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(52, 199, 89, 0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

