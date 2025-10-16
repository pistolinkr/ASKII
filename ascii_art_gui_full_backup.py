#!/usr/bin/env python3
"""
ASCII Art GUI Application - Full Version
GUI interface for generating ASCII art and converting images/videos
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, colorchooser
import math
import threading
import time
import os
from ascii_art import AsciiArtRenderer
from ascii_converter import AsciiConverter
from ascii_3d import ASCII3DRenderer
from ascii_exporter import AsciiExporter
import cv2
from PIL import Image, ImageTk
import numpy as np
# Completely disable darkdetect for macOS compatibility
DARKDETECT_AVAILABLE = False


class AsciiArtGUIFull:
    """ASCII Art와 이미지/비디오 변환을 지원하는 GUI 애플리케이션"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Studio")
        self.root.geometry("1100x750")
        
        # Theme colors
        self.themes = {
            "Light": {
                "bg": "#f5f5f7",
                "fg": "#1d1d1f",
                "panel_bg": "#ffffff",
                "display_bg": "#1d1d1f",
                "display_fg": "#f5f5f7",
                "button_bg": "#007aff",
                "button_fg": "#ffffff",
                "secondary_fg": "#6d6d70",
                "input_bg": "#ffffff",
                "accent_green": "#34c759",
                "accent_red": "#ff3b30",
                "accent_gray": "#e5e5ea",
                "accent_gray_dark": "#8e8e93",
                "border": "#d1d1d6",
                "accent_blue": "#007aff",
                "section_bg": "#f5f5f7",
                "slider_track": "#e5e5ea",
                "slider_handle": "#007aff"
            },
            "Dark": {
                "bg": "#1d1d1f",
                "fg": "#f5f5f7",
                "panel_bg": "#2c2c2e",
                "display_bg": "#000000",
                "display_fg": "#00ff00",
                "button_bg": "#0a84ff",
                "button_fg": "#ffffff",
                "secondary_fg": "#98989d",
                "input_bg": "#3a3a3c",
                "accent_green": "#30d158",
                "accent_red": "#ff453a",
                "accent_gray": "#636366",
                "accent_gray_dark": "#48484a",
                "border": "#38383a",
                "accent_blue": "#0a84ff",
                "section_bg": "#2c2c2e",
                "slider_track": "#48484a",
                "slider_handle": "#0a84ff"
            },
            "System": {
                "bg": "#f5f5f7",
                "fg": "#1d1d1f",
                "panel_bg": "#ffffff",
                "display_bg": "#1d1d1f",
                "display_fg": "#f5f5f7",
                "button_bg": "#007aff",
                "button_fg": "#ffffff",
                "secondary_fg": "#6d6d70",
                "input_bg": "#ffffff",
                "accent_green": "#34c759",
                "accent_red": "#ff3b30",
                "accent_gray": "#e5e5ea",
                "accent_gray_dark": "#8e8e93",
                "border": "#d1d1d6",
                "accent_blue": "#007aff",
                "section_bg": "#f5f5f7",
                "slider_track": "#e5e5ea",
                "slider_handle": "#007aff"
            }
        }
        
        # Detect system theme
        # Always use Light theme for macOS compatibility
        self.current_theme = "Light"
        self.last_detected_theme = None
        self.apply_theme()
        
        self.renderer = AsciiArtRenderer()
        self.renderer_3d = ASCII3DRenderer(width=80, height=35)
        self.exporter = AsciiExporter(font_size=10, bg_color=(0, 0, 0), fg_color=(0, 255, 0))
        self.animation_running = False
        self.animation_thread = None
        self.video_playing = False
        self.video_thread = None
        self.current_image_path = None
        self.current_video_path = None
        self.render_3d_running = False
        self.render_3d_thread = None
        
        # Custom colors and aspect ratio settings
        self.custom_fg_color = None  # RGB tuple
        self.custom_bg_color = None  # RGB tuple
        self.aspect_ratio_width = 2.0  # Default aspect ratio (width:height)
        self.aspect_ratio_height = 1.0
        self.ratio_selector = None
        self.selected_ratio = None
        self.vid_aspect_width_var = None
        self.vid_aspect_height_var = None
        
        # Spacing variables
        self.letter_spacing = 1  # 자간
        self.line_spacing = 1    # 행간
        self.font_size_multiplier = 1  # 폰트 크기 배율
        
        # Depth rendering variables
        self.use_depth_rendering = True  # 깊이 기반 렌더링 사용 여부
        self.use_edge_detection = True   # 경계선 감지 사용 여부
        
        # Text enhancement variables
        self.text_enhancement = True     # 텍스트 가독성 향상 사용 여부
        self.use_anti_aliasing = True    # 안티앨리어싱 사용 여부
        self.text_outline = True         # 텍스트 외곽선 사용 여부
        self.contrast_boost = 1.5        # 대비 강화 배율
        
        self.setup_ui()
        
        # Start system theme monitoring
        self.start_theme_monitoring()
    
    def detect_system_theme(self):
        """시스템 테마를 감지합니다"""
        # Always return Light theme for macOS compatibility
        return "Light"
    
    def start_theme_monitoring(self):
        """시스템 테마 변화를 모니터링합니다"""
        # Theme monitoring disabled for macOS compatibility
        pass
    
    def check_theme_change(self):
        """시스템 테마 변화를 확인하고 필요시 UI를 업데이트합니다"""
        # Theme change checking disabled for macOS compatibility
        pass
    
    def rebuild_ui(self):
        """UI를 재구성합니다"""
        # 현재 UI를 파괴하고 재생성
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.apply_theme()
        
        # UI 재설정
        theme = self.themes[self.current_theme]
        
        # Header frame
        header_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="ASCII Art Studio",
            font=("SF Pro Display", 28, "bold"),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        title_label.pack(side=tk.LEFT)
        
        # Theme selector
        theme_frame = tk.Frame(header_frame, bg=theme["bg"])
        theme_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            theme_frame,
            text="Theme:",
            font=("SF Pro Text", 12),
            bg=theme["bg"],
            fg=theme["fg"]
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        
        # Only Light and Dark themes for macOS compatibility
        theme_options = ["Light", "Dark"]
        for option in theme_options:
            rb = tk.Radiobutton(
                theme_frame,
                text=option,
                variable=self.theme_var,
                value=option,
                command=self.change_theme,
                bg=theme["bg"],
                fg=theme["fg"],
                font=("SF Pro Text", 11),
                activebackground=theme["bg"],
                selectcolor=theme["button_bg"],
                bd=0,
                highlightthickness=0,
                padx=8,
                pady=4
            )
            rb.pack(side=tk.LEFT, padx=2)
        
        # Notebook for tabs
        self.setup_notebook_style()
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_generator_tab()
        self.create_image_tab()
        self.create_video_tab()
        self.create_3d_tab()
    
    def apply_theme(self):
        """현재 테마를 적용합니다"""
        # If System theme is selected, detect actual system theme
        theme = self.themes[self.current_theme]
        
        self.root.configure(bg=theme["bg"])
    
    def setup_notebook_style(self):
        """노트북 스타일을 설정합니다"""
        theme = self.themes[self.current_theme]
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=theme["bg"], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10], 
                       font=("SF Pro Text", 13),
                       background=theme["panel_bg"],
                       foreground=theme["fg"])
        style.map('TNotebook.Tab',
                 background=[('selected', theme["button_bg"])],
                 foreground=[('selected', theme["button_fg"])])
    
    def change_theme(self):
        """테마를 변경합니다"""
        self.current_theme = self.theme_var.get()
        
        # System theme is not supported for macOS compatibility
        
        # UI 재구성
        self.rebuild_ui()
    
    def setup_ui(self):
        """UI 컴포넌트를 설정합니다"""
        theme = self.themes[self.current_theme]
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg=theme["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header frame
        header_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="ASCII Art Studio",
            font=("SF Pro Display", 28, "bold"),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        title_label.pack(side=tk.LEFT)
        
        # Theme selector
        theme_frame = tk.Frame(header_frame, bg=theme["bg"])
        theme_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            theme_frame,
            text="Theme:",
            font=("SF Pro Text", 12),
            bg=theme["bg"],
            fg=theme["fg"]
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        
        # Only Light and Dark themes for macOS compatibility
        theme_options = ["Light", "Dark"]
        for option in theme_options:
            rb = tk.Radiobutton(
                theme_frame,
                text=option,
                variable=self.theme_var,
                value=option,
                command=self.change_theme,
                bg=theme["bg"],
                fg=theme["fg"],
                font=("SF Pro Text", 11),
                activebackground=theme["bg"],
                selectcolor=theme["button_bg"],
                bd=0,
                highlightthickness=0,
                padx=8,
                pady=4
            )
            rb.pack(side=tk.LEFT, padx=2)
        
        # Notebook for tabs
        self.setup_notebook_style()
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_generator_tab()
        self.create_image_tab()
        self.create_video_tab()
        self.create_3d_tab()
    
    def create_ratio_selector(self, parent, theme):
        """소셜미디어 스타일의 그리드 기반 비율 선택기를 생성합니다"""
        # Predefined ratio options (width:height)
        ratios = [
            (1, 1),   # Square
            (4, 3),   # Classic
            (3, 2),   # 3:2
            (16, 9),  # Widescreen
            (9, 16),  # Vertical (Stories)
            (2, 1),   # 2:1
            (1, 2),   # 1:2
            (3, 4),   # Portrait
        ]
        
        # Create main container
        selector_frame = tk.Frame(parent, bg=theme["bg"])
        selector_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Grid container
        grid_frame = tk.Frame(selector_frame, bg=theme["bg"])
        grid_frame.pack()
        
        # Create grid buttons
        self.ratio_buttons = []
        for i, (w, h) in enumerate(ratios):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                grid_frame,
                text=f"{w}:{h}",
                width=6,
                height=2,
                font=("SF Pro Text", 9),
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                bd=1,
                relief="solid",
                command=lambda w=w, h=h: self.select_ratio(w, h)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.ratio_buttons.append((btn, w, h))
        
        # Current selection display
        self.ratio_display = tk.Label(
            selector_frame,
            text="Selected: 2:1",
            font=("SF Pro Text", 10, "bold"),
            bg=theme["bg"],
            fg=theme["accent_blue"]
        )
        self.ratio_display.pack(pady=(5, 0))
        
        # Set default selection (2:1)
        self.select_ratio(2, 1)
    
    def select_ratio(self, width, height):
        """비율을 선택하고 UI를 업데이트합니다"""
        self.aspect_ratio_width = float(width)
        self.aspect_ratio_height = float(height)
        self.selected_ratio = (width, height)
        
        # Update button appearances
        for btn, w, h in self.ratio_buttons:
            if (w, h) == (width, height):
                btn.config(bg=self.themes[self.current_theme]["accent_blue"])
                btn.config(fg="white")
            else:
                btn.config(bg=self.themes[self.current_theme]["button_bg"])
                btn.config(fg=self.themes[self.current_theme]["button_fg"])
        
        # Update display
        self.ratio_display.config(text=f"Selected: {width}:{height}")
        
        # Trigger re-render if we have content
        if hasattr(self, 'current_image_path') and self.current_image_path:
            self.convert_image()
    
    def create_video_ratio_selector(self, parent, theme):
        """비디오용 그리드 기반 비율 선택기를 생성합니다"""
        # Initialize video aspect ratio variables
        self.vid_aspect_width_var = tk.StringVar(value="2")
        self.vid_aspect_height_var = tk.StringVar(value="1")
        
        # Predefined ratio options (width:height)
        ratios = [
            (1, 1),   # Square
            (4, 3),   # Classic
            (3, 2),   # 3:2
            (16, 9),  # Widescreen
            (9, 16),  # Vertical (Stories)
            (2, 1),   # 2:1
            (1, 2),   # 1:2
            (3, 4),   # Portrait
        ]
        
        # Create main container
        selector_frame = tk.Frame(parent, bg=theme["bg"])
        selector_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Grid container
        grid_frame = tk.Frame(selector_frame, bg=theme["bg"])
        grid_frame.pack()
        
        # Create grid buttons
        self.vid_ratio_buttons = []
        for i, (w, h) in enumerate(ratios):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                grid_frame,
                text=f"{w}:{h}",
                width=6,
                height=2,
                font=("SF Pro Text", 9),
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                bd=1,
                relief="solid",
                command=lambda w=w, h=h: self.select_video_ratio(w, h)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.vid_ratio_buttons.append((btn, w, h))
        
        # Current selection display
        self.vid_ratio_display = tk.Label(
            selector_frame,
            text="Selected: 2:1",
            font=("SF Pro Text", 10, "bold"),
            bg=theme["bg"],
            fg=theme["accent_blue"]
        )
        self.vid_ratio_display.pack(pady=(5, 0))
        
        # Set default selection (2:1)
        self.select_video_ratio(2, 1)
    
    def select_video_ratio(self, width, height):
        """비디오 비율을 선택하고 UI를 업데이트합니다"""
        # Update video aspect ratio variables
        if hasattr(self, 'vid_aspect_width_var'):
            self.vid_aspect_width_var.set(str(width))
        if hasattr(self, 'vid_aspect_height_var'):
            self.vid_aspect_height_var.set(str(height))
        
        # Update button appearances
        for btn, w, h in self.vid_ratio_buttons:
            if (w, h) == (width, height):
                btn.config(bg=self.themes[self.current_theme]["accent_blue"])
                btn.config(fg="white")
            else:
                btn.config(bg=self.themes[self.current_theme]["button_bg"])
                btn.config(fg=self.themes[self.current_theme]["button_fg"])
        
        # Update display
        self.vid_ratio_display.config(text=f"Selected: {width}:{height}")
    
    def create_generator_tab(self):
        """생성기 탭을 생성합니다"""
        theme = self.themes[self.current_theme]
        
        tab = tk.Frame(self.notebook, bg=theme["panel_bg"])
        self.notebook.add(tab, text="Generate Art")
        
        # Split into left and right panels
        left_frame = tk.Frame(tab, bg=theme["panel_bg"], width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
        left_frame.pack_propagate(False)
        
        right_frame = tk.Frame(tab, bg=theme["display_bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=15)
        
        # Left panel - Controls
        self.create_section_label(left_frame, "Art Type")
        
        self.art_type = tk.StringVar(value="banner")
        art_types = [
            ("Banner", "banner"),
            ("Wave", "wave"),
            ("Circle", "circle"),
            ("Spiral", "spiral"),
            ("Heart", "heart"),
            ("Box", "box")
        ]
        
        for text, value in art_types:
            rb = tk.Radiobutton(
                left_frame,
                text=text,
                variable=self.art_type,
                value=value,
                command=self.on_type_change,
                bg=theme["panel_bg"],
                fg=theme["fg"],
                font=("SF Pro Text", 12),
                activebackground=theme["panel_bg"],
                selectcolor=theme["button_bg"]
            )
            rb.pack(anchor=tk.W, padx=20, pady=2)
        
        # Parameters
        self.create_section_label(left_frame, "Parameters", top_margin=20)
        
        # Text input
        self.text_label = tk.Label(
            left_frame,
            text="Text:",
            font=("SF Pro Text", 12),
            bg=theme["panel_bg"],
            fg=theme["fg"]
        )
        self.text_label.pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        self.text_entry = tk.Entry(
            left_frame,
            font=("SF Pro Text", 11),
            bg=theme["input_bg"],
            fg=theme["fg"],
            relief=tk.FLAT,
            insertbackground=theme["fg"]
        )
        self.text_entry.insert(0, "Hello, World!")
        self.text_entry.pack(fill=tk.X, padx=20, pady=(0, 10), ipady=5)
        self.text_entry.bind("<KeyRelease>", lambda e: self.render_art())
        
        # Sliders
        self.create_slider(left_frame, "Width:", 20, 100, 60, "gen_width")
        self.create_slider(left_frame, "Size:", 5, 30, 10, "gen_size")
        
        # Spacing controls
        self.create_section_label(left_frame, "Spacing", top_margin=20)
        self.create_slider(left_frame, "Letter Spacing:", 1, 5, 1, "letter_spacing")
        self.create_slider(left_frame, "Line Spacing:", 1, 5, 1, "line_spacing")
        self.create_slider(left_frame, "Font Size:", 1, 3, 1, "font_size")
        
        # Depth rendering controls
        self.create_section_label(left_frame, "Depth Rendering", top_margin=20)
        
        self.depth_rendering_var = tk.BooleanVar(value=True)
        self.depth_rendering_var.trace("w", self.on_depth_rendering_change)
        tk.Checkbutton(
            left_frame,
            text="Enable Depth Rendering",
            variable=self.depth_rendering_var,
            bg=theme["panel_bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 11),
            activebackground=theme["panel_bg"],
            selectcolor=theme["button_bg"],
            bd=0,
            highlightthickness=0
        ).pack(fill=tk.X, padx=20, pady=5)
        
        self.edge_detection_var = tk.BooleanVar(value=True)
        self.edge_detection_var.trace("w", self.on_edge_detection_change)
        tk.Checkbutton(
            left_frame,
            text="Enable Edge Detection",
            variable=self.edge_detection_var,
            bg=theme["panel_bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 11),
            activebackground=theme["panel_bg"],
            selectcolor=theme["button_bg"],
            bd=0,
            highlightthickness=0
        ).pack(fill=tk.X, padx=20, pady=5)
        
        # Text enhancement controls
        self.create_section_label(left_frame, "Text Enhancement", top_margin=20)
        
        self.text_enhancement_var = tk.BooleanVar(value=True)
        self.text_enhancement_var.trace("w", self.on_text_enhancement_change)
        tk.Checkbutton(
            left_frame,
            text="Enable Text Enhancement",
            variable=self.text_enhancement_var,
            bg=theme["panel_bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 11),
            activebackground=theme["panel_bg"],
            selectcolor=theme["button_bg"],
            bd=0,
            highlightthickness=0
        ).pack(fill=tk.X, padx=20, pady=5)
        
        self.text_outline_var = tk.BooleanVar(value=True)
        self.text_outline_var.trace("w", self.on_text_outline_change)
        tk.Checkbutton(
            left_frame,
            text="Enable Text Outline",
            variable=self.text_outline_var,
            bg=theme["panel_bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 11),
            activebackground=theme["panel_bg"],
            selectcolor=theme["button_bg"],
            bd=0,
            highlightthickness=0
        ).pack(fill=tk.X, padx=20, pady=5)
        
        self.anti_aliasing_var = tk.BooleanVar(value=True)
        self.anti_aliasing_var.trace("w", self.on_anti_aliasing_change)
        tk.Checkbutton(
            left_frame,
            text="Enable Anti-Aliasing",
            variable=self.anti_aliasing_var,
            bg=theme["panel_bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 11),
            activebackground=theme["panel_bg"],
            selectcolor=theme["button_bg"],
            bd=0,
            highlightthickness=0
        ).pack(fill=tk.X, padx=20, pady=5)
        
        # Character input
        tk.Label(
            left_frame,
            text="Character:",
            font=("SF Pro Text", 12),
            bg=theme["panel_bg"],
            fg=theme["fg"]
        ).pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        self.char_entry = tk.Entry(
            left_frame,
            font=("SF Pro Text", 11),
            bg=theme["input_bg"],
            fg=theme["fg"],
            relief=tk.FLAT,
            insertbackground=theme["fg"]
        )
        self.char_entry.insert(0, "*")
        self.char_entry.pack(fill=tk.X, padx=20, pady=(0, 10), ipady=5)
        self.char_entry.bind("<KeyRelease>", lambda e: self.render_art())
        
        # Animation controls
        self.create_section_label(left_frame, "Animation", top_margin=20)
        
        button_frame = tk.Frame(left_frame, bg=theme["panel_bg"])
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start",
            command=self.start_animation,
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=theme["button_bg"]
        )
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5), pady=5)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_animation,
            bg=theme["accent_gray_dark"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            activebackground=theme["accent_gray_dark"]
        )
        self.stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0), pady=5)
        
        self.create_slider(left_frame, "FPS:", 5, 30, 10, "gen_fps")
        
        # Right panel - Display
        self.gen_display = scrolledtext.ScrolledText(
            right_frame,
            font=("Courier", 9),
            bg=theme["display_bg"],
            fg=theme["display_fg"],
            relief=tk.FLAT,
            wrap=tk.NONE,
            padx=15,
            pady=15,
            insertbackground=theme["display_fg"]
        )
        self.gen_display.pack(fill=tk.BOTH, expand=True)
        
        # Initial render
        self.render_art()
    
    def create_image_tab(self):
        """이미지 변환 탭을 생성합니다"""
        theme = self.themes[self.current_theme]
        
        tab = tk.Frame(self.notebook, bg=theme["panel_bg"])
        self.notebook.add(tab, text="Image to ASCII")
        
        # Split into left and right panels
        left_frame = tk.Frame(tab, bg=theme["panel_bg"], width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
        left_frame.pack_propagate(False)
        
        right_frame = tk.Frame(tab, bg=theme["display_bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=15)
        
        # Left panel - Controls
        self.create_section_label(left_frame, "Image File")
        
        btn_frame = tk.Frame(left_frame, bg=theme["panel_bg"])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="Select Image",
            command=self.select_image,
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            activebackground=theme["button_bg"]
        ).pack(fill=tk.X)
        
        self.img_path_label = tk.Label(
            left_frame,
            text="No image selected",
            font=("SF Pro Text", 10),
            bg=theme["panel_bg"],
            fg=theme["secondary_fg"],
            wraplength=250
        )
        self.img_path_label.pack(padx=20, pady=(0, 10))
        
        # Conversion options
        self.create_section_label(left_frame, "Options", top_margin=20)
        
        # Width slider
        width_label = tk.Label(
            left_frame,
            text="Width",
            font=("SF Pro Text", 11),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        width_label.pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        width_frame = tk.Frame(left_frame, bg=theme["bg"])
        width_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.img_width_slider = tk.Scale(
            width_frame,
            from_=40,
            to=200,
            orient=tk.HORIZONTAL,
            bg=theme["bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 10),
            troughcolor=theme["input_bg"],
            relief=tk.FLAT,
            highlightthickness=0,
            activebackground=theme["button_bg"],
            command=self.on_image_setting_change
        )
        self.img_width_slider.set(80)
        self.img_width_slider.pack(fill=tk.X)
        
        # Aspect ratio controls with grid selector
        aspect_frame = tk.Frame(left_frame, bg=theme["bg"])
        aspect_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            aspect_frame,
            text="Aspect Ratio:",
            font=("SF Pro Text", 11),
            bg=theme["bg"],
            fg=theme["fg"]
        ).pack(anchor=tk.W)
        
        # Create grid-based ratio selector
        self.create_ratio_selector(aspect_frame, theme)
        
        # Color controls
        color_frame = tk.Frame(left_frame, bg=theme["bg"])
        color_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            color_frame,
            text="Colors:",
            font=("SF Pro Text", 11),
            bg=theme["bg"],
            fg=theme["fg"]
        ).pack(anchor=tk.W)
        
        # Foreground color button
        fg_color_frame = tk.Frame(color_frame, bg=theme["bg"])
        fg_color_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            fg_color_frame,
            text="Text:",
            font=("SF Pro Text", 10),
            bg=theme["bg"],
            fg=theme["fg"],
            width=8,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.fg_color_button = tk.Button(
            fg_color_frame,
            text="Choose",
            command=self.choose_fg_color,
            bg=theme["accent_gray"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 10),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=2,
            activebackground=theme["accent_gray"]
        )
        self.fg_color_button.pack(side=tk.LEFT, padx=(5, 0))
        
        self.fg_color_preview = tk.Label(
            fg_color_frame,
            text="●",
            font=("SF Pro Text", 16),
            bg=theme["bg"],
            fg="#00ff00"  # Default green
        )
        self.fg_color_preview.pack(side=tk.LEFT, padx=(10, 0))
        
        # Background color button
        bg_color_frame = tk.Frame(color_frame, bg=theme["bg"])
        bg_color_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            bg_color_frame,
            text="Background:",
            font=("SF Pro Text", 10),
            bg=theme["bg"],
            fg=theme["fg"],
            width=8,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.bg_color_button = tk.Button(
            bg_color_frame,
            text="Choose",
            command=self.choose_bg_color,
            bg=theme["accent_gray"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 10),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=2,
            activebackground=theme["accent_gray"]
        )
        self.bg_color_button.pack(side=tk.LEFT, padx=(5, 0))
        
        self.bg_color_preview = tk.Label(
            bg_color_frame,
            text="●",
            font=("SF Pro Text", 16),
            bg=theme["bg"],
            fg="#000000"  # Default black
        )
        self.bg_color_preview.pack(side=tk.LEFT, padx=(10, 0))
        
        self.img_detailed = tk.BooleanVar(value=True)
        self.img_detailed.trace("w", self.on_image_setting_change)
        tk.Checkbutton(
            left_frame,
            text="Detailed",
            variable=self.img_detailed,
            bg=theme["bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 11),
            activebackground=theme["bg"],
            selectcolor=theme["button_bg"],
            bd=0,
            highlightthickness=0
        ).pack(fill=tk.X, padx=20, pady=5)
        
        self.img_invert = tk.BooleanVar(value=False)
        self.img_invert.trace("w", self.on_image_setting_change)
        tk.Checkbutton(
            left_frame,
            text="Invert",
            variable=self.img_invert,
            bg=theme["bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 11),
            activebackground=theme["bg"],
            selectcolor=theme["button_bg"],
            bd=0,
            highlightthickness=0
        ).pack(fill=tk.X, padx=20, pady=5)
        
        # Convert button
        self.create_section_label(left_frame, "Convert", top_margin=20)
        
        tk.Button(
            left_frame,
            text="Convert to ASCII",
            command=self.convert_image,
            bg=theme["accent_green"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            activebackground=theme["accent_green"]
        ).pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            left_frame,
            text="Save as Text",
            command=self.save_ascii_image,
            bg=theme["accent_gray"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_gray"]
        ).pack(fill=tk.X, padx=20, pady=(0, 5))
        
        tk.Button(
            left_frame,
            text="Export as Image (PNG/JPG)",
            command=self.export_ascii_image,
            bg=theme["accent_gray"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_gray"]
        ).pack(fill=tk.X, padx=20, pady=(0, 5))
        
        # Screenshot export buttons
        tk.Button(
            left_frame,
            text="📸 Capture Display Area",
            command=self.capture_display_area,
            bg=theme["accent_green"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_green"]
        ).pack(fill=tk.X, padx=20, pady=(0, 5))
        
        tk.Button(
            left_frame,
            text="📷 Screenshot Full GUI",
            command=self.screenshot_full_gui,
            bg=theme["accent_blue"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_blue"]
        ).pack(fill=tk.X, padx=20)
        
        # Right panel - Display
        self.img_display = scrolledtext.ScrolledText(
            right_frame,
            font=("Courier", 7),
            bg=theme["display_bg"],
            fg=theme["display_fg"],
            relief=tk.FLAT,
            wrap=tk.NONE,
            padx=15,
            pady=15,
            insertbackground=theme["display_fg"]
        )
        self.img_display.pack(fill=tk.BOTH, expand=True)
        self.img_display.insert(1.0, "Select an image to convert to ASCII art")
    
    def create_video_tab(self):
        """비디오 변환 탭을 생성합니다"""
        theme = self.themes[self.current_theme]
        
        tab = tk.Frame(self.notebook, bg=theme["panel_bg"])
        self.notebook.add(tab, text="Video to ASCII")
        
        # Split into left and right panels
        left_frame = tk.Frame(tab, bg="#ffffff", width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
        left_frame.pack_propagate(False)
        
        right_frame = tk.Frame(tab, bg="#1d1d1f")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=15)
        
        # Left panel - Controls
        self.create_section_label(left_frame, "Video File")
        
        btn_frame = tk.Frame(left_frame, bg=theme["panel_bg"])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text="Select Video",
            command=self.select_video,
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            activebackground=theme["button_bg"]
        ).pack(fill=tk.X)
        
        self.vid_path_label = tk.Label(
            left_frame,
            text="No video selected",
            font=("SF Pro Text", 10),
            bg="#ffffff",
            fg="#8e8e93",
            wraplength=250
        )
        self.vid_path_label.pack(padx=20, pady=(0, 10))
        
        # Video info
        self.vid_info_label = tk.Label(
            left_frame,
            text="",
            font=("SF Pro Text", 10),
            bg="#ffffff",
            fg="#1d1d1f",
            justify=tk.LEFT
        )
        self.vid_info_label.pack(padx=20, pady=(0, 10))
        
        # Options
        self.create_section_label(left_frame, "Options", top_margin=20)
        
        # Width slider
        width_label = tk.Label(
            left_frame,
            text="Width",
            font=("SF Pro Text", 11),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        width_label.pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        width_frame = tk.Frame(left_frame, bg=theme["bg"])
        width_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.vid_width_slider = tk.Scale(
            width_frame,
            from_=40,
            to=120,
            orient=tk.HORIZONTAL,
            bg=theme["bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 10),
            troughcolor=theme["input_bg"],
            relief=tk.FLAT,
            highlightthickness=0,
            activebackground=theme["button_bg"],
            command=self.on_video_setting_change
        )
        self.vid_width_slider.set(80)
        self.vid_width_slider.pack(fill=tk.X)
        
        # FPS slider
        fps_label = tk.Label(
            left_frame,
            text="FPS",
            font=("SF Pro Text", 11),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        fps_label.pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        fps_frame = tk.Frame(left_frame, bg=theme["bg"])
        fps_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.vid_fps_slider = tk.Scale(
            fps_frame,
            from_=5,
            to=30,
            orient=tk.HORIZONTAL,
            bg=theme["bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 10),
            troughcolor=theme["input_bg"],
            relief=tk.FLAT,
            highlightthickness=0,
            activebackground=theme["button_bg"],
            command=self.on_video_setting_change
        )
        self.vid_fps_slider.set(15)
        self.vid_fps_slider.pack(fill=tk.X)
        
        # Video aspect ratio controls with grid selector
        vid_aspect_frame = tk.Frame(left_frame, bg=theme["bg"])
        vid_aspect_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            vid_aspect_frame,
            text="Aspect Ratio:",
            font=("SF Pro Text", 11),
            bg=theme["bg"],
            fg=theme["fg"]
        ).pack(anchor=tk.W)
        
        # Create grid-based ratio selector for video
        self.create_video_ratio_selector(vid_aspect_frame, theme)
        
        self.vid_detailed = tk.BooleanVar(value=False)
        self.vid_detailed.trace("w", self.on_video_setting_change)
        tk.Checkbutton(
            left_frame,
            text="Detailed characters",
            variable=self.vid_detailed,
            bg="#ffffff",
            fg="#1d1d1f",
            font=("SF Pro Text", 12),
            activebackground="#ffffff",
            selectcolor="#007aff"
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        self.vid_invert = tk.BooleanVar(value=False)
        self.vid_invert.trace("w", self.on_video_setting_change)
        tk.Checkbutton(
            left_frame,
            text="Invert brightness",
            variable=self.vid_invert,
            bg="#ffffff",
            fg="#1d1d1f",
            font=("SF Pro Text", 12),
            activebackground="#ffffff",
            selectcolor="#007aff"
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        # Playback controls
        self.create_section_label(left_frame, "Playback", top_margin=20)
        
        btn_frame2 = tk.Frame(left_frame, bg=theme["panel_bg"])
        btn_frame2.pack(fill=tk.X, padx=20, pady=10)
        
        self.vid_play_btn = tk.Button(
            btn_frame2,
            text="Play",
            command=self.play_video,
            bg=theme["accent_green"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=theme["accent_green"]
        )
        self.vid_play_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5), pady=5)
        
        self.vid_stop_btn = tk.Button(
            btn_frame2,
            text="Stop",
            command=self.stop_video,
            bg=theme["accent_gray_dark"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            activebackground=theme["accent_gray_dark"]
        )
        self.vid_stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0), pady=5)
        
        # Export button
        tk.Button(
            left_frame,
            text="Export as Video (MP4/AVI/MOV)",
            command=self.export_video,
            bg=theme["accent_gray"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_gray"]
        ).pack(fill=tk.X, padx=20, pady=(10, 5))
        
        # Screenshot export buttons for video tab
        tk.Button(
            left_frame,
            text="📸 Capture Display Area",
            command=self.capture_display_area,
            bg=theme["accent_green"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_green"]
        ).pack(fill=tk.X, padx=20, pady=(0, 5))
        
        tk.Button(
            left_frame,
            text="📷 Screenshot Full GUI",
            command=self.screenshot_full_gui,
            bg=theme["accent_blue"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_blue"]
        ).pack(fill=tk.X, padx=20)
        
        # Right panel - Display
        self.vid_display = scrolledtext.ScrolledText(
            right_frame,
            font=("Courier", 6),
            bg="#1d1d1f",
            fg="#f5f5f7",
            relief=tk.FLAT,
            wrap=tk.NONE,
            padx=10,
            pady=10
        )
        self.vid_display.pack(fill=tk.BOTH, expand=True)
        self.vid_display.insert(1.0, "Select a video to convert to ASCII art")
    
    def create_section_label(self, parent, text, top_margin=0):
        """섹션 라벨을 생성합니다"""
        theme = self.themes[self.current_theme]
        label = tk.Label(
            parent,
            text=text,
            font=("SF Pro Display", 14, "bold"),
            bg=theme["section_bg"],
            fg=theme["fg"]
        )
        label.pack(anchor=tk.W, padx=20, pady=(top_margin, 10))
    
    def create_slider(self, parent, label_text, from_, to, default, attr_name):
        """슬라이더 컨트롤을 생성합니다"""
        theme = self.themes[self.current_theme]
        label = tk.Label(
            parent,
            text=label_text,
            font=("SF Pro Text", 12),
            bg=theme["panel_bg"],
            fg=theme["fg"]
        )
        label.pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        frame = tk.Frame(parent, bg=theme["panel_bg"])
        frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        slider = tk.Scale(
            frame,
            from_=from_,
            to=to,
            orient=tk.HORIZONTAL,
            bg=theme["panel_bg"],
            fg=theme["fg"],
            font=("SF Pro Text", 10),
            troughcolor=theme["slider_track"],
            relief=tk.FLAT,
            highlightthickness=0,
            activebackground=theme["slider_handle"],
            sliderlength=20,
            width=15
        )
        slider.set(default)
        slider.pack(fill=tk.X)
        
        # Spacing sliders에 대한 콜백 추가
        if attr_name in ["letter_spacing", "line_spacing", "font_size"]:
            slider.config(command=lambda v: self.on_spacing_change(attr_name, int(v)))
        
        setattr(self, f"{attr_name}_slider", slider)
    
    def on_spacing_change(self, attr_name, value):
        """Spacing 설정이 변경될 때 호출됩니다"""
        if attr_name == "letter_spacing":
            self.letter_spacing = value
        elif attr_name == "line_spacing":
            self.line_spacing = value
        elif attr_name == "font_size":
            self.font_size_multiplier = value
        
        # Renderer에 새로운 spacing 설정 적용
        self.renderer.set_spacing(self.letter_spacing, self.line_spacing)
        self.renderer.set_font_size(self.font_size_multiplier)
        
        # ASCII 아트 다시 렌더링
        self.render_art()
    
    def on_depth_rendering_change(self, *args):
        """깊이 렌더링 설정이 변경될 때 호출됩니다"""
        self.use_depth_rendering = self.depth_rendering_var.get()
        self.renderer.use_depth_rendering = self.use_depth_rendering
        self.render_art()
    
    def on_edge_detection_change(self, *args):
        """경계선 감지 설정이 변경될 때 호출됩니다"""
        self.use_edge_detection = self.edge_detection_var.get()
        self.renderer.use_edge_detection = self.use_edge_detection
        self.render_art()
    
    def on_text_enhancement_change(self, *args):
        """텍스트 향상 설정이 변경될 때 호출됩니다"""
        self.text_enhancement = self.text_enhancement_var.get()
        self.renderer.text_enhancement = self.text_enhancement
        self.render_art()
    
    def on_text_outline_change(self, *args):
        """텍스트 외곽선 설정이 변경될 때 호출됩니다"""
        self.text_outline = self.text_outline_var.get()
        self.renderer.text_outline = self.text_outline
        self.render_art()
    
    def on_anti_aliasing_change(self, *args):
        """안티앨리어싱 설정이 변경될 때 호출됩니다"""
        self.use_anti_aliasing = self.anti_aliasing_var.get()
        self.renderer.use_anti_aliasing = self.use_anti_aliasing
        self.render_art()
    
    # Generator Tab Methods
    def on_type_change(self):
        """아트 타입 변경 시"""
        art_type = self.art_type.get()
        if art_type in ["banner", "box"]:
            self.text_label.pack(anchor=tk.W, padx=20, pady=(5, 2))
            self.text_entry.pack(fill=tk.X, padx=20, pady=(0, 10), ipady=5)
        else:
            self.text_label.pack_forget()
            self.text_entry.pack_forget()
        self.render_art()
    
    def render_art(self):
        """ASCII 아트를 렌더링합니다"""
        if self.animation_running:
            return
        
        art_type = self.art_type.get()
        width = int(self.gen_width_slider.get())
        size = int(self.gen_size_slider.get())
        text = self.text_entry.get()
        char = self.char_entry.get()[:1] or "*"
        
        try:
            if art_type == "banner":
                art = self.renderer.text_banner(text, width, char)
            elif art_type == "wave":
                art = self.renderer.wave(width=width, height=size)
            elif art_type == "circle":
                art = self.renderer.circle(radius=size, char=char)
            elif art_type == "spiral":
                art = self.renderer.spiral(size=size)
            elif art_type == "heart":
                art = self.renderer.heart(size=size)
            elif art_type == "box":
                art = self.renderer.box_text(text, padding=2, char=char)
            else:
                art = "Unknown art type"
            
            self.gen_display.delete(1.0, tk.END)
            self.gen_display.insert(1.0, art)
        except Exception as e:
            self.gen_display.delete(1.0, tk.END)
            self.gen_display.insert(1.0, f"Error: {str(e)}")
    
    def start_animation(self):
        """애니메이션을 시작합니다"""
        if self.animation_running:
            return
        
        self.animation_running = True
        self.start_btn.config(state=tk.DISABLED, bg="#636366")
        self.stop_btn.config(state=tk.NORMAL, bg="#007aff")
        
        art_type = self.art_type.get()
        self.animation_thread = threading.Thread(
            target=self.animate,
            args=(art_type,),
            daemon=True
        )
        self.animation_thread.start()
    
    def stop_animation(self):
        """애니메이션을 중지합니다"""
        self.animation_running = False
        self.start_btn.config(state=tk.NORMAL, bg="#007aff")
        self.stop_btn.config(state=tk.DISABLED, bg="#8e8e93")
        self.render_art()
    
    def animate(self, art_type):
        """애니메이션을 실행합니다"""
        fps = int(self.gen_fps_slider.get())
        frame = 0
        
        while self.animation_running:
            try:
                width = int(self.gen_width_slider.get())
                size = int(self.gen_size_slider.get())
                
                if art_type == "wave":
                    phase = (frame / fps) * 2 * math.pi
                    art = self.renderer.wave(width=width, height=size, phase=phase)
                elif art_type == "spiral":
                    rotation = (frame / fps) * math.pi / 2
                    art = self.renderer.spiral(size=size, rotation=rotation)
                else:
                    self.root.after(0, self.render_art)
                    time.sleep(1 / fps)
                    frame += 1
                    continue
                
                self.root.after(0, self.update_display, self.gen_display, art)
                time.sleep(1 / fps)
                frame += 1
            except Exception as e:
                print(f"Animation error: {e}")
                break
    
    # Image Tab Methods
    def select_image(self):
        """이미지 파일을 선택합니다"""
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.current_image_path = filename
            theme = self.themes[self.current_theme]
            if self.current_theme == "System":
                actual_theme = self.detect_system_theme()
                theme = self.themes[actual_theme]
            else:
                theme = self.themes[self.current_theme]
            self.img_path_label.config(
                text=os.path.basename(filename),
                fg=theme["fg"]
            )
    
    def convert_image(self):
        """이미지를 ASCII로 변환합니다"""
        if not self.current_image_path:
            messagebox.showwarning("No Image", "Please select an image first")
            return
        
        try:
            width = int(self.img_width_slider.get())
            detailed = self.img_detailed.get()
            invert = self.img_invert.get()
            
            # Get aspect ratio
            try:
                aspect_w = float(self.aspect_width_var.get())
                aspect_h = float(self.aspect_height_var.get())
                if aspect_h == 0:
                    aspect_h = 1.0
                aspect_ratio = aspect_w / aspect_h
            except (ValueError, AttributeError):
                aspect_ratio = 2.0  # Default aspect ratio
            
            converter = AsciiConverter(width=width, detailed=detailed, invert=invert, aspect_ratio=aspect_ratio)
            ascii_art = converter.image_to_ascii(self.current_image_path)
            
            self.img_display.delete(1.0, tk.END)
            self.img_display.insert(1.0, ascii_art)
            
            # Apply colors - custom colors take priority
            if self.current_theme == "System":
                actual_theme = self.detect_system_theme()
                theme = self.themes[actual_theme]
            else:
                theme = self.themes[self.current_theme]
            
            # Set default theme colors first
            fg_color = theme["display_fg"]
            bg_color = theme["display_bg"]
            
            # Override with custom colors if set
            if self.custom_fg_color:
                fg_color = f"#{self.custom_fg_color[0]:02x}{self.custom_fg_color[1]:02x}{self.custom_fg_color[2]:02x}"
            
            if self.custom_bg_color:
                bg_color = f"#{self.custom_bg_color[0]:02x}{self.custom_bg_color[1]:02x}{self.custom_bg_color[2]:02x}"
            
            # Apply colors to the text widget
            self.img_display.config(fg=fg_color, bg=bg_color)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image: {str(e)}")
    
    def save_ascii_image(self):
        """ASCII 이미지를 텍스트 파일로 저장합니다"""
        content = self.img_display.get(1.0, tk.END).strip()
        
        if not content or content == "Select an image to convert to ASCII art":
            messagebox.showwarning("No Content", "No ASCII art to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save ASCII Art as Text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"ASCII art saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def export_ascii_image(self):
        """ASCII 이미지를 이미지 파일로 내보냅니다"""
        content = self.img_display.get(1.0, tk.END).strip()
        
        if not content or content == "Select an image to convert to ASCII art":
            messagebox.showwarning("No Content", "No ASCII art to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export ASCII Art as Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                # Use user-defined colors instead of theme colors
                bg_color = self.custom_bg_color if self.custom_bg_color else (0, 0, 0)
                fg_color = self.custom_fg_color if self.custom_fg_color else (255, 255, 255)
                
                # Calculate image dimensions with user-defined aspect ratio
                lines = content.split('\n')
                if not lines:
                    messagebox.showerror("Error", "No ASCII art content to export!")
                    return
                
                # Remove empty lines and get actual content dimensions
                non_empty_lines = [line for line in lines if line.strip()]
                if not non_empty_lines:
                    messagebox.showerror("Error", "No valid ASCII art content to export!")
                    return
                
                # Find the actual content width (trim trailing spaces)
                max_width = max(len(line.rstrip()) for line in non_empty_lines)
                height = len(non_empty_lines)
                
                # Font size settings
                font_size = 12
                char_width = font_size * 0.6
                char_height = font_size * 1.2
                
                # Calculate base dimensions without aspect ratio
                base_width = max_width * char_width
                base_height = height * char_height
                
                # Apply user-defined aspect ratio to maintain proportions
                aspect_ratio = self.aspect_ratio_width / self.aspect_ratio_height
                
                # Adjust dimensions to maintain aspect ratio while fitting content
                if base_width / base_height > aspect_ratio:
                    # Content is wider than desired aspect ratio
                    img_width = int(base_width)
                    img_height = int(base_width / aspect_ratio)
                else:
                    # Content is taller than desired aspect ratio
                    img_width = int(base_height * aspect_ratio)
                    img_height = int(base_height)
                
                # Ensure minimum size but don't add unnecessary padding
                img_width = max(img_width, int(max_width * char_width))
                img_height = max(img_height, int(height * char_height))
                
                # Create image with PIL
                from PIL import Image, ImageDraw, ImageFont
                img = Image.new('RGB', (img_width, img_height), color=bg_color)
                draw = ImageDraw.Draw(img)
                
                # Try to use system font
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
                
                # Draw text with user-defined colors
                y_offset = 0
                for line in non_empty_lines:
                    # Trim trailing spaces to avoid unnecessary padding
                    trimmed_line = line.rstrip()
                    if trimmed_line:  # Only draw lines with content
                        draw.text((0, y_offset), trimmed_line, font=font, fill=fg_color)
                    y_offset += char_height
                
                # Save image
                img.save(filename)
                messagebox.showinfo("Success", f"ASCII art exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def capture_display_area(self):
        """ASCII 아트 디스플레이 영역을 캡처합니다"""
        try:
            import tkinter as tk
            from PIL import ImageGrab
            import time
            
            # 잠시 대기하여 UI가 안정화되도록 함
            time.sleep(0.5)
            
            # 디스플레이 영역의 좌표 계산
            display_widget = self.img_display
            x = self.root.winfo_rootx() + display_widget.winfo_x()
            y = self.root.winfo_rooty() + display_widget.winfo_y()
            width = display_widget.winfo_width()
            height = display_widget.winfo_height()
            
            # 화면 영역이 유효한지 확인
            if width <= 1 or height <= 1:
                messagebox.showerror("Error", "Display area is too small to capture!")
                return
            
            # 파일 저장 경로 선택
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save Display Area Screenshot"
            )
            
            if file_path:
                # 디스플레이 영역 캡처
                screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                screenshot.save(file_path)
                messagebox.showinfo("Success", f"Display area captured and saved to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture display area: {str(e)}")
    
    def screenshot_full_gui(self):
        """전체 GUI 창을 스크린샷합니다"""
        try:
            import tkinter as tk
            from PIL import ImageGrab
            import time
            
            # 잠시 대기하여 UI가 안정화되도록 함
            time.sleep(0.5)
            
            # GUI 창의 좌표 계산
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            # 창 크기가 유효한지 확인
            if width <= 1 or height <= 1:
                messagebox.showerror("Error", "GUI window is too small to capture!")
                return
            
            # 파일 저장 경로 선택
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save GUI Screenshot"
            )
            
            if file_path:
                # 전체 GUI 창 캡처
                screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                screenshot.save(file_path)
                messagebox.showinfo("Success", f"GUI screenshot saved to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture GUI screenshot: {str(e)}")
    
    def capture_3d_display_area(self):
        """3D 디스플레이 영역을 캡처합니다"""
        try:
            import tkinter as tk
            from PIL import ImageGrab
            import time
            
            # 잠시 대기하여 UI가 안정화되도록 함
            time.sleep(0.5)
            
            # 3D 디스플레이 영역의 좌표 계산
            display_widget = self.display_3d
            x = self.root.winfo_rootx() + display_widget.winfo_x()
            y = self.root.winfo_rooty() + display_widget.winfo_y()
            width = display_widget.winfo_width()
            height = display_widget.winfo_height()
            
            # 화면 영역이 유효한지 확인
            if width <= 1 or height <= 1:
                messagebox.showerror("Error", "3D display area is too small to capture!")
                return
            
            # 파일 저장 경로 선택
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save 3D Display Area Screenshot"
            )
            
            if file_path:
                # 3D 디스플레이 영역 캡처
                screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                screenshot.save(file_path)
                messagebox.showinfo("Success", f"3D display area captured and saved to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture 3D display area: {str(e)}")
    
    def choose_fg_color(self):
        """텍스트 색상을 선택합니다"""
        try:
            # Try to import colorchooser
            try:
                from tkinter import colorchooser
                color = colorchooser.askcolor(
                    title="Choose Text Color",
                    color="#00ff00" if not self.custom_fg_color else 
                          f"#{self.custom_fg_color[0]:02x}{self.custom_fg_color[1]:02x}{self.custom_fg_color[2]:02x}"
                )
            except Exception as e:
                # Fallback: show a simple color input dialog
                messagebox.showinfo("Color Chooser", "Color chooser not available. Using default green.")
                color = ((0, 255, 0), "#00ff00")  # Default green
            
            if color[0]:  # color[0] is RGB tuple
                self.custom_fg_color = tuple(int(c) for c in color[0])
                # Update preview
                hex_color = color[1]  # color[1] is hex string
                self.fg_color_preview.config(fg=hex_color)
                
                # Apply color to display if there's content
                if hasattr(self, 'img_display') and self.img_display.get(1.0, tk.END).strip():
                    # Get current theme colors as default
                    if self.current_theme == "System":
                        actual_theme = self.detect_system_theme()
                        theme = self.themes[actual_theme]
                    else:
                        theme = self.themes[self.current_theme]
                    
                    # Set default theme colors first
                    fg_color = hex_color
                    bg_color = theme["display_bg"]
                    
                    # Override background if custom background is set
                    if self.custom_bg_color:
                        bg_color = f"#{self.custom_bg_color[0]:02x}{self.custom_bg_color[1]:02x}{self.custom_bg_color[2]:02x}"
                    
                    self.img_display.config(fg=fg_color, bg=bg_color)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open color chooser: {str(e)}")
    
    def choose_bg_color(self):
        """배경 색상을 선택합니다"""
        try:
            # Try to import colorchooser
            try:
                from tkinter import colorchooser
                color = colorchooser.askcolor(
                    title="Choose Background Color",
                    color="#000000" if not self.custom_bg_color else 
                          f"#{self.custom_bg_color[0]:02x}{self.custom_bg_color[1]:02x}{self.custom_bg_color[2]:02x}"
                )
            except Exception as e:
                # Fallback: show a simple color input dialog
                messagebox.showinfo("Color Chooser", "Color chooser not available. Using default black.")
                color = ((0, 0, 0), "#000000")  # Default black
            
            if color[0]:  # color[0] is RGB tuple
                self.custom_bg_color = tuple(int(c) for c in color[0])
                # Update preview
                hex_color = color[1]  # color[1] is hex string
                self.bg_color_preview.config(fg=hex_color)
                
                # Apply color to display if there's content
                if hasattr(self, 'img_display') and self.img_display.get(1.0, tk.END).strip():
                    # Get current theme colors as default
                    if self.current_theme == "System":
                        actual_theme = self.detect_system_theme()
                        theme = self.themes[actual_theme]
                    else:
                        theme = self.themes[self.current_theme]
                    
                    # Set default theme colors first
                    fg_color = theme["display_fg"]
                    bg_color = hex_color
                    
                    # Override foreground if custom foreground is set
                    if self.custom_fg_color:
                        fg_color = f"#{self.custom_fg_color[0]:02x}{self.custom_fg_color[1]:02x}{self.custom_fg_color[2]:02x}"
                    
                    self.img_display.config(fg=fg_color, bg=bg_color)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open color chooser: {str(e)}")
    
    # Video Tab Methods
    def select_video(self):
        """비디오 파일을 선택합니다"""
        filename = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.current_video_path = filename
            self.vid_path_label.config(
                text=os.path.basename(filename),
                fg="#1d1d1f"
            )
            
            # Get video info
            try:
                cap = cv2.VideoCapture(filename)
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = frame_count / fps if fps > 0 else 0
                cap.release()
                
                info_text = f"FPS: {fps:.1f}\nFrames: {frame_count}\nDuration: {duration:.1f}s"
                self.vid_info_label.config(text=info_text)
            except:
                self.vid_info_label.config(text="Could not read video info")
    
    def play_video(self):
        """비디오를 재생합니다"""
        if not self.current_video_path:
            messagebox.showwarning("No Video", "Please select a video first")
            return
        
        if self.video_playing:
            return
        
        self.video_playing = True
        self.vid_play_btn.config(state=tk.DISABLED, bg="#636366")
        self.vid_stop_btn.config(state=tk.NORMAL, bg="#ff3b30")
        
        self.video_thread = threading.Thread(
            target=self.play_video_thread,
            daemon=True
        )
        self.video_thread.start()
    
    def stop_video(self):
        """비디오 재생을 중지합니다"""
        self.video_playing = False
        theme = self.themes[self.current_theme]
        self.vid_play_btn.config(state=tk.NORMAL, bg=theme["accent_green"])
        self.vid_stop_btn.config(state=tk.DISABLED, bg=theme["accent_gray"])
    
    def export_video(self):
        """비디오를 ASCII 비디오로 내보냅니다"""
        if not self.current_video_path:
            messagebox.showwarning("No Video", "Please select a video first")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export ASCII Video",
            defaultextension=".mp4",
            filetypes=[
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("MOV files", "*.mov"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                # Show progress dialog
                progress_window = tk.Toplevel(self.root)
                progress_window.title("Exporting Video")
                progress_window.geometry("400x100")
                progress_window.transient(self.root)
                progress_window.grab_set()
                
                theme = self.themes[self.current_theme]
                progress_window.configure(bg=theme["bg"])
                
                tk.Label(
                    progress_window,
                    text="Converting video to ASCII...\nThis may take a while.",
                    font=("SF Pro Text", 12),
                    bg=theme["bg"],
                    fg=theme["fg"]
                ).pack(pady=20)
                
                progress_window.update()
                
                # Get settings
                width = int(self.vid_width_slider.get())
                fps = int(self.vid_fps_slider.get())
                detailed = self.vid_detailed.get()
                invert = self.vid_invert.get()
                
                # Get aspect ratio
                try:
                    aspect_w = float(self.vid_aspect_width_var.get())
                    aspect_h = float(self.vid_aspect_height_var.get())
                    if aspect_h == 0:
                        aspect_h = 1.0
                    aspect_ratio = aspect_w / aspect_h
                except ValueError:
                    aspect_ratio = 2.0  # Default aspect ratio
                
                # Set colors based on custom colors or theme
                if self.custom_fg_color and self.custom_bg_color:
                    fg_color = self.custom_fg_color
                    bg_color = self.custom_bg_color
                elif self.current_theme == "Dark":
                    bg_color = (0, 0, 0)
                    fg_color = (0, 255, 0)
                else:
                    bg_color = (29, 29, 31)
                    fg_color = (245, 245, 247)
                
                converter = AsciiConverter(width=width, detailed=detailed, invert=invert, aspect_ratio=aspect_ratio)
                exporter = AsciiExporter(font_size=6, bg_color=bg_color, fg_color=fg_color)
                
                # Convert video (this will take a while)
                success = exporter.video_to_ascii_video(
                    self.current_video_path,
                    filename,
                    converter,
                    fps=fps,
                    max_frames=300  # Limit to 300 frames for reasonable processing time
                )
                
                progress_window.destroy()
                
                if success:
                    messagebox.showinfo("Success", f"ASCII video exported to {filename}")
                else:
                    messagebox.showerror("Error", "Failed to export video")
                    
            except Exception as e:
                if 'progress_window' in locals():
                    progress_window.destroy()
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def play_video_thread(self):
        """비디오 재생 스레드"""
        try:
            cap = cv2.VideoCapture(self.current_video_path)
            
            width = int(self.vid_width_slider.get())
            fps = int(self.vid_fps_slider.get())
            detailed = self.vid_detailed.get()
            invert = self.vid_invert.get()
            
            # Get aspect ratio
            try:
                aspect_w = float(self.vid_aspect_width_var.get())
                aspect_h = float(self.vid_aspect_height_var.get())
                if aspect_h == 0:
                    aspect_h = 1.0
                aspect_ratio = aspect_w / aspect_h
            except ValueError:
                aspect_ratio = 2.0  # Default aspect ratio
            
            converter = AsciiConverter(width=width, detailed=detailed, invert=invert, aspect_ratio=aspect_ratio)
            
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_skip = max(1, int(original_fps / fps))
            frame_delay = 1.0 / fps
            
            frame_count = 0
            
            while self.video_playing and cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                if frame_count % frame_skip != 0:
                    frame_count += 1
                    continue
                
                # Convert frame to ASCII using converter
                ascii_frame = converter._frame_to_ascii(frame)
                
                # Update display
                self.root.after(0, self.update_display, self.vid_display, ascii_frame)
                
                time.sleep(frame_delay)
                frame_count += 1
            
            cap.release()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play video: {str(e)}")
        
        finally:
            self.video_playing = False
            if self.current_theme == "System":
                actual_theme = self.detect_system_theme()
                theme = self.themes[actual_theme]
            else:
                theme = self.themes[self.current_theme]
            self.root.after(0, lambda: self.vid_play_btn.config(state=tk.NORMAL, bg=theme["accent_green"]))
            self.root.after(0, lambda: self.vid_stop_btn.config(state=tk.DISABLED, bg=theme["accent_gray"]))
    
    def update_display(self, display, text):
        """디스플레이를 업데이트합니다"""
        display.delete(1.0, tk.END)
        display.insert(1.0, text)
        
        # Apply custom colors if this is the video display
        if display == self.vid_display:
            # Get current theme colors as default
            if self.current_theme == "System":
                actual_theme = self.detect_system_theme()
                theme = self.themes[actual_theme]
            else:
                theme = self.themes[self.current_theme]
            
            # Set default theme colors first
            fg_color = theme["display_fg"]
            bg_color = theme["display_bg"]
            
            # Override with custom colors if set
            if self.custom_fg_color:
                fg_color = f"#{self.custom_fg_color[0]:02x}{self.custom_fg_color[1]:02x}{self.custom_fg_color[2]:02x}"
            
            if self.custom_bg_color:
                bg_color = f"#{self.custom_bg_color[0]:02x}{self.custom_bg_color[1]:02x}{self.custom_bg_color[2]:02x}"
            
            # Apply colors to the text widget
            display.config(fg=fg_color, bg=bg_color)
    
    # 3D Tab Methods
    def create_3d_tab(self):
        """3D 렌더링 탭을 생성합니다"""
        theme = self.themes[self.current_theme]
        
        tab = tk.Frame(self.notebook, bg=theme["panel_bg"])
        self.notebook.add(tab, text="3D Objects")
        
        # Split into left and right panels
        left_frame = tk.Frame(tab, bg=theme["panel_bg"], width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)
        left_frame.pack_propagate(False)
        
        right_frame = tk.Frame(tab, bg=theme["display_bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=15)
        
        # Left panel - Controls
        self.create_section_label(left_frame, "3D Shape")
        
        self.shape_3d = tk.StringVar(value="cube")
        shapes = [
            ("Cube", "cube"),
            ("Sphere", "sphere"),
            ("Donut", "torus"),
            ("Pyramid", "pyramid")
        ]
        
        for text, value in shapes:
            rb = tk.Radiobutton(
                left_frame,
                text=text,
                variable=self.shape_3d,
                value=value,
                bg=theme["panel_bg"],
                fg=theme["fg"],
                font=("SF Pro Text", 12),
                activebackground=theme["panel_bg"],
                selectcolor=theme["button_bg"]
            )
            rb.pack(anchor=tk.W, padx=20, pady=2)
        
        # Rotation Controls
        self.create_section_label(left_frame, "Rotation", top_margin=20)
        
        self.create_slider(left_frame, "Speed:", 1, 50, 10, "speed_3d")
        
        # Rendering Options
        self.create_section_label(left_frame, "Rendering", top_margin=20)
        
        self.create_slider(left_frame, "FPS:", 10, 60, 30, "fps_3d")
        self.create_slider(left_frame, "Detail:", 20, 50, 30, "detail_3d")
        
        # Playback controls
        self.create_section_label(left_frame, "Controls", top_margin=20)
        
        btn_frame = tk.Frame(left_frame, bg=theme["panel_bg"])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.render_3d_start_btn = tk.Button(
            btn_frame,
            text="Start",
            command=self.start_3d_render,
            bg=theme["accent_green"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=theme["accent_green"]
        )
        self.render_3d_start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5), pady=5)
        
        self.render_3d_stop_btn = tk.Button(
            btn_frame,
            text="Stop",
            command=self.stop_3d_render,
            bg=theme["accent_gray_dark"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            activebackground=theme["accent_gray_dark"]
        )
        self.render_3d_stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0), pady=5)
        
        # Screenshot export buttons for 3D tab
        screenshot_frame = tk.Frame(left_frame, bg=theme["panel_bg"])
        screenshot_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            screenshot_frame,
            text="📸 Capture Display Area",
            command=self.capture_3d_display_area,
            bg=theme["accent_green"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_green"]
        ).pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(
            screenshot_frame,
            text="📷 Screenshot Full GUI",
            command=self.screenshot_full_gui,
            bg=theme["accent_blue"],
            fg=theme["button_fg"],
            font=("SF Pro Text", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            activebackground=theme["accent_blue"]
        ).pack(fill=tk.X)
        
        # Info section
        self.create_section_label(left_frame, "Info", top_margin=20)
        
        info_text = "Real-time 3D ASCII rendering with full 360° rotation. " \
                   "Objects are rendered with lighting and depth."
        
        info_label = tk.Label(
            left_frame,
            text=info_text,
            font=("SF Pro Text", 10),
            bg=theme["panel_bg"],
            fg=theme["secondary_fg"],
            wraplength=250,
            justify=tk.LEFT
        )
        info_label.pack(padx=20, pady=10)
        
        # Right panel - Display
        self.display_3d = scrolledtext.ScrolledText(
            right_frame,
            font=("Courier", 8),
            bg=theme["display_bg"],
            fg=theme["display_fg"],
            relief=tk.FLAT,
            wrap=tk.NONE,
            padx=10,
            pady=10,
            insertbackground=theme["display_fg"]
        )
        self.display_3d.pack(fill=tk.BOTH, expand=True)
        self.display_3d.insert(1.0, "Click 'Start' to begin 3D rendering")
    
    def start_3d_render(self):
        """3D 렌더링을 시작합니다"""
        if self.render_3d_running:
            return
        
        theme = self.themes[self.current_theme]
        
        self.render_3d_running = True
        self.render_3d_start_btn.config(state=tk.DISABLED, bg=theme["accent_gray"])
        self.render_3d_stop_btn.config(state=tk.NORMAL, bg=theme["accent_red"])
        
        self.render_3d_thread = threading.Thread(
            target=self.render_3d_loop,
            daemon=True
        )
        self.render_3d_thread.start()
    
    def stop_3d_render(self):
        """3D 렌더링을 중지합니다"""
        theme = self.themes[self.current_theme]
        
        self.render_3d_running = False
        self.render_3d_start_btn.config(state=tk.NORMAL, bg=theme["accent_green"])
        self.render_3d_stop_btn.config(state=tk.DISABLED, bg=theme["accent_gray"])
    
    def render_3d_loop(self):
        """3D 렌더링 루프"""
        frame = 0
        
        try:
            while self.render_3d_running:
                shape = self.shape_3d.get()
                speed = int(self.speed_3d_slider.get()) / 10.0
                fps = int(self.fps_3d_slider.get())
                detail = int(self.detail_3d_slider.get())
                
                self.renderer_3d.clear()
                
                angle = frame * 0.05 * speed
                
                if shape == "cube":
                    self.renderer_3d.draw_cube(angle, angle * 0.7, angle * 0.5, size=1.5)
                elif shape == "sphere":
                    self.renderer_3d.draw_sphere(angle * 0.6, angle, radius=1.5, detail=detail)
                elif shape == "torus":
                    self.renderer_3d.draw_torus(angle, angle * 0.5, angle * 0.8, R=2, r=0.8, detail=detail)
                elif shape == "pyramid":
                    self.renderer_3d.draw_pyramid(angle, angle * 0.7, angle * 0.5, size=1.5)
                
                ascii_output = self.renderer_3d.render()
                
                # Update display
                self.root.after(0, self.update_display, self.display_3d, ascii_output)
                
                time.sleep(1 / fps)
                frame += 1
                
        except Exception as e:
            print(f"3D render error: {e}")
        finally:
            self.render_3d_running = False
            if self.current_theme == "System":
                actual_theme = self.detect_system_theme()
                theme = self.themes[actual_theme]
            else:
                theme = self.themes[self.current_theme]
            self.root.after(0, lambda: self.render_3d_start_btn.config(state=tk.NORMAL, bg=theme["accent_green"]))
            self.root.after(0, lambda: self.render_3d_stop_btn.config(state=tk.DISABLED, bg=theme["accent_gray"]))

    # Auto-convert callback functions
    def on_image_setting_change(self, *args):
        """이미지 설정이 변경될 때 자동으로 변환을 실행합니다"""
        if self.current_image_path:
            try:
                self.convert_image()
            except Exception as e:
                # 에러가 발생해도 무시 (사용자가 입력 중일 수 있음)
                pass

    def on_aspect_ratio_change(self, *args):
        """이미지 비율이 변경될 때 자동으로 변환을 실행합니다"""
        if self.current_image_path:
            try:
                self.convert_image()
            except Exception as e:
                # 에러가 발생해도 무시 (사용자가 입력 중일 수 있음)
                pass

    def on_video_setting_change(self, *args):
        """비디오 설정이 변경될 때 자동으로 변환을 실행합니다"""
        if self.current_video_path and self.video_playing:
            # 비디오가 재생 중일 때만 자동 변환
            # 실제로는 재생 중에 설정이 변경되면 새로운 설정으로 계속 재생
            pass

    def on_video_aspect_ratio_change(self, *args):
        """비디오 비율이 변경될 때 자동으로 변환을 실행합니다"""
        if self.current_video_path and self.video_playing:
            # 비디오가 재생 중일 때만 자동 변환
            pass


def main():
    root = tk.Tk()
    app = AsciiArtGUIFull(root)
    root.mainloop()


if __name__ == "__main__":
    main()

