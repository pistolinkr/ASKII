#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
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

class AsciiArtGUISimple:
    """ASCII Art와 이미지/비디오 변환을 지원하는 간단한 GUI 애플리케이션"""
    
    def __init__(self):
        self.root = tk.Tk()
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
            }
        }
        
        self.current_theme = "Light"
        self.theme = self.themes[self.current_theme]
        
        # Initialize renderer
        self.renderer = AsciiArtRenderer()
        self.converter = AsciiConverter()
        self.exporter = AsciiExporter()
        
        # Initialize variables
        self.current_image_path = None
        self.current_video_path = None
        self.custom_fg_color = None
        self.custom_bg_color = None
        self.aspect_ratio_width = 2.0
        self.aspect_ratio_height = 1.0
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI를 설정합니다"""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.theme["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="ASCII Art Studio",
            font=("SF Pro Text", 24, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["fg"]
        )
        title_label.pack(pady=20)
        
        # Create tabs
        self.create_tabs()
        
    def create_tabs(self):
        """탭을 생성합니다"""
        # Tab container
        tab_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        tab_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Tab buttons
        self.tab_buttons = {}
        tabs = [
            ("Generate", "Generate Art"),
            ("Image", "Image to ASCII"),
            ("Video", "Video to ASCII"),
            ("3D", "3D Objects")
        ]
        
        for i, (key, label) in enumerate(tabs):
            btn = tk.Button(
                tab_frame,
                text=label,
                command=lambda k=key: self.switch_tab(k),
                bg=self.theme["accent_blue"] if i == 0 else self.theme["button_bg"],
                fg=self.theme["button_fg"],
                font=("SF Pro Text", 12, "bold"),
                relief=tk.FLAT,
                padx=20,
                pady=10,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.tab_buttons[key] = btn
        
        # Content area
        self.content_frame = tk.Frame(self.main_frame, bg=self.theme["bg"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create tab contents
        self.create_generate_tab()
        self.create_image_tab()
        self.create_video_tab()
        self.create_3d_tab()
        
        # Show default tab
        self.switch_tab("Generate")
        
    def create_generate_tab(self):
        """Generate Art 탭을 생성합니다"""
        frame = tk.Frame(self.content_frame, bg=self.theme["bg"])
        
        # Left panel
        left_frame = tk.Frame(frame, bg=self.theme["panel_bg"], relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Art type selection
        art_frame = tk.Frame(left_frame, bg=self.theme["panel_bg"])
        art_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            art_frame,
            text="Art Type:",
            font=("SF Pro Text", 12, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["fg"]
        ).pack(anchor=tk.W)
        
        self.art_type_var = tk.StringVar(value="banner")
        art_types = [
            ("Banner", "banner"),
            ("Wave", "wave"),
            ("Circle", "circle"),
            ("Spiral", "spiral"),
            ("Heart", "heart"),
            ("Box Text", "box_text")
        ]
        
        for text, value in art_types:
            tk.Radiobutton(
                art_frame,
                text=text,
                variable=self.art_type_var,
                value=value,
                command=self.generate_art,
                bg=self.theme["panel_bg"],
                fg=self.theme["fg"],
                font=("SF Pro Text", 10),
                selectcolor=self.theme["accent_blue"]
            ).pack(anchor=tk.W, pady=2)
        
        # Generate button
        generate_btn = tk.Button(
            art_frame,
            text="Generate Art",
            command=self.generate_art,
            bg=self.theme["accent_green"],
            fg=self.theme["button_fg"],
            font=("SF Pro Text", 12, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        generate_btn.pack(pady=20)
        
        # Right panel - Display
        right_frame = tk.Frame(frame, bg=self.theme["bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Display area
        self.art_display = scrolledtext.ScrolledText(
            right_frame,
            bg=self.theme["display_bg"],
            fg=self.theme["display_fg"],
            font=("Monaco", 10),
            wrap=tk.NONE,
            state=tk.DISABLED
        )
        self.art_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_contents = {"Generate": frame}
        
    def create_image_tab(self):
        """Image to ASCII 탭을 생성합니다"""
        frame = tk.Frame(self.content_frame, bg=self.theme["bg"])
        
        # Left panel
        left_frame = tk.Frame(frame, bg=self.theme["panel_bg"], relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Image selection
        img_frame = tk.Frame(left_frame, bg=self.theme["panel_bg"])
        img_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            img_frame,
            text="Image to ASCII:",
            font=("SF Pro Text", 12, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["fg"]
        ).pack(anchor=tk.W)
        
        select_btn = tk.Button(
            img_frame,
            text="Select Image",
            command=self.select_image,
            bg=self.theme["button_bg"],
            fg=self.theme["button_fg"],
            font=("SF Pro Text", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        select_btn.pack(pady=10)
        
        convert_btn = tk.Button(
            img_frame,
            text="Convert to ASCII",
            command=self.convert_image,
            bg=self.theme["accent_green"],
            fg=self.theme["button_fg"],
            font=("SF Pro Text", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        convert_btn.pack(pady=10)
        
        # Right panel - Display
        right_frame = tk.Frame(frame, bg=self.theme["bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Display area
        self.img_display = scrolledtext.ScrolledText(
            right_frame,
            bg=self.theme["display_bg"],
            fg=self.theme["display_fg"],
            font=("Monaco", 8),
            wrap=tk.NONE,
            state=tk.DISABLED
        )
        self.img_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_contents["Image"] = frame
        
    def create_video_tab(self):
        """Video to ASCII 탭을 생성합니다"""
        frame = tk.Frame(self.content_frame, bg=self.theme["bg"])
        
        # Left panel
        left_frame = tk.Frame(frame, bg=self.theme["panel_bg"], relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Video selection
        vid_frame = tk.Frame(left_frame, bg=self.theme["panel_bg"])
        vid_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            vid_frame,
            text="Video to ASCII:",
            font=("SF Pro Text", 12, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["fg"]
        ).pack(anchor=tk.W)
        
        select_btn = tk.Button(
            vid_frame,
            text="Select Video",
            command=self.select_video,
            bg=self.theme["button_bg"],
            fg=self.theme["button_fg"],
            font=("SF Pro Text", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        select_btn.pack(pady=10)
        
        convert_btn = tk.Button(
            vid_frame,
            text="Convert to ASCII",
            command=self.convert_video,
            bg=self.theme["accent_green"],
            fg=self.theme["button_fg"],
            font=("SF Pro Text", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        convert_btn.pack(pady=10)
        
        # Right panel - Display
        right_frame = tk.Frame(frame, bg=self.theme["bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Display area
        self.vid_display = scrolledtext.ScrolledText(
            right_frame,
            bg=self.theme["display_bg"],
            fg=self.theme["display_fg"],
            font=("Monaco", 8),
            wrap=tk.NONE,
            state=tk.DISABLED
        )
        self.vid_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_contents["Video"] = frame
        
    def create_3d_tab(self):
        """3D Objects 탭을 생성합니다"""
        frame = tk.Frame(self.content_frame, bg=self.theme["bg"])
        
        # Left panel
        left_frame = tk.Frame(frame, bg=self.theme["panel_bg"], relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 3D object selection
        obj_frame = tk.Frame(left_frame, bg=self.theme["panel_bg"])
        obj_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            obj_frame,
            text="3D Objects:",
            font=("SF Pro Text", 12, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["fg"]
        ).pack(anchor=tk.W)
        
        self.obj_type_var = tk.StringVar(value="cube")
        obj_types = [
            ("Cube", "cube"),
            ("Sphere", "sphere"),
            ("Pyramid", "pyramid"),
            ("Torus", "torus")
        ]
        
        for text, value in obj_types:
            tk.Radiobutton(
                obj_frame,
                text=text,
                variable=self.obj_type_var,
                value=value,
                command=self.generate_3d,
                bg=self.theme["panel_bg"],
                fg=self.theme["fg"],
                font=("SF Pro Text", 10),
                selectcolor=self.theme["accent_blue"]
            ).pack(anchor=tk.W, pady=2)
        
        generate_btn = tk.Button(
            obj_frame,
            text="Generate 3D",
            command=self.generate_3d,
            bg=self.theme["accent_green"],
            fg=self.theme["button_fg"],
            font=("SF Pro Text", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        generate_btn.pack(pady=20)
        
        # Right panel - Display
        right_frame = tk.Frame(frame, bg=self.theme["bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Display area
        self.display_3d = scrolledtext.ScrolledText(
            right_frame,
            bg=self.theme["display_bg"],
            fg=self.theme["display_fg"],
            font=("Monaco", 8),
            wrap=tk.NONE,
            state=tk.DISABLED
        )
        self.display_3d.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_contents["3D"] = frame
        
    def switch_tab(self, tab_name):
        """탭을 전환합니다"""
        # Hide all tab contents
        for content in self.tab_contents.values():
            content.pack_forget()
        
        # Show selected tab content
        if tab_name in self.tab_contents:
            self.tab_contents[tab_name].pack(fill=tk.BOTH, expand=True)
        
        # Update tab button colors
        for key, btn in self.tab_buttons.items():
            if key == tab_name:
                btn.config(bg=self.theme["accent_blue"])
            else:
                btn.config(bg=self.theme["button_bg"])
        
    def generate_art(self):
        """ASCII 아트를 생성합니다"""
        art_type = self.art_type_var.get()
        
        try:
            if art_type == "banner":
                art = self.renderer.text_banner("ASCII ART")
            elif art_type == "wave":
                art = self.renderer.wave(20)
            elif art_type == "circle":
                art = self.renderer.circle(15)
            elif art_type == "spiral":
                art = self.renderer.spiral(20)
            elif art_type == "heart":
                art = self.renderer.heart(15)
            elif art_type == "box_text":
                art = self.renderer.box_text("ASCII ART", 30)
            else:
                art = "Unknown art type"
            
            # Display the art
            self.art_display.config(state=tk.NORMAL)
            self.art_display.delete(1.0, tk.END)
            self.art_display.insert(1.0, art)
            self.art_display.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate art: {str(e)}")
    
    def select_image(self):
        """이미지를 선택합니다"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.current_image_path = file_path
            messagebox.showinfo("Success", f"Image selected: {os.path.basename(file_path)}")
    
    def convert_image(self):
        """이미지를 ASCII로 변환합니다"""
        if not self.current_image_path:
            messagebox.showwarning("No Image", "Please select an image first!")
            return
        
        try:
            # Convert image to ASCII
            ascii_art = self.converter.image_to_ascii(
                self.current_image_path,
                width=80,
                height=40
            )
            
            # Display the result
            self.img_display.config(state=tk.NORMAL)
            self.img_display.delete(1.0, tk.END)
            self.img_display.insert(1.0, ascii_art)
            self.img_display.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image: {str(e)}")
    
    def select_video(self):
        """비디오를 선택합니다"""
        file_path = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.current_video_path = file_path
            messagebox.showinfo("Success", f"Video selected: {os.path.basename(file_path)}")
    
    def convert_video(self):
        """비디오를 ASCII로 변환합니다"""
        if not self.current_video_path:
            messagebox.showwarning("No Video", "Please select a video first!")
            return
        
        try:
            # Convert video to ASCII (first frame only for simplicity)
            ascii_art = self.converter.video_to_ascii(
                self.current_video_path,
                width=80,
                height=40,
                max_frames=1
            )
            
            # Display the result
            self.vid_display.config(state=tk.NORMAL)
            self.vid_display.delete(1.0, tk.END)
            self.vid_display.insert(1.0, ascii_art)
            self.vid_display.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert video: {str(e)}")
    
    def generate_3d(self):
        """3D 객체를 생성합니다"""
        obj_type = self.obj_type_var.get()
        
        try:
            # Generate 3D object
            if obj_type == "cube":
                art = self.renderer.cube(10)
            elif obj_type == "sphere":
                art = self.renderer.sphere(10)
            elif obj_type == "pyramid":
                art = self.renderer.pyramid(10)
            elif obj_type == "torus":
                art = self.renderer.torus(10, 5)
            else:
                art = "Unknown object type"
            
            # Display the result
            self.display_3d.config(state=tk.NORMAL)
            self.display_3d.delete(1.0, tk.END)
            self.display_3d.insert(1.0, art)
            self.display_3d.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate 3D object: {str(e)}")
    
    def run(self):
        """GUI를 실행합니다"""
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = AsciiArtGUISimple()
    app.run()

if __name__ == "__main__":
    main()
