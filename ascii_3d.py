#!/usr/bin/env python3
"""
3D ASCII Art Renderer
Real-time rotating 3D objects in ASCII
"""

import math
import time
import argparse
import numpy as np
from typing import Tuple


class ASCII3DRenderer:
    """3D 객체를 ASCII로 렌더링하는 클래스"""
    
    BRIGHTNESS_CHARS = ".,-~:;=!*#$@"
    
    def __init__(self, width=80, height=40):
        self.width = width
        self.height = height
        self.buffer = [[' ' for _ in range(width)] for _ in range(height)]
        self.zbuffer = [[float('-inf') for _ in range(width)] for _ in range(height)]
    
    def clear(self):
        """버퍼를 초기화합니다"""
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.zbuffer = [[float('-inf') for _ in range(self.width)] for _ in range(self.height)]
    
    def project(self, x, y, z, distance=5):
        """3D 좌표를 2D 화면 좌표로 투영합니다"""
        factor = distance / (distance + z)
        screen_x = int(self.width / 2 + x * factor * 20)
        screen_y = int(self.height / 2 - y * factor * 10)
        return screen_x, screen_y, z
    
    def set_pixel(self, x, y, z, brightness):
        """픽셀을 설정합니다 (z-buffering 적용)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            if z > self.zbuffer[y][x]:
                self.zbuffer[y][x] = z
                char_idx = int(brightness * (len(self.BRIGHTNESS_CHARS) - 1))
                char_idx = max(0, min(len(self.BRIGHTNESS_CHARS) - 1, char_idx))
                self.buffer[y][x] = self.BRIGHTNESS_CHARS[char_idx]
    
    def render(self):
        """버퍼를 문자열로 렌더링합니다"""
        return '\n'.join(''.join(row) for row in self.buffer)
    
    def rotate_x(self, x, y, z, angle):
        """X축 회전"""
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return x, y * cos_a - z * sin_a, y * sin_a + z * cos_a
    
    def rotate_y(self, x, y, z, angle):
        """Y축 회전"""
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a
    
    def rotate_z(self, x, y, z, angle):
        """Z축 회전"""
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return x * cos_a - y * sin_a, x * sin_a + y * cos_a, z
    
    def calculate_lighting(self, nx, ny, nz, light_x=0, light_y=0, light_z=-1):
        """조명 계산 (Lambert shading)"""
        # 법선 벡터와 광원 벡터의 내적
        length = math.sqrt(light_x**2 + light_y**2 + light_z**2)
        light_x, light_y, light_z = light_x/length, light_y/length, light_z/length
        
        dot = nx * light_x + ny * light_y + nz * light_z
        return max(0, dot)
    
    def draw_cube(self, angle_x, angle_y, angle_z, size=1.5):
        """회전하는 큐브를 그립니다"""
        vertices = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]
        
        faces = [
            (0, 1, 2, 3), (4, 5, 6, 7),  # front, back
            (0, 1, 5, 4), (2, 3, 7, 6),  # bottom, top
            (0, 3, 7, 4), (1, 2, 6, 5)   # left, right
        ]
        
        face_normals = [
            (0, 0, -1), (0, 0, 1),
            (0, -1, 0), (0, 1, 0),
            (-1, 0, 0), (1, 0, 0)
        ]
        
        # 회전된 정점 계산
        rotated_vertices = []
        for vx, vy, vz in vertices:
            vx, vy, vz = vx * size, vy * size, vz * size
            vx, vy, vz = self.rotate_x(vx, vy, vz, angle_x)
            vx, vy, vz = self.rotate_y(vx, vy, vz, angle_y)
            vx, vy, vz = self.rotate_z(vx, vy, vz, angle_z)
            rotated_vertices.append((vx, vy, vz))
        
        # 각 면 그리기
        for face_idx, face in enumerate(faces):
            v1, v2, v3, v4 = [rotated_vertices[i] for i in face]
            
            # 면의 중심과 법선 계산
            cx = (v1[0] + v2[0] + v3[0] + v4[0]) / 4
            cy = (v1[1] + v2[1] + v3[1] + v4[1]) / 4
            cz = (v1[2] + v2[2] + v3[2] + v4[2]) / 4
            
            # 법선 벡터 회전
            nx, ny, nz = face_normals[face_idx]
            nx, ny, nz = self.rotate_x(nx, ny, nz, angle_x)
            nx, ny, nz = self.rotate_y(nx, ny, nz, angle_y)
            nx, ny, nz = self.rotate_z(nx, ny, nz, angle_z)
            
            # 조명 계산
            brightness = self.calculate_lighting(nx, ny, nz)
            
            # 면 채우기
            self._fill_quad(v1, v2, v3, v4, brightness)
    
    def draw_sphere(self, angle_x, angle_y, radius=1.5, detail=30):
        """회전하는 구를 그립니다"""
        for i in range(detail):
            for j in range(detail):
                theta = (i / detail) * math.pi
                phi = (j / detail) * 2 * math.pi
                
                x = radius * math.sin(theta) * math.cos(phi)
                y = radius * math.sin(theta) * math.sin(phi)
                z = radius * math.cos(theta)
                
                # 회전 적용
                x, y, z = self.rotate_x(x, y, z, angle_x)
                x, y, z = self.rotate_y(x, y, z, angle_y)
                
                # 법선 벡터 (구의 중심에서 표면으로)
                length = math.sqrt(x**2 + y**2 + z**2)
                nx, ny, nz = x/length, y/length, z/length
                
                # 조명 계산
                brightness = self.calculate_lighting(nx, ny, nz)
                
                # 투영 및 렌더링
                screen_x, screen_y, depth = self.project(x, y, z)
                self.set_pixel(screen_x, screen_y, depth, brightness)
    
    def draw_torus(self, angle_x, angle_y, angle_z, R=2, r=1, detail=40):
        """회전하는 도넛(토러스)을 그립니다"""
        for i in range(detail):
            for j in range(detail):
                theta = (i / detail) * 2 * math.pi
                phi = (j / detail) * 2 * math.pi
                
                # 토러스 방정식
                x = (R + r * math.cos(phi)) * math.cos(theta)
                y = (R + r * math.cos(phi)) * math.sin(theta)
                z = r * math.sin(phi)
                
                # 회전 적용
                x, y, z = self.rotate_x(x, y, z, angle_x)
                x, y, z = self.rotate_y(x, y, z, angle_y)
                x, y, z = self.rotate_z(x, y, z, angle_z)
                
                # 법선 벡터 계산
                circle_center_x = R * math.cos(theta)
                circle_center_y = R * math.sin(theta)
                circle_center_z = 0
                
                # 회전된 원의 중심
                cx, cy, cz = self.rotate_x(circle_center_x, circle_center_y, circle_center_z, angle_x)
                cx, cy, cz = self.rotate_y(cx, cy, cz, angle_y)
                cx, cy, cz = self.rotate_z(cx, cy, cz, angle_z)
                
                nx, ny, nz = x - cx, y - cy, z - cz
                length = math.sqrt(nx**2 + ny**2 + nz**2)
                if length > 0:
                    nx, ny, nz = nx/length, ny/length, nz/length
                
                # 조명 계산
                brightness = self.calculate_lighting(nx, ny, nz)
                
                # 투영 및 렌더링
                screen_x, screen_y, depth = self.project(x, y, z)
                self.set_pixel(screen_x, screen_y, depth, brightness)
    
    def draw_pyramid(self, angle_x, angle_y, angle_z, size=1.5):
        """회전하는 피라미드를 그립니다"""
        # 피라미드 정점
        vertices = [
            (0, size, 0),      # 꼭대기
            (-size, -size, -size),  # 밑면
            (size, -size, -size),
            (size, -size, size),
            (-size, -size, size)
        ]
        
        faces = [
            (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1),  # 측면
            (1, 2, 3), (1, 3, 4)  # 밑면
        ]
        
        # 회전된 정점 계산
        rotated_vertices = []
        for vx, vy, vz in vertices:
            vx, vy, vz = self.rotate_x(vx, vy, vz, angle_x)
            vx, vy, vz = self.rotate_y(vx, vy, vz, angle_y)
            vx, vy, vz = self.rotate_z(vx, vy, vz, angle_z)
            rotated_vertices.append((vx, vy, vz))
        
        # 각 면 그리기
        for face in faces:
            v1, v2, v3 = [rotated_vertices[i] for i in face]
            
            # 법선 벡터 계산 (외적)
            edge1 = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
            edge2 = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])
            
            nx = edge1[1] * edge2[2] - edge1[2] * edge2[1]
            ny = edge1[2] * edge2[0] - edge1[0] * edge2[2]
            nz = edge1[0] * edge2[1] - edge1[1] * edge2[0]
            
            length = math.sqrt(nx**2 + ny**2 + nz**2)
            if length > 0:
                nx, ny, nz = nx/length, ny/length, nz/length
                
                brightness = self.calculate_lighting(nx, ny, nz)
                self._fill_triangle(v1, v2, v3, brightness)
    
    def _fill_triangle(self, v1, v2, v3, brightness):
        """삼각형을 채웁니다"""
        # 스캔라인 알고리즘으로 삼각형 채우기
        points = [v1, v2, v3]
        for point in points:
            screen_x, screen_y, depth = self.project(*point)
            # 간단한 점 렌더링
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    self.set_pixel(screen_x + dx, screen_y + dy, depth, brightness)
    
    def _fill_quad(self, v1, v2, v3, v4, brightness):
        """사각형을 채웁니다"""
        # 사각형을 두 개의 삼각형으로 분할
        self._fill_triangle(v1, v2, v3, brightness)
        self._fill_triangle(v1, v3, v4, brightness)


def animate_cube(duration=float('inf'), fps=30, speed=1.0):
    """큐브 애니메이션"""
    renderer = ASCII3DRenderer(width=80, height=40)
    frame = 0
    
    print("\033[?25l")  # 커서 숨기기
    
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            renderer.clear()
            
            angle = frame * 0.05 * speed
            renderer.draw_cube(angle, angle * 0.7, angle * 0.5)
            
            print("\033[2J\033[H", end="")
            print("Rotating Cube (Press Ctrl+C to stop)")
            print(renderer.render())
            
            time.sleep(1 / fps)
            frame += 1
    finally:
        print("\033[?25h")  # 커서 표시


def animate_sphere(duration=float('inf'), fps=30, speed=1.0):
    """구 애니메이션"""
    renderer = ASCII3DRenderer(width=80, height=40)
    frame = 0
    
    print("\033[?25l")
    
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            renderer.clear()
            
            angle_x = frame * 0.03 * speed
            angle_y = frame * 0.05 * speed
            renderer.draw_sphere(angle_x, angle_y)
            
            print("\033[2J\033[H", end="")
            print("Rotating Sphere (Press Ctrl+C to stop)")
            print(renderer.render())
            
            time.sleep(1 / fps)
            frame += 1
    finally:
        print("\033[?25h")


def animate_torus(duration=float('inf'), fps=30, speed=1.0):
    """도넛 애니메이션"""
    renderer = ASCII3DRenderer(width=80, height=40)
    frame = 0
    
    print("\033[?25l")
    
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            renderer.clear()
            
            angle_x = frame * 0.05 * speed
            angle_y = frame * 0.03 * speed
            angle_z = frame * 0.07 * speed
            renderer.draw_torus(angle_x, angle_y, angle_z)
            
            print("\033[2J\033[H", end="")
            print("Rotating Donut (Press Ctrl+C to stop)")
            print(renderer.render())
            
            time.sleep(1 / fps)
            frame += 1
    finally:
        print("\033[?25h")


def animate_pyramid(duration=float('inf'), fps=30, speed=1.0):
    """피라미드 애니메이션"""
    renderer = ASCII3DRenderer(width=80, height=40)
    frame = 0
    
    print("\033[?25l")
    
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            renderer.clear()
            
            angle = frame * 0.05 * speed
            renderer.draw_pyramid(angle, angle * 0.7, angle * 0.5)
            
            print("\033[2J\033[H", end="")
            print("Rotating Pyramid (Press Ctrl+C to stop)")
            print(renderer.render())
            
            time.sleep(1 / fps)
            frame += 1
    finally:
        print("\033[?25h")


def animate_mixed(duration=float('inf'), fps=30, speed=1.0):
    """여러 객체 동시 애니메이션"""
    renderer = ASCII3DRenderer(width=120, height=40)
    frame = 0
    
    print("\033[?25l")
    
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            renderer.clear()
            
            angle = frame * 0.05 * speed
            
            # 세 개의 객체를 다른 위치에 렌더링
            # 큐브 (왼쪽)
            saved_width = renderer.width
            renderer.width = 40
            renderer.draw_cube(angle, angle * 0.7, angle * 0.5, size=1.0)
            
            # 도넛 (중앙)
            renderer.width = 80
            renderer.draw_torus(angle, angle * 0.5, angle * 0.8, R=1.5, r=0.7)
            
            # 구 (오른쪽)
            renderer.width = saved_width
            renderer.draw_sphere(angle * 0.8, angle, radius=1.0)
            
            print("\033[2J\033[H", end="")
            print("Mixed 3D Objects (Press Ctrl+C to stop)")
            print(renderer.render())
            
            time.sleep(1 / fps)
            frame += 1
    finally:
        print("\033[?25h")


def main():
    parser = argparse.ArgumentParser(
        description="3D ASCII Art - Real-time rotating 3D objects"
    )
    
    parser.add_argument(
        "shape",
        choices=["cube", "sphere", "torus", "pyramid", "mixed"],
        help="3D 객체 타입"
    )
    
    parser.add_argument(
        "-d", "--duration",
        type=float,
        default=float('inf'),
        help="애니메이션 지속 시간 (초, 기본값: 무한)"
    )
    
    parser.add_argument(
        "-f", "--fps",
        type=int,
        default=30,
        help="프레임레이트 (기본값: 30)"
    )
    
    parser.add_argument(
        "-s", "--speed",
        type=float,
        default=1.0,
        help="회전 속도 (기본값: 1.0)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.shape == "cube":
            animate_cube(args.duration, args.fps, args.speed)
        elif args.shape == "sphere":
            animate_sphere(args.duration, args.fps, args.speed)
        elif args.shape == "torus":
            animate_torus(args.duration, args.fps, args.speed)
        elif args.shape == "pyramid":
            animate_pyramid(args.duration, args.fps, args.speed)
        elif args.shape == "mixed":
            animate_mixed(args.duration, args.fps, args.speed)
    except KeyboardInterrupt:
        print("\n\nAnimation stopped")


if __name__ == "__main__":
    main()

