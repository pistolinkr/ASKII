# ASCII AI - 아스키로 생각하는 AI

A client-side web application for creating and analyzing ASCII art. Convert images to ASCII, generate text-based ASCII art, create patterns, and analyze ASCII compositions.

## Features

- 🖼️ **Image to ASCII**: Convert uploaded images to ASCII art with customizable width and styles
- 📝 **Text to ASCII**: Generate ASCII art from text input with multiple font styles
- 🎨 **Pattern Generator**: Create geometric, fractal, and random ASCII patterns
- 🔍 **ASCII Analysis**: Analyze ASCII text for complexity, character density, and visual characteristics

## Technologies

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Image Processing**: HTML5 Canvas API
- **Deployment**: Vercel (Static Site)

## How It Works

This application runs entirely in the browser using:
- Canvas API for image processing and ASCII conversion
- Client-side algorithms for pattern generation
- Local text analysis and statistics

## Getting Started

1. Clone the repository
2. Open `templates/index.html` in a web browser
3. Or deploy to Vercel for live hosting

## Usage

### Image to ASCII
1. Upload an image file
2. Set desired width (20-200 characters)
3. Choose style (standard, detailed, blocks, minimal)
4. Click "ASCII로 변환" to generate

### Text to ASCII
1. Enter text in the input field
2. Select style (block, banner, simple)
3. Click "ASCII 아트 생성" to generate

### Pattern Generation
1. Choose pattern type (random, geometric, fractal)
2. Set size (10-50)
3. Click "패턴 생성" to create

### ASCII Analysis
1. Paste ASCII text in the textarea
2. Click "분석하기" to analyze
3. View statistics and insights

## Deployment

This project is configured for Vercel deployment:
- `vercel.json` handles routing and static file serving
- All functionality works client-side without server requirements
- Simply connect your GitHub repository to Vercel

## Browser Support

- Modern browsers with ES6+ support
- Canvas API support required for image processing
- Responsive design for mobile and desktop

## License

MIT License - feel free to use and modify as needed.
