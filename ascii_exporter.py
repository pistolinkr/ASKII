#!/usr/bin/env python3
"""
ASCII Art Exporter
Export ASCII art to image and video formats
"""

from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os


class AsciiExporter:
    """ASCII 아트를 이미지와 비디오로 내보내는 클래스"""
    
    def __init__(self, font_size=10, bg_color=(0, 0, 0), fg_color=(255, 255, 255)):
        """
        Args:
            font_size: 폰트 크기
            bg_color: 배경색 (R, G, B)
            fg_color: 텍스트색 (R, G, B)
        """
        self.font_size = font_size
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        # Try to use a monospace font
        try:
            # macOS
            self.font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", font_size)
        except:
            try:
                # Linux
                self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
            except:
                try:
                    # Windows
                    self.font = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", font_size)
                except:
                    # Fallback to default
                    self.font = ImageFont.load_default()
    
    def text_to_image(self, ascii_text, output_path):
        """
        ASCII 텍스트를 이미지로 변환합니다
        
        Args:
            ascii_text: ASCII 아트 텍스트
            output_path: 출력 이미지 경로 (.png 또는 .jpg)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            lines = ascii_text.split('\n')
            
            # Calculate image dimensions
            # Use a sample to get char width/height
            test_bbox = self.font.getbbox('M')
            char_width = test_bbox[2] - test_bbox[0]
            char_height = test_bbox[3] - test_bbox[1]
            
            max_width = max(len(line) for line in lines) if lines else 0
            height = len(lines)
            
            img_width = max_width * char_width + 20  # Add padding
            img_height = height * char_height + 20
            
            # Create image
            img = Image.new('RGB', (img_width, img_height), self.bg_color)
            draw = ImageDraw.Draw(img)
            
            # Draw text
            y_offset = 10
            for line in lines:
                draw.text((10, y_offset), line, font=self.font, fill=self.fg_color)
                y_offset += char_height
            
            # Save image
            if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                img.save(output_path, 'JPEG', quality=95)
            else:
                img.save(output_path, 'PNG')
            
            return True
            
        except Exception as e:
            print(f"Error exporting to image: {e}")
            return False
    
    def frames_to_video(self, frames_text, output_path, fps=15, original_width=None, original_height=None):
        """
        ASCII 프레임들을 비디오로 변환합니다
        
        Args:
            frames_text: ASCII 프레임 텍스트 리스트
            output_path: 출력 비디오 경로 (.mp4, .avi, .mov)
            fps: 프레임레이트
            original_width: 원본 비디오 너비 (None이면 자동)
            original_height: 원본 비디오 높이 (None이면 자동)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not frames_text:
                return False
            
            # Get dimensions from first frame
            lines = frames_text[0].split('\n')
            test_bbox = self.font.getbbox('M')
            char_width = test_bbox[2] - test_bbox[0]
            char_height = test_bbox[3] - test_bbox[1]
            
            max_width = max(len(line) for line in lines) if lines else 0
            height = len(lines)
            
            frame_width = max_width * char_width + 20
            frame_height = height * char_height + 20
            
            # Ensure even dimensions for video encoding
            frame_width = frame_width + (frame_width % 2)
            frame_height = frame_height + (frame_height % 2)
            
            # Determine codec based on file extension
            ext = os.path.splitext(output_path)[1].lower()
            if ext == '.avi':
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
            elif ext == '.mov':
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            else:  # .mp4 or other
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            # Create video writer
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
            
            if not out.isOpened():
                print("Error: Could not open video writer")
                return False
            
            # Write frames
            for frame_text in frames_text:
                # Create PIL image
                img = Image.new('RGB', (frame_width, frame_height), self.bg_color)
                draw = ImageDraw.Draw(img)
                
                # Draw text
                y_offset = 10
                for line in frame_text.split('\n'):
                    draw.text((10, y_offset), line, font=self.font, fill=self.fg_color)
                    y_offset += char_height
                
                # Convert PIL image to OpenCV format
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                
                out.write(frame)
            
            out.release()
            return True
            
        except Exception as e:
            print(f"Error exporting to video: {e}")
            return False
    
    def video_to_ascii_video(self, input_video_path, output_path, converter, fps=15, max_frames=None):
        """
        비디오를 ASCII 비디오로 변환합니다
        
        Args:
            input_video_path: 입력 비디오 경로
            output_path: 출력 비디오 경로
            converter: AsciiConverter 인스턴스
            fps: 출력 프레임레이트
            max_frames: 최대 프레임 수
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cap = cv2.VideoCapture(input_video_path)
            
            if not cap.isOpened():
                return False
            
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            if max_frames is None:
                max_frames = total_frames
            
            frame_skip = max(1, int(original_fps / fps))
            
            # Collect ASCII frames
            frames_text = []
            frame_count = 0
            processed = 0
            
            print(f"Processing video: {total_frames} frames")
            
            while cap.isOpened() and processed < max_frames:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                if frame_count % frame_skip != 0:
                    frame_count += 1
                    continue
                
                # Convert frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Resize
                height, width = gray.shape
                aspect_ratio = height / width
                new_height = int(converter.width * aspect_ratio * 0.55)
                resized = cv2.resize(gray, (converter.width, new_height))
                
                # Convert to ASCII
                ascii_frame = converter._pixels_to_ascii(resized)
                frames_text.append(ascii_frame)
                
                frame_count += 1
                processed += 1
                
                if processed % 10 == 0:
                    print(f"Processed {processed}/{max_frames} frames")
            
            cap.release()
            
            print(f"Creating video with {len(frames_text)} frames...")
            
            # Create video from ASCII frames
            success = self.frames_to_video(
                frames_text, 
                output_path, 
                fps=fps,
                original_width=original_width,
                original_height=original_height
            )
            
            return success
            
        except Exception as e:
            print(f"Error converting video: {e}")
            return False


def main():
    """CLI for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Export ASCII art to image/video")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("output", help="Output file (.png, .jpg, .avi, .mov)")
    parser.add_argument("--font-size", type=int, default=10, help="Font size")
    parser.add_argument("--bg-color", default="0,0,0", help="Background color (R,G,B)")
    parser.add_argument("--fg-color", default="255,255,255", help="Foreground color (R,G,B)")
    
    args = parser.parse_args()
    
    # Parse colors
    bg_color = tuple(map(int, args.bg_color.split(',')))
    fg_color = tuple(map(int, args.fg_color.split(',')))
    
    exporter = AsciiExporter(
        font_size=args.font_size,
        bg_color=bg_color,
        fg_color=fg_color
    )
    
    # Read input
    with open(args.input, 'r', encoding='utf-8') as f:
        ascii_text = f.read()
    
    # Export
    success = exporter.text_to_image(ascii_text, args.output)
    
    if success:
        print(f"Successfully exported to {args.output}")
    else:
        print("Export failed")


if __name__ == "__main__":
    main()

