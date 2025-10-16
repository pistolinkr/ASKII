#!/usr/bin/env python3
"""
ASCII Image and Video Converter
Converts images and videos to ASCII art
"""

import argparse
import cv2
import numpy as np
from PIL import Image
import sys
import time


class AsciiConverter:
    """이미지와 비디오를 ASCII로 변환하는 클래스"""
    
    # ASCII characters from dark to light
    ASCII_CHARS_SIMPLE = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
    ASCII_CHARS_DETAILED = ['$', '@', 'B', '%', '8', '&', 'W', 'M', '#', '*', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', 'Z', 'O', '0', 'Q', 'L', 'C', 'J', 'U', 'Y', 'X', 'z', 'c', 'v', 'u', 'n', 'x', 'r', 'j', 'f', 't', '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']', '?', '-', '_', '+', '~', '<', '>', 'i', '!', 'l', 'I', ';', ':', ',', '"', '^', '`', "'", '.', ' ']
    
    def __init__(self, width=100, detailed=False, invert=False, aspect_ratio=2.0):
        """
        Args:
            width: ASCII 출력의 너비
            detailed: 상세한 ASCII 문자 세트 사용 여부
            invert: 밝기 반전 여부
            aspect_ratio: 가로세로 비율 (width/height)
        """
        self.width = width
        self.chars = self.ASCII_CHARS_DETAILED if detailed else self.ASCII_CHARS_SIMPLE
        self.invert = invert
        self.aspect_ratio = aspect_ratio
        
        if invert:
            self.chars = self.chars[::-1]
    
    def image_to_ascii(self, image_path, output_file=None):
        """
        이미지를 ASCII 아트로 변환합니다
        
        Args:
            image_path: 입력 이미지 경로
            output_file: 출력 파일 경로 (None이면 콘솔 출력)
        
        Returns:
            ASCII 아트 문자열
        """
        try:
            # 이미지 로드
            img = Image.open(image_path)
            
            # 그레이스케일로 변환
            img = img.convert('L')
            
            # 종횡비 유지하며 리사이즈
            aspect_ratio = img.height / img.width
            new_height = int(self.width * aspect_ratio * 0.55)  # 0.55는 문자 종횡비 보정
            img = img.resize((self.width, new_height))
            
            # ASCII로 변환
            ascii_art = self._pixels_to_ascii(np.array(img))
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(ascii_art)
                print(f"ASCII art saved to {output_file}")
            else:
                print(ascii_art)
            
            return ascii_art
            
        except Exception as e:
            print(f"Error converting image: {e}")
            return None
    
    def video_to_ascii(self, video_path, output_file=None, fps=None, max_frames=None):
        """
        비디오를 ASCII 아트로 변환합니다
        
        Args:
            video_path: 입력 비디오 경로
            output_file: 출력 파일 경로 (None이면 콘솔 출력)
            fps: 출력 프레임레이트 (None이면 원본 사용)
            max_frames: 최대 프레임 수 (None이면 전체)
        """
        try:
            # 비디오 캡처 객체 생성
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print(f"Error: Could not open video {video_path}")
                return
            
            # 비디오 정보 가져오기
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if fps is None:
                fps = original_fps
            
            if max_frames is None:
                max_frames = total_frames
            
            frame_delay = 1.0 / fps
            frame_skip = max(1, int(original_fps / fps))
            
            print(f"Converting video: {total_frames} frames at {original_fps:.2f} FPS")
            print(f"Output: {min(max_frames, total_frames)} frames at {fps:.2f} FPS")
            print("Press Ctrl+C to stop\n")
            
            frame_count = 0
            processed_frames = 0
            
            output_list = []
            
            try:
                while cap.isOpened() and processed_frames < max_frames:
                    ret, frame = cap.read()
                    
                    if not ret:
                        break
                    
                    # 프레임 스킵
                    if frame_count % frame_skip != 0:
                        frame_count += 1
                        continue
                    
                    # 그레이스케일 변환
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # 리사이즈
                    height, width = gray.shape
                    aspect_ratio = height / width
                    new_height = int(self.width * aspect_ratio * 0.55)
                    resized = cv2.resize(gray, (self.width, new_height))
                    
                    # ASCII로 변환
                    ascii_frame = self._pixels_to_ascii(resized)
                    
                    if output_file:
                        output_list.append(ascii_frame)
                        output_list.append("\n" + "="*self.width + f" Frame {processed_frames + 1} " + "="*self.width + "\n\n")
                    else:
                        # 화면 지우고 출력
                        print("\033[2J\033[H", end="")
                        print(f"Frame {processed_frames + 1}/{min(max_frames, total_frames)}")
                        print(ascii_frame)
                        time.sleep(frame_delay)
                    
                    frame_count += 1
                    processed_frames += 1
                    
            except KeyboardInterrupt:
                print("\n\nConversion stopped by user")
            
            finally:
                cap.release()
                
                if output_file and output_list:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.writelines(output_list)
                    print(f"\nASCII video saved to {output_file}")
                
                print(f"Processed {processed_frames} frames")
                
        except Exception as e:
            print(f"Error converting video: {e}")
    
    def webcam_to_ascii(self, fps=15):
        """
        웹캠을 실시간으로 ASCII 아트로 변환합니다
        
        Args:
            fps: 프레임레이트
        """
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("Error: Could not open webcam")
                return
            
            print("Webcam ASCII Art - Press Ctrl+C to stop\n")
            frame_delay = 1.0 / fps
            
            try:
                while True:
                    ret, frame = cap.read()
                    
                    if not ret:
                        break
                    
                    # 그레이스케일 변환
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # 리사이즈
                    height, width = gray.shape
                    aspect_ratio = height / width
                    new_height = int(self.width * aspect_ratio * 0.55)
                    resized = cv2.resize(gray, (self.width, new_height))
                    
                    # ASCII로 변환
                    ascii_frame = self._pixels_to_ascii(resized)
                    
                    # 화면 지우고 출력
                    print("\033[2J\033[H", end="")
                    print("Webcam ASCII Art (Press Ctrl+C to stop)")
                    print(ascii_frame)
                    
                    time.sleep(frame_delay)
                    
            except KeyboardInterrupt:
                print("\n\nWebcam stopped by user")
            
            finally:
                cap.release()
                
        except Exception as e:
            print(f"Error with webcam: {e}")
    
    def _pixels_to_ascii(self, pixels):
        """
        픽셀 배열을 ASCII 문자열로 변환합니다
        
        Args:
            pixels: numpy array of grayscale pixel values
        
        Returns:
            ASCII art string
        """
        # 픽셀 값을 ASCII 문자 인덱스로 변환
        normalized = pixels / 255.0
        indices = (normalized * (len(self.chars) - 1)).astype(int)
        
        # 각 행을 ASCII 문자열로 변환
        ascii_lines = []
        for row in indices:
            line = ''.join(self.chars[i] for i in row)
            ascii_lines.append(line)
        
        return '\n'.join(ascii_lines)
    
    def _frame_to_ascii(self, frame):
        """비디오 프레임을 ASCII로 변환합니다"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self._pixels_to_ascii(gray)


def main():
    parser = argparse.ArgumentParser(
        description="Convert images and videos to ASCII art"
    )
    
    parser.add_argument(
        "mode",
        choices=["image", "video", "webcam"],
        help="변환 모드"
    )
    
    parser.add_argument(
        "-i", "--input",
        help="입력 파일 경로 (image/video 모드에서 필수)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="출력 파일 경로 (선택사항)"
    )
    
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=100,
        help="ASCII 아트 너비 (기본값: 100)"
    )
    
    parser.add_argument(
        "-f", "--fps",
        type=int,
        default=15,
        help="비디오/웹캠 프레임레이트 (기본값: 15)"
    )
    
    parser.add_argument(
        "--max-frames",
        type=int,
        help="비디오 최대 프레임 수"
    )
    
    parser.add_argument(
        "-d", "--detailed",
        action="store_true",
        help="상세한 ASCII 문자 세트 사용"
    )
    
    parser.add_argument(
        "--invert",
        action="store_true",
        help="밝기 반전"
    )
    
    args = parser.parse_args()
    
    # 입력 파일 검증
    if args.mode in ["image", "video"] and not args.input:
        parser.error(f"{args.mode} mode requires --input argument")
    
    # 변환기 생성
    converter = AsciiConverter(
        width=args.width,
        detailed=args.detailed,
        invert=args.invert
    )
    
    # 모드별 실행
    if args.mode == "image":
        converter.image_to_ascii(args.input, args.output)
    
    elif args.mode == "video":
        converter.video_to_ascii(
            args.input,
            args.output,
            fps=args.fps,
            max_frames=args.max_frames
        )
    
    elif args.mode == "webcam":
        converter.webcam_to_ascii(fps=args.fps)


if __name__ == "__main__":
    main()

