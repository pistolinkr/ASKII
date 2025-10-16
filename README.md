# ASCII Art Studio

A comprehensive Python tool for generating dynamic ASCII art and converting images/videos to ASCII art with both CLI and GUI interfaces.

## Features

### ASCII Art Generation
- Multiple ASCII art types (banner, wave, circle, spiral, heart, box)
- Animated ASCII art (wave and spiral animations)
- Customizable parameters (size, width, characters)
- Real-time preview and animation control

### 3D ASCII Rendering
- Real-time 3D objects rotating in 360°
- Multiple shapes: Cube, Sphere, Donut (Torus), Pyramid
- Full 3D transformations with lighting and depth
- Adjustable rotation speed and detail level
- Z-buffering for proper depth rendering

### Image & Video Conversion
- Convert images to ASCII art
- Convert videos to ASCII art with playback
- Real-time webcam ASCII conversion
- Adjustable width, detail level, and brightness
- Save ASCII art to text files
- Export to image formats (PNG, JPEG)
- Export to video formats (MP4, AVI, MOV)

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## GUI Application

### Full-Featured GUI
Launch the complete ASCII Art Studio with image/video conversion:

```bash
python3 ascii_art_gui_full.py
```

Features:
- **Generate Art Tab**: Create patterns and animated ASCII art
- **Image to ASCII Tab**: Convert images to ASCII with preview, export to PNG/JPEG
- **Video to ASCII Tab**: Play videos as ASCII art in real-time, export to MP4/AVI/MOV
- **3D Objects Tab**: Real-time 3D ASCII rendering with 360° rotation
- **Theme Toggle**: Light/Dark/System theme support
- Clean, minimal Apple-style design

### Simple Generator GUI
For just pattern generation:

```bash
python3 ascii_art_gui.py
```

## CLI Usage

### Pattern Generation

Generate static ASCII art patterns:

```bash
# Generate a text banner
python3 ascii_art.py banner -t "Welcome!" -w 50 -c "#"

# Generate a wave pattern
python3 ascii_art.py wave -w 80 -s 10

# Generate a circle
python3 ascii_art.py circle -s 15 -c "O"

# Generate a spiral pattern
python3 ascii_art.py spiral -s 20

# Generate a heart
python3 ascii_art.py heart -s 12

# Generate boxed text
python3 ascii_art.py box -t "Hello World" -c "*"
```

### Animated ASCII Art

```bash
# Animate a wave (10 seconds at 10 FPS)
python3 ascii_art.py animate-wave -d 10 --fps 10

# Animate a spiral (15 seconds at 15 FPS)
python3 ascii_art.py animate-spiral -d 15 --fps 15
```

## Options

- `-t, --text`: Text to display (for text-based art)
- `-w, --width`: Width of the art
- `-s, --size`: Size of the art
- `-c, --char`: Character to use for rendering
- `-d, --duration`: Animation duration in seconds
- `--fps`: Animation frames per second

## Examples

```bash
# Large banner with custom character
python3 ascii_art.py banner -t "ASCII Art!" -w 80 -c "="

# Small circle
python3 ascii_art.py circle -s 8 -c "@"

# Fast wave animation
python3 ascii_art.py animate-wave -d 5 --fps 20
```

### Image Conversion

Convert images to ASCII art:

```bash
# Convert an image
python3 ascii_converter.py image -i photo.jpg -w 100

# Save to file
python3 ascii_converter.py image -i photo.jpg -o output.txt -w 120

# Use detailed characters
python3 ascii_converter.py image -i photo.jpg -w 100 -d

# Invert brightness
python3 ascii_converter.py image -i photo.jpg -w 100 --invert
```

### Video Conversion

Convert videos to ASCII art:

```bash
# Play video as ASCII in terminal
python3 ascii_converter.py video -i video.mp4 -w 80 -f 15

# Save video frames to file
python3 ascii_converter.py video -i video.mp4 -o output.txt -w 80

# Process first 100 frames only
python3 ascii_converter.py video -i video.mp4 -w 80 --max-frames 100
```

### Webcam

Convert webcam feed to ASCII in real-time:

```bash
# Start webcam ASCII art
python3 ascii_converter.py webcam -w 100 -f 15
```

### 3D Objects

Render rotating 3D objects in real-time:

```bash
# Rotating cube
python3 ascii_3d.py cube -f 30 -s 1.0

# Rotating sphere
python3 ascii_3d.py sphere -f 30 -s 1.5

# Rotating donut (torus)
python3 ascii_3d.py torus -f 30 -s 1.0

# Rotating pyramid
python3 ascii_3d.py pyramid -f 30 -s 2.0

# Run for 10 seconds with faster rotation
python3 ascii_3d.py cube -d 10 -f 30 -s 2.0
```

Options:
- `-d, --duration`: Animation duration in seconds (default: infinite)
- `-f, --fps`: Frame rate (default: 30)
- `-s, --speed`: Rotation speed multiplier (default: 1.0)

## Files

- `ascii_art.py` - CLI tool for pattern generation
- `ascii_converter.py` - CLI tool for image/video conversion
- `ascii_3d.py` - CLI tool for 3D object rendering
- `ascii_exporter.py` - Export ASCII art to image/video formats
- `ascii_art_gui.py` - Simple GUI for pattern generation
- `ascii_art_gui_full.py` - Full-featured GUI with all features
- `requirements.txt` - Python package dependencies

## Export Features

### Image Export
Convert ASCII art to PNG or JPEG images with original aspect ratio:
- Customizable font size and colors
- Theme-aware color schemes (Light/Dark)
- High-quality image output

### Video Export
Convert videos to ASCII art videos with original aspect ratio:
- Support for MP4, AVI, MOV formats
- Adjustable frame rate and quality
- Progress indicator during conversion
- Maintains video dimensions

**Note**: Video export processes up to 300 frames by default for reasonable processing time. For longer videos, use the CLI tools.

