import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import tempfile
import os
import threading

class SpeechTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Translator")
        self.root.geometry("900x700")
        self.root.minsize(800, 650)
        self.root.configure(bg="#f5f5f5")
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        pygame.mixer.init()
        
        # Language options
        self.languages = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Chinese': 'zh-cn',
            'Arabic': 'ar',
            'Hindi': 'hi',
            'Turkish': 'tr',
            'Swedish': 'sv',
            'Dutch': 'nl',
            'Polish': 'pl',
            'Greek': 'el'
        }
        
        # Default target languages
        self.default_targets = ['Spanish', 'French', 'German', 'Italian', 'Japanese', 'Chinese']
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#ffffff", height=120)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="Record yourself and receive voice translations",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        title.pack(pady=(20, 10))
        
        # Language selection frame
        lang_select_frame = tk.Frame(header, bg="#ffffff")
        lang_select_frame.pack(pady=(0, 15))
        
        tk.Label(
            lang_select_frame,
            text="Source Language:",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#666666"
        ).grid(row=0, column=0, padx=10, sticky="w")
        
        self.source_lang_var = tk.StringVar(value="English")
        self.source_lang_dropdown = ttk.Combobox(
            lang_select_frame,
            textvariable=self.source_lang_var,
            values=list(self.languages.keys()),
            state="readonly",
            width=15,
            font=("Segoe UI", 10)
        )
        self.source_lang_dropdown.grid(row=0, column=1, padx=10)
        
        tk.Label(
            lang_select_frame,
            text="Target Languages:",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#666666"
        ).grid(row=0, column=2, padx=10, sticky="w")
        
        tk.Button(
            lang_select_frame,
            text="Select Languages",
            font=("Segoe UI", 9),
            bg="#4CAF50",
            fg="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.open_language_selector,
            padx=15,
            pady=5
        ).grid(row=0, column=3, padx=10)
        
        tk.Button(
            lang_select_frame,
            text="Use Defaults",
            font=("Segoe UI", 9),
            bg="#2196F3",
            fg="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.use_default_languages,
            padx=15,
            pady=5
        ).grid(row=0, column=4, padx=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Audio input card
        audio_card = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1)
        audio_card.pack(fill="x", pady=(0, 15))
        
        audio_header = tk.Frame(audio_card, bg="#ffffff")
        audio_header.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(
            audio_header,
            text="🎵 Audio Input",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#666666"
        ).pack(side="left")
        
        # Waveform visualization placeholder
        self.waveform_canvas = tk.Canvas(
            audio_card,
            height=80,
            bg="#ffffff",
            highlightthickness=0
        )
        self.waveform_canvas.pack(fill="x", padx=20, pady=10)
        self.draw_waveform()
        
        # Recognized text display
        self.recognized_text = tk.Text(
            audio_card,
            height=2,
            font=("Segoe UI", 10),
            bg="#f9f9f9",
            fg="#333333",
            wrap=tk.WORD,
            relief="flat",
            padx=10,
            pady=10
        )
        self.recognized_text.pack(fill="x", padx=20, pady=(0, 15))
        self.recognized_text.insert("1.0", "Your speech will appear here...")
        self.recognized_text.config(state="disabled")
        
        # Action buttons
        button_frame = tk.Frame(main_container, bg="#f5f5f5")
        button_frame.pack(fill="x", pady=(0, 15))
        
        self.record_btn = tk.Button(
            button_frame,
            text="🎤 Start Recording",
            font=("Segoe UI", 11, "bold"),
            bg="#ff9966",
            fg="#ffffff",
            activebackground="#ff7744",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.start_recording,
            padx=40,
            pady=12
        )
        self.record_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="Clear All",
            font=("Segoe UI", 11),
            bg="#e0e0e0",
            fg="#666666",
            activebackground="#d0d0d0",
            activeforeground="#666666",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_all,
            padx=40,
            pady=12
        ).pack(side="left", expand=True, fill="x")
        
        # Status label
        self.status_label = tk.Label(
            main_container,
            text="Ready to record",
            font=("Segoe UI", 9),
            bg="#f5f5f5",
            fg="#999999"
        )
        self.status_label.pack(pady=(0, 10))
        
        # Scrollable translations container
        canvas_frame = tk.Frame(main_container, bg="#f5f5f5")
        canvas_frame.pack(fill="both", expand=True)
        
        self.translations_canvas = tk.Canvas(canvas_frame, bg="#f5f5f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.translations_canvas.yview)
        self.scrollable_frame = tk.Frame(self.translations_canvas, bg="#f5f5f5")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.translations_canvas.configure(scrollregion=self.translations_canvas.bbox("all"))
        )
        
        self.translations_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.translations_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.translations_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure grid weights
        for i in range(3):
            self.scrollable_frame.columnconfigure(i, weight=1)
        
        self.translation_cards = {}
        
        # Initialize with default languages
        self.use_default_languages()
        
    def draw_waveform(self):
        """Draw a simple waveform visualization"""
        self.waveform_canvas.delete("all")
        width = 800
        height = 80
        center = height // 2
        
        self.waveform_canvas.create_line(0, center, width, center, fill="#e0e0e0", dash=(2, 2))
        
        import random
        for i in range(0, width, 4):
            bar_height = random.randint(5, 35)
            self.waveform_canvas.create_line(
                i, center - bar_height,
                i, center + bar_height,
                fill="#66b3ff",
                width=2
            )
    
    def open_language_selector(self):
        """Open a window to select target languages"""
        selector_window = tk.Toplevel(self.root)
        selector_window.title("Select Target Languages")
        selector_window.geometry("400x500")
        selector_window.configure(bg="#ffffff")
        
        tk.Label(
            selector_window,
            text="Select languages to translate to:",
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=20)
        
        # Scrollable frame for checkboxes
        canvas = tk.Canvas(selector_window, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(selector_window, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#ffffff")
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Create checkboxes
        self.lang_vars = {}
        current_targets = list(self.translation_cards.keys())
        
        for lang in sorted(self.languages.keys()):
            if lang != self.source_lang_var.get():
                var = tk.BooleanVar(value=(lang in current_targets))
                self.lang_vars[lang] = var
                
                cb = tk.Checkbutton(
                    scrollable,
                    text=lang,
                    variable=var,
                    font=("Segoe UI", 10),
                    bg="#ffffff",
                    activebackground="#ffffff",
                    selectcolor="#ffffff"
                )
                cb.pack(anchor="w", pady=5, padx=20)
        
        # Apply button
        tk.Button(
            selector_window,
            text="Apply Selection",
            font=("Segoe UI", 11, "bold"),
            bg="#4CAF50",
            fg="#ffffff",
            activebackground="#45a049",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self.apply_language_selection(selector_window),
            padx=30,
            pady=10
        ).pack(pady=20)
    
    def apply_language_selection(self, window):
        """Apply the selected languages"""
        selected = [lang for lang, var in self.lang_vars.items() if var.get()]
        
        if not selected:
            self.status_label.config(text="Please select at least one language", fg="#ff6666")
            return
        
        self.update_translation_cards(selected)
        window.destroy()
        self.status_label.config(text="Languages updated. Ready to record.", fg="#66cc66")
    
    def use_default_languages(self):
        """Use default target languages"""
        self.update_translation_cards(self.default_targets)
        self.status_label.config(text="Default languages loaded. Ready to record.", fg="#66cc66")
    
    def update_translation_cards(self, languages):
        """Update the translation cards with selected languages"""
        # Clear existing cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.translation_cards.clear()
        
        # Create new cards
        for idx, lang in enumerate(languages):
            row = idx // 3
            col = idx % 3
            card = self.create_translation_card(self.scrollable_frame, lang)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.translation_cards[lang] = card
    
    def create_translation_card(self, parent, language):
        """Create a translation card for a specific language"""
        card = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        
        # Header
        header = tk.Frame(card, bg="#ffffff")
        header.pack(fill="x", padx=15, pady=(10, 5))
        
        tk.Label(
            header,
            text=f"🌍 {language}",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#666666"
        ).pack(side="left")
        
        # Translation text
        text_widget = tk.Text(
            card,
            height=3,
            font=("Segoe UI", 9),
            bg="#f9f9f9",
            fg="#333333",
            wrap=tk.WORD,
            relief="flat",
            padx=10,
            pady=10
        )
        text_widget.pack(fill="both", expand=True, padx=15, pady=5)
        text_widget.insert("1.0", "Translation will appear here...")
        text_widget.config(state="disabled")
        card.text_widget = text_widget
        
        # Controls
        controls = tk.Frame(card, bg="#ffffff")
        controls.pack(pady=10)
        
        play_btn = tk.Button(
            controls,
            text="▶ Play",
            font=("Segoe UI", 10),
            bg="#4CAF50",
            fg="#ffffff",
            activebackground="#45a049",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda l=language: self.play_translation(l),
            padx=15,
            pady=5,
            state="disabled"
        )
        play_btn.pack()
        card.play_button = play_btn
        
        return card
    
    def start_recording(self):
        thread = threading.Thread(target=self.record_and_translate)
        thread.daemon = True
        thread.start()
    
    def record_and_translate(self):
        try:
            self.status_label.config(text="🔴 Recording... Speak now!", fg="#ff6666")
            self.record_btn.config(state="disabled", bg="#cccccc")
            
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            self.status_label.config(text="⚙️ Processing...", fg="#6699ff")
            
            # Get source language
            source_lang = self.languages[self.source_lang_var.get()]
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language=source_lang)
            
            # Display recognized text
            self.recognized_text.config(state="normal")
            self.recognized_text.delete("1.0", tk.END)
            self.recognized_text.insert("1.0", text)
            self.recognized_text.config(state="disabled")
            
            # Translate to all selected languages
            for lang_name, card in self.translation_cards.items():
                try:
                    lang_code = self.languages[lang_name]
                    translation = self.translator.translate(text, src=source_lang, dest=lang_code)
                    
                    card.text_widget.config(state="normal")
                    card.text_widget.delete("1.0", tk.END)
                    card.text_widget.insert("1.0", translation.text)
                    card.text_widget.config(state="disabled")
                    
                    card.translation_text = translation.text
                    card.lang_code = lang_code
                    card.play_button.config(state="normal")
                except Exception as e:
                    card.text_widget.config(state="normal")
                    card.text_widget.delete("1.0", tk.END)
                    card.text_widget.insert("1.0", f"Translation error: {str(e)}")
                    card.text_widget.config(state="disabled")
            
            self.status_label.config(text="✓ Translation complete!", fg="#66cc66")
            
        except sr.WaitTimeoutError:
            self.status_label.config(text="⚠ No speech detected", fg="#ff9966")
        except sr.UnknownValueError:
            self.status_label.config(text="⚠ Could not understand audio", fg="#ff9966")
        except Exception as e:
            self.status_label.config(text=f"⚠ Error: {str(e)}", fg="#ff6666")
        finally:
            self.record_btn.config(state="normal", bg="#ff9966")
    
    def play_translation(self, language):
        card = self.translation_cards[language]
        if hasattr(card, 'translation_text'):
            thread = threading.Thread(target=self.play_audio, args=(card,))
            thread.daemon = True
            thread.start()
    
    def play_audio(self, card):
        try:
            card.play_button.config(state="disabled", text="⏸ Playing...")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
            
            tts = gTTS(text=card.translation_text, lang=card.lang_code)
            tts.save(temp_file)
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.unload()
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"Audio error: {e}")
        finally:
            card.play_button.config(state="normal", text="▶ Play")
    
    def clear_all(self):
        # Clear recognized text
        self.recognized_text.config(state="normal")
        self.recognized_text.delete("1.0", tk.END)
        self.recognized_text.insert("1.0", "Your speech will appear here...")
        self.recognized_text.config(state="disabled")
        
        # Clear all translation cards
        for card in self.translation_cards.values():
            card.text_widget.config(state="normal")
            card.text_widget.delete("1.0", tk.END)
            card.text_widget.insert("1.0", "Translation will appear here...")
            card.text_widget.config(state="disabled")
            
            if hasattr(card, 'translation_text'):
                delattr(card, 'translation_text')
            card.play_button.config(state="disabled")
        
        self.status_label.config(text="Ready to record", fg="#999999")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechTranslatorApp(root)
    root.mainloop()