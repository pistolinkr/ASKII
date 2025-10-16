# ASCII Art Studio 🎨

A comprehensive web-based ASCII art generation and conversion tool. Transform images into ASCII art, generate artistic patterns, and create 3D ASCII objects - all in your browser!

## 🌐 Live Demo

**Visit the live site:** [ascii-lilac.vercel.app](https://ascii-lilac.vercel.app)

## ✨ Features

### 🎯 Web Interface

**Generate Art**
- Text banners with ASCII styling
- Geometric patterns (waves, circles, spirals, hearts)
- Box text with decorative borders
- Real-time preview with adjustable size

**Image to ASCII**
- Upload and convert images instantly
- Adjustable width (30-200 characters)
- Detailed/Simple character sets
- Color inversion option
- One-click copy to clipboard

**3D Objects**
- Render ASCII 3D shapes (cube, sphere, pyramid, torus)
- Interactive size controls
- Instant generation and preview

### 💻 CLI Tools

All features are also available as command-line tools for automation and scripting.

## 🚀 Quick Start

### Web Application

1. Clone the repository:
```bash
git clone https://github.com/pistolinkr/ASKII.git
cd ASKII
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Run the web server:
```bash
python3 app.py
```

4. Open your browser and visit:
```
http://localhost:5000
```

### CLI Usage

**Generate ASCII Art:**
```bash
python3 ascii_art.py banner -t "Hello World"
python3 ascii_art.py wave -s 20
python3 ascii_art.py heart -s 15
```

**Convert Image to ASCII:**
```bash
python3 ascii_converter.py image -i photo.jpg -w 100
python3 ascii_converter.py image -i photo.jpg -w 150 -d --invert
```

**Convert Video to ASCII:**
```bash
python3 ascii_converter.py video -i video.mp4 -w 80 --fps 15
```

**Webcam ASCII Art:**
```bash
python3 ascii_converter.py webcam --fps 15
```

**3D ASCII Objects:**
```bash
python3 ascii_3d.py cube -s 10
python3 ascii_3d.py sphere -s 15
python3 ascii_3d.py torus -s 12
```

## 🎨 Technology Stack

- **Backend**: Flask (Python 3.9+)
- **Frontend**: Vanilla JavaScript, CSS3, HTML5
- **Image Processing**: OpenCV, Pillow, NumPy
- **Deployment**: Vercel (Serverless)
- **Design**: Apple-inspired minimal aesthetic

## 📦 Dependencies

- Flask 3.0.0
- NumPy 2.0.2
- OpenCV-Python 4.12.0.88
- Pillow 11.3.0

## 🛠️ Project Structure

```
ASKII/
├── app.py                      # Flask web application
├── ascii_art.py                # ASCII art generator
├── ascii_converter.py          # Image/video converter
├── ascii_3d.py                 # 3D object renderer
├── ascii_exporter.py           # Export utilities
├── templates/
│   └── index.html              # Web interface
├── static/
│   ├── style.css               # Styles
│   └── script.js               # Client-side logic
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel deployment config
└── README.md                   # This file
```

## 🌟 Features in Detail

### Art Types

- **Banner**: Large text with ASCII styling
- **Wave**: Flowing wave patterns
- **Circle**: Perfect ASCII circles
- **Spiral**: Mesmerizing spiral patterns
- **Heart**: ASCII heart shapes
- **Box Text**: Text enclosed in decorative boxes

### Image Conversion

- Automatic aspect ratio preservation
- Grayscale conversion
- Customizable character density
- Multiple detail levels
- Brightness inversion

### 3D Rendering

- Wireframe 3D objects
- Rotating animations
- Multiple primitive shapes
- Adjustable viewing angles

## 📸 Screenshots

The web interface features:
- Clean, minimal Apple-inspired design
- Dark ASCII display panels
- Intuitive controls with sliders and radio buttons
- Real-time conversion and preview
- Responsive layout for mobile and desktop

## 🚢 Deployment

### Deploy to Vercel

1. Fork this repository
2. Sign up at [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Vercel will automatically detect the configuration
5. Deploy!

### Manual Deployment

For other platforms, ensure Python 3.9+ is available and run:

```bash
pip3 install -r requirements.txt
python3 app.py
```

The app will be available at `http://localhost:5000`

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

MIT License - feel free to use and modify as needed.

## 👤 Author

Created by [Pistol™](https://github.com/pistolinkr)

## 🔗 Links

- **Live Site**: [ascii-lilac.vercel.app](https://ascii-lilac.vercel.app)
- **GitHub**: [github.com/pistolinkr/ASKII](https://github.com/pistolinkr/ASKII)

---

**Made with ASCII** ❤️
