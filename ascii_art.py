#!/usr/bin/env python3
"""
Dynamic ASCII Art Generator
Generates customizable ASCII art with variable rendering options
"""

import argparse
import math
import time
from typing import Callable


class AsciiArtRenderer:
    """ASCII 아트를 가변적으로 렌더링하는 클래스"""
    
    def __init__(self):
        self.letter_spacing = 1  # 자간 (문자 간 간격)
        self.line_spacing = 1    # 행간 (줄 간 간격)
        self.font_size = 1       # 폰트 크기 배율
        self.use_depth_rendering = True  # 깊이 기반 렌더링 사용 여부
        self.use_edge_detection = True   # 경계선 감지 사용 여부
    
    def set_spacing(self, letter_spacing: int = 1, line_spacing: int = 1):
        """자간과 행간을 설정합니다"""
        self.letter_spacing = max(0, letter_spacing)
        self.line_spacing = max(0, line_spacing)
    
    def set_font_size(self, size: int = 1):
        """폰트 크기를 설정합니다"""
        self.font_size = max(1, size)
    
    def apply_spacing(self, text: str) -> str:
        """텍스트에 자간과 행간을 적용합니다"""
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # 자간 적용
            if self.letter_spacing > 1:
                spaced_line = ''
                for i, char in enumerate(line):
                    spaced_line += char
                    if i < len(line) - 1:  # 마지막 문자가 아닌 경우
                        spaced_line += ' ' * (self.letter_spacing - 1)
                line = spaced_line
            
            # 폰트 크기 적용 (가로로 확장)
            if self.font_size > 1:
                expanded_line = ''
                for char in line:
                    if char == ' ':
                        expanded_line += ' ' * self.font_size
                    else:
                        expanded_line += char * self.font_size
                line = expanded_line
            
            processed_lines.append(line)
        
        # 행간 적용
        if self.line_spacing > 1:
            final_lines = []
            for i, line in enumerate(processed_lines):
                final_lines.append(line)
                if i < len(processed_lines) - 1:  # 마지막 줄이 아닌 경우
                    # 빈 줄 추가
                    for _ in range(self.line_spacing - 1):
                        final_lines.append('')
            return '\n'.join(final_lines)
        
        return '\n'.join(processed_lines)
    
    def depth_based_render(self, shape_data, width, height, char="*"):
        """깊이 기반으로 ASCII 아트를 렌더링합니다"""
        # 깊이 맵 생성
        depth_map = self._create_depth_map(shape_data, width, height)
        
        # Z-order 정렬을 위한 점들 수집
        points = []
        for y in range(height):
            for x in range(width):
                if depth_map[y][x] > 0:
                    points.append((x, y, depth_map[y][x]))
        
        # Z-order로 정렬 (깊이순)
        points.sort(key=lambda p: p[2], reverse=True)
        
        # 캔버스 초기화
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # 경계선 감지
        if self.use_edge_detection:
            edges = self._detect_edges(depth_map, width, height)
        
        # 점들을 Z-order대로 렌더링
        for x, y, depth in points:
            if self.use_edge_detection and edges[y][x]:
                # 경계선에는 더 선명한 문자 사용
                canvas[y][x] = self._get_edge_char(depth)
            else:
                # 일반 영역에는 깊이에 따른 문자 사용
                canvas[y][x] = self._get_depth_char(depth)
        
        # 결과를 문자열로 변환
        lines = [''.join(row) for row in canvas]
        result = '\n'.join(lines)
        return self.apply_spacing(result)
    
    def _create_depth_map(self, shape_data, width, height):
        """모양 데이터로부터 깊이 맵을 생성합니다"""
        depth_map = [[0 for _ in range(width)] for _ in range(height)]
        
        for y in range(height):
            for x in range(width):
                if isinstance(shape_data, list) and len(shape_data) > y:
                    if isinstance(shape_data[y], list) and len(shape_data[y]) > x:
                        depth_map[y][x] = shape_data[y][x]
                else:
                    # 함수형 데이터의 경우
                    depth_map[y][x] = self._calculate_depth(x, y, shape_data, width, height)
        
        return depth_map
    
    def _calculate_depth(self, x, y, shape_func, width, height):
        """특정 좌표의 깊이를 계산합니다"""
        if callable(shape_func):
            return shape_func(x, y, width, height)
        return 0
    
    def _detect_edges(self, depth_map, width, height):
        """깊이 맵에서 경계선을 감지합니다"""
        edges = [[False for _ in range(width)] for _ in range(height)]
        
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                current_depth = depth_map[y][x]
                if current_depth > 0:
                    # 8방향 이웃 체크
                    neighbors = [
                        depth_map[y-1][x-1], depth_map[y-1][x], depth_map[y-1][x+1],
                        depth_map[y][x-1],                     depth_map[y][x+1],
                        depth_map[y+1][x-1], depth_map[y+1][x], depth_map[y+1][x+1]
                    ]
                    
                    # 이웃 중에 배경(0)이 있거나 깊이 차이가 큰 경우 경계선으로 판단
                    if any(n == 0 for n in neighbors) or any(abs(n - current_depth) > 0.3 for n in neighbors if n > 0):
                        edges[y][x] = True
        
        return edges
    
    def _get_edge_char(self, depth):
        """경계선용 문자를 깊이에 따라 선택합니다"""
        edge_chars = ['#', '@', '%', '&', '*', '+', '=', '-', '~', '.']
        depth_index = min(int(depth * len(edge_chars)), len(edge_chars) - 1)
        return edge_chars[depth_index]
    
    def _get_depth_char(self, depth):
        """깊이에 따른 문자를 선택합니다"""
        if depth <= 0:
            return ' '
        elif depth <= 0.1:
            return '.'
        elif depth <= 0.2:
            return ':'
        elif depth <= 0.3:
            return '-'
        elif depth <= 0.4:
            return '='
        elif depth <= 0.5:
            return '+'
        elif depth <= 0.6:
            return '*'
        elif depth <= 0.7:
            return '#'
        elif depth <= 0.8:
            return '%'
        elif depth <= 0.9:
            return '@'
        else:
            return '&'
    
    @staticmethod
    def clear_screen():
        """화면을 지웁니다"""
        print("\033[2J\033[H", end="")
    
    def text_banner(self, text: str, width: int = 60, char: str = "*") -> str:
        """텍스트 배너를 생성합니다"""
        lines = []
        lines.append(char * width)
        
        # 텍스트를 중앙 정렬
        padding = (width - len(text) - 2) // 2
        line = char + " " * padding + text + " " * (width - len(text) - padding - 2) + char
        lines.append(line)
        
        lines.append(char * width)
        result = "\n".join(lines)
        return self.apply_spacing(result)
    
    def wave(self, width: int = 80, height: int = 10, phase: float = 0) -> str:
        """사인 파형 ASCII 아트를 생성합니다"""
        lines = []
        for y in range(height):
            line = ""
            for x in range(width):
                # 사인 파형 계산
                wave_y = height / 2 + (height / 4) * math.sin((x / width) * 4 * math.pi + phase)
                if abs(y - wave_y) < 0.5:
                    line += "~"
                else:
                    line += " "
            lines.append(line)
        result = "\n".join(lines)
        return self.apply_spacing(result)
    
    def circle(self, radius: int = 10, char: str = "O") -> str:
        """원 형태의 ASCII 아트를 생성합니다"""
        if self.use_depth_rendering:
            return self._render_circle_depth(radius)
        else:
            lines = []
            for y in range(-radius, radius + 1):
                line = ""
                for x in range(-radius * 2, radius * 2 + 1):
                    # 원의 방정식: x^2 + y^2 = r^2
                    distance = math.sqrt((x / 2) ** 2 + y ** 2)
                    if abs(distance - radius) < 0.5:
                        line += char
                    else:
                        line += " "
                lines.append(line)
            result = "\n".join(lines)
            return self.apply_spacing(result)
    
    def _render_circle_depth(self, radius: int) -> str:
        """깊이 기반으로 원을 렌더링합니다"""
        width = radius * 4 + 1
        height = radius * 2 + 1
        
        def circle_depth_func(x, y, w, h):
            center_x = w // 2
            center_y = h // 2
            dx = (x - center_x) / 2
            dy = y - center_y
            distance = math.sqrt(dx**2 + dy**2)
            
            if abs(distance - radius) < 0.5:
                # 경계선: 깊이 1.0
                return 1.0
            elif distance < radius:
                # 내부: 거리에 반비례하는 깊이
                return max(0.1, 1.0 - (distance / radius) * 0.8)
            else:
                # 외부
                return 0.0
        
        return self.depth_based_render(circle_depth_func, width, height)
    
    def spiral(self, size: int = 20, density: float = 0.5, rotation: float = 0) -> str:
        """나선형 ASCII 아트를 생성합니다"""
        if self.use_depth_rendering:
            return self._render_spiral_depth(size, density, rotation)
        else:
            lines = []
            center = size
            for y in range(size * 2):
                line = ""
                for x in range(size * 2):
                    dx = x - center
                    dy = y - center
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    angle = math.atan2(dy, dx) + rotation
                    
                    # 나선 패턴
                    spiral_value = (angle + distance * density) % (2 * math.pi)
                    if spiral_value < math.pi:
                        line += "*"
                    else:
                        line += " "
                lines.append(line)
            result = "\n".join(lines)
            return self.apply_spacing(result)
    
    def _render_spiral_depth(self, size: int, density: float, rotation: float) -> str:
        """깊이 기반으로 나선을 렌더링합니다"""
        width = size * 2
        height = size * 2
        
        def spiral_depth_func(x, y, w, h):
            center_x = w // 2
            center_y = h // 2
            dx = x - center_x
            dy = y - center_y
            distance = math.sqrt(dx*dx + dy*dy)
            angle = math.atan2(dy, dx) + rotation
            
            # 나선 패턴
            spiral_value = (angle + distance * density) % (2 * math.pi)
            
            if spiral_value < math.pi:
                # 나선 영역: 각도에 따른 깊이
                return max(0.1, spiral_value / math.pi)
            else:
                return 0.0
        
        return self.depth_based_render(spiral_depth_func, width, height)
    
    def heart(self, size: int = 10) -> str:
        """하트 모양 ASCII 아트를 생성합니다"""
        if self.use_depth_rendering:
            return self._render_heart_depth(size)
        else:
            lines = []
            for y in range(size * 2):
                line = ""
                for x in range(size * 3):
                    # 하트 방정식을 이용한 패턴
                    px = (x - size * 1.5) / size
                    py = (y - size * 0.8) / size
                    
                    # 하트 함수
                    value = (px ** 2 + py ** 2 - 1) ** 3 - px ** 2 * py ** 3
                    
                    if value < 0:
                        line += "♥"
                    else:
                        line += " "
                lines.append(line)
            result = "\n".join(lines)
            return self.apply_spacing(result)
    
    def _render_heart_depth(self, size: int) -> str:
        """깊이 기반으로 하트를 렌더링합니다"""
        width = size * 3
        height = size * 2
        
        def heart_depth_func(x, y, w, h):
            # 하트 방정식을 이용한 패턴
            px = (x - w/2) / size
            py = (y - h/2) / size
            
            # 하트 함수
            value = (px ** 2 + py ** 2 - 1) ** 3 - px ** 2 * py ** 3
            
            if value < 0:
                # 하트 내부: 중심에서 멀어질수록 깊이 감소
                distance_from_center = math.sqrt(px*px + py*py)
                return max(0.1, 1.0 - distance_from_center * 0.5)
            else:
                return 0.0
        
        return self.depth_based_render(heart_depth_func, width, height)
    
    def box_text(self, text: str, padding: int = 2, char: str = "#") -> str:
        """텍스트를 박스로 감쌉니다"""
        lines = text.split("\n")
        max_width = max(len(line) for line in lines)
        
        result = []
        result.append(char * (max_width + padding * 2 + 2))
        
        for line in lines:
            padded_line = line + " " * (max_width - len(line))
            result.append(char + " " * padding + padded_line + " " * padding + char)
        
        result.append(char * (max_width + padding * 2 + 2))
        return "\n".join(result)


def animate_wave(duration: int = 10, fps: int = 10):
    """파형 애니메이션을 실행합니다"""
    renderer = AsciiArtRenderer()
    frames = duration * fps
    
    for i in range(frames):
        renderer.clear_screen()
        phase = (i / fps) * 2 * math.pi
        art = renderer.wave(width=80, height=15, phase=phase)
        print(art)
        time.sleep(1 / fps)


def animate_spiral(duration: int = 10, fps: int = 10):
    """나선 애니메이션을 실행합니다"""
    renderer = AsciiArtRenderer()
    frames = duration * fps
    
    for i in range(frames):
        renderer.clear_screen()
        rotation = (i / fps) * math.pi / 2
        art = renderer.spiral(size=20, density=0.5, rotation=rotation)
        print(art)
        time.sleep(1 / fps)


def main():
    parser = argparse.ArgumentParser(
        description="Dynamic ASCII Art Generator - 가변 ASCII 아트 생성기"
    )
    
    parser.add_argument(
        "type",
        choices=["banner", "wave", "circle", "spiral", "heart", "box", "animate-wave", "animate-spiral"],
        help="생성할 ASCII 아트 타입"
    )
    
    parser.add_argument(
        "-t", "--text",
        default="Hello, World!",
        help="텍스트 기반 아트에 사용할 텍스트"
    )
    
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=60,
        help="아트의 너비"
    )
    
    parser.add_argument(
        "-s", "--size",
        type=int,
        default=10,
        help="아트의 크기"
    )
    
    parser.add_argument(
        "-c", "--char",
        default="*",
        help="사용할 문자"
    )
    
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=10,
        help="애니메이션 지속 시간 (초)"
    )
    
    parser.add_argument(
        "--fps",
        type=int,
        default=10,
        help="애니메이션 FPS"
    )
    
    args = parser.parse_args()
    renderer = AsciiArtRenderer()
    
    if args.type == "banner":
        art = renderer.text_banner(args.text, args.width, args.char)
        print(art)
    
    elif args.type == "wave":
        art = renderer.wave(width=args.width, height=args.size)
        print(art)
    
    elif args.type == "circle":
        art = renderer.circle(radius=args.size, char=args.char)
        print(art)
    
    elif args.type == "spiral":
        art = renderer.spiral(size=args.size)
        print(art)
    
    elif args.type == "heart":
        art = renderer.heart(size=args.size)
        print(art)
    
    elif args.type == "box":
        art = renderer.box_text(args.text, padding=2, char=args.char)
        print(art)
    
    elif args.type == "animate-wave":
        animate_wave(duration=args.duration, fps=args.fps)
    
    elif args.type == "animate-spiral":
        animate_spiral(duration=args.duration, fps=args.fps)


if __name__ == "__main__":
    main()

