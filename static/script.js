// Tab switching
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.dataset.tab;
        
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
document.getElementById('artSize').addEventListener('input', (e) => {
    document.getElementById('artSizeValue').textContent = e.target.value;
});

document.getElementById('imageWidth').addEventListener('input', (e) => {
    document.getElementById('imageWidthValue').textContent = e.target.value;
});

document.getElementById('objSize').addEventListener('input', (e) => {
    document.getElementById('objSizeValue').textContent = e.target.value;
});

// Generate Art
document.getElementById('generateBtn').addEventListener('click', async () => {
    const artType = document.querySelector('input[name="artType"]:checked').value;
    const text = document.getElementById('artText').value;
    const size = parseInt(document.getElementById('artSize').value);
    
    const button = document.getElementById('generateBtn');
    const display = document.getElementById('artDisplay');
    
    button.classList.add('loading');
    button.disabled = true;
    
    try {
        const response = await fetch('/api/generate-art', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ type: artType, text: text, size: size })
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

// Copy Generate Art
document.getElementById('copyGenerateBtn').addEventListener('click', () => {
    const text = document.getElementById('artDisplay').textContent;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!');
    });
});

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

