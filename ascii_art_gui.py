#!/usr/bin/env python3
"""
ASCII Art GUI Application
GUI interface for generating and rendering dynamic ASCII art
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, font as tkfont
import math
import threading
import time
from ascii_art import AsciiArtRenderer


class AsciiArtGUI:
    """ASCII Art를 렌더링하는 GUI 애플리케이션"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Generator")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f7")
        
        self.renderer = AsciiArtRenderer()
        self.animation_running = False
        self.animation_thread = None
        
        self.setup_ui()
        self.render_art()
    
    def setup_ui(self):
        """UI 컴포넌트를 설정합니다"""
        # Main container with padding
        main_frame = tk.Frame(self.root, bg="#f5f5f7")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Controls
        control_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Title
        title_label = tk.Label(
            control_frame,
            text="ASCII Art",
            font=("SF Pro Display", 24, "bold"),
            bg="#ffffff",
            fg="#1d1d1f"
        )
        title_label.pack(pady=(20, 30), padx=20)
        
        # Art Type Selection
        self.create_section_label(control_frame, "Art Type")
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
                control_frame,
                text=text,
                variable=self.art_type,
                value=value,
                command=self.on_type_change,
                bg="#ffffff",
                fg="#1d1d1f",
                font=("SF Pro Text", 13),
                activebackground="#ffffff",
                selectcolor="#007aff",
                bd=0,
                highlightthickness=0
            )
            rb.pack(anchor=tk.W, padx=30, pady=3)
        
        # Parameters
        self.create_section_label(control_frame, "Parameters", top_margin=25)
        
        # Text input
        self.text_label = tk.Label(
            control_frame,
            text="Text:",
            font=("SF Pro Text", 13),
            bg="#ffffff",
            fg="#1d1d1f"
        )
        self.text_label.pack(anchor=tk.W, padx=30, pady=(5, 2))
        
        self.text_entry = tk.Entry(
            control_frame,
            font=("SF Pro Text", 12),
            bg="#f5f5f7",
            fg="#1d1d1f",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground="#d2d2d7",
            highlightcolor="#007aff"
        )
        self.text_entry.insert(0, "Hello, World!")
        self.text_entry.pack(fill=tk.X, padx=30, pady=(0, 10), ipady=6)
        self.text_entry.bind("<KeyRelease>", lambda e: self.render_art())
        
        # Width slider
        self.create_slider(control_frame, "Width:", 20, 100, 60, "width")
        
        # Size slider
        self.create_slider(control_frame, "Size:", 5, 30, 10, "size")
        
        # Character input
        tk.Label(
            control_frame,
            text="Character:",
            font=("SF Pro Text", 13),
            bg="#ffffff",
            fg="#1d1d1f"
        ).pack(anchor=tk.W, padx=30, pady=(5, 2))
        
        self.char_entry = tk.Entry(
            control_frame,
            font=("SF Pro Text", 12),
            bg="#f5f5f7",
            fg="#1d1d1f",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground="#d2d2d7",
            highlightcolor="#007aff"
        )
        self.char_entry.insert(0, "*")
        self.char_entry.pack(fill=tk.X, padx=30, pady=(0, 10), ipady=6)
        self.char_entry.bind("<KeyRelease>", lambda e: self.render_art())
        
        # Animation Controls
        self.create_section_label(control_frame, "Animation", top_margin=25)
        
        button_frame = tk.Frame(control_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, padx=30, pady=10)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start",
            command=self.start_animation,
            bg="#007aff",
            fg="#ffffff",
            font=("SF Pro Text", 13, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            activebackground="#0051d5"
        )
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_animation,
            bg="#8e8e93",
            fg="#ffffff",
            font=("SF Pro Text", 13, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            activebackground="#636366",
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
        
        # FPS slider
        self.create_slider(control_frame, "FPS:", 5, 30, 10, "fps")
        
        # Right panel - Display
        display_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.FLAT)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Display title
        display_title = tk.Label(
            display_frame,
            text="Preview",
            font=("SF Pro Display", 18, "bold"),
            bg="#ffffff",
            fg="#1d1d1f"
        )
        display_title.pack(pady=(20, 15), padx=20)
        
        # Text display area
        text_frame = tk.Frame(display_frame, bg="#1d1d1f")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.display = scrolledtext.ScrolledText(
            text_frame,
            font=("Courier", 10),
            bg="#1d1d1f",
            fg="#f5f5f7",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15,
            wrap=tk.NONE
        )
        self.display.pack(fill=tk.BOTH, expand=True)
    
    def create_section_label(self, parent, text, top_margin=0):
        """섹션 라벨을 생성합니다"""
        label = tk.Label(
            parent,
            text=text,
            font=("SF Pro Display", 15, "bold"),
            bg="#ffffff",
            fg="#1d1d1f"
        )
        label.pack(anchor=tk.W, padx=20, pady=(top_margin, 10))
    
    def create_slider(self, parent, label_text, from_, to, default, attr_name):
        """슬라이더 컨트롤을 생성합니다"""
        label = tk.Label(
            parent,
            text=label_text,
            font=("SF Pro Text", 13),
            bg="#ffffff",
            fg="#1d1d1f"
        )
        label.pack(anchor=tk.W, padx=30, pady=(5, 2))
        
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(fill=tk.X, padx=30, pady=(0, 10))
        
        slider = tk.Scale(
            frame,
            from_=from_,
            to=to,
            orient=tk.HORIZONTAL,
            command=lambda v: self.render_art(),
            bg="#ffffff",
            fg="#1d1d1f",
            font=("SF Pro Text", 11),
            troughcolor="#f5f5f7",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            activebackground="#007aff"
        )
        slider.set(default)
        slider.pack(fill=tk.X)
        
        setattr(self, f"{attr_name}_slider", slider)
    
    def on_type_change(self):
        """아트 타입 변경 시 UI를 업데이트합니다"""
        art_type = self.art_type.get()
        
        # Show/hide text input based on art type
        if art_type in ["banner", "box"]:
            self.text_label.pack(anchor=tk.W, padx=30, pady=(5, 2))
            self.text_entry.pack(fill=tk.X, padx=30, pady=(0, 10), ipady=6)
        else:
            self.text_label.pack_forget()
            self.text_entry.pack_forget()
        
        self.render_art()
    
    def render_art(self):
        """현재 설정으로 ASCII 아트를 렌더링합니다"""
        if self.animation_running:
            return
        
        art_type = self.art_type.get()
        width = int(self.width_slider.get())
        size = int(self.size_slider.get())
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
            
            self.display.delete(1.0, tk.END)
            self.display.insert(1.0, art)
        except Exception as e:
            self.display.delete(1.0, tk.END)
            self.display.insert(1.0, f"Error: {str(e)}")
    
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
        fps = int(self.fps_slider.get())
        frame = 0
        
        while self.animation_running:
            try:
                width = int(self.width_slider.get())
                size = int(self.size_slider.get())
                
                if art_type == "wave":
                    phase = (frame / fps) * 2 * math.pi
                    art = self.renderer.wave(width=width, height=size, phase=phase)
                elif art_type == "spiral":
                    rotation = (frame / fps) * math.pi / 2
                    art = self.renderer.spiral(size=size, rotation=rotation)
                else:
                    # For non-animated types, just render normally
                    self.root.after(0, self.render_art)
                    time.sleep(1 / fps)
                    frame += 1
                    continue
                
                # Update display in main thread
                self.root.after(0, self.update_display, art)
                
                time.sleep(1 / fps)
                frame += 1
            except Exception as e:
                print(f"Animation error: {e}")
                break
        
        self.animation_running = False
    
    def update_display(self, text):
        """디스플레이를 업데이트합니다"""
        self.display.delete(1.0, tk.END)
        self.display.insert(1.0, text)


def main():
    root = tk.Tk()
    app = AsciiArtGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

