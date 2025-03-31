# ui.py

import tkinter as tk
from tkinter import ttk, scrolledtext
from llm_interface import LLMClient
import threading
import whisper
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os

class LLMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama LLM UI")
        self.root.geometry("800x600")

        self.models = ['llama3', 'mistral', 'gemma', 'codellama']
        self.llm = LLMClient(self.models[0])

        self.create_widgets()

    def apply_font(self):
        font_style = (self.font_family.get(), self.font_size.get())
        self.prompt_input.config(font=font_style)
        self.response_output.config(font=font_style)

    def create_widgets(self):
        # Model selection
        model_frame = tk.Frame(self.root)
        model_frame.pack(pady=10)

        tk.Label(model_frame, text="Select Model:").pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value=self.models[0])
        model_menu = ttk.Combobox(model_frame, textvariable=self.model_var, values=self.models, state="readonly")
        model_menu.pack(side=tk.LEFT)
        model_menu.bind("<<ComboboxSelected>>", self.on_model_change)

        # Whisper model selector
        tk.Label(model_frame, text=" | Whisper Model:").pack(side=tk.LEFT)
        self.whisper_model_var = tk.StringVar(value="base")
        whisper_options = ['tiny', 'base', 'small', 'medium', 'large']
        self.whisper_menu = ttk.Combobox(model_frame, textvariable=self.whisper_model_var, values=whisper_options, state="readonly")
        self.whisper_menu.pack(side=tk.LEFT)

        # Font Options
        font_frame = tk.Frame(self.root)
        font_frame.pack(pady=5)

        tk.Label(font_frame, text="Font:").pack(side=tk.LEFT)
        self.font_family = tk.StringVar(value="Arial")
        font_choices = ["Arial", "Courier", "Helvetica", "Times", "Comic Sans MS"]
        font_menu = ttk.Combobox(font_frame, textvariable=self.font_family, values=font_choices, state="readonly")
        font_menu.pack(side=tk.LEFT)

        tk.Label(font_frame, text=" Size:").pack(side=tk.LEFT)
        self.font_size = tk.IntVar(value=12)
        font_size_spin = tk.Spinbox(font_frame, from_=8, to=24, textvariable=self.font_size, width=5)
        font_size_spin.pack(side=tk.LEFT)

        # Apply font button
        apply_font_btn = tk.Button(font_frame, text="Apply Font", command=self.apply_font)
        apply_font_btn.pack(side=tk.LEFT, padx=10)

        # Prompt input
        prompt_label = tk.Label(self.root, text="Enter your prompt:")
        prompt_label.pack()
        self.prompt_input = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD)
        self.prompt_input.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.get_response)
        self.submit_button.pack(pady=10)

        # Voice buttons (Start + Stop)
        self.recording = False
        voice_frame = tk.Frame(self.root)
        voice_frame.pack(pady=10)

        self.voice_button = tk.Button(voice_frame, text="🎙️ Start Recording", command=self.start_recording)
        self.voice_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(voice_frame, text="🛑 Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # Response output
        response_label = tk.Label(self.root, text="Response:")
        response_label.pack()
        self.response_output = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.response_output.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    def on_model_change(self, event):
        selected_model = self.model_var.get()
        self.llm.set_model(selected_model)

    def format_response(self, text):
        # Split long lines into paragraphs, remove leading/trailing spaces
        lines = text.strip().split('\n')
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if line:
                formatted_lines.append(line)

        return "\n\n".join(formatted_lines)

    def get_response(self):
        prompt = self.prompt_input.get("1.0", tk.END).strip()
        if not prompt:
            return

        self.response_output.config(state=tk.NORMAL)
        self.response_output.delete("1.0", tk.END)
        self.response_output.insert(tk.END, "Generating response...\n")
        self.response_output.config(state=tk.DISABLED)

        self.root.update()

        response = self.llm.get_response(prompt)

        self.response_output.config(state=tk.NORMAL)
        self.response_output.delete("1.0", tk.END)
        formatted = self.format_response(response)
        self.response_output.insert(tk.END, formatted)
        self.response_output.config(state=tk.DISABLED)

    def start_recording(self):
        self.recording = True
        self.voice_button.config(state=tk.DISABLED, text="🎙️ Recording...")
        self.stop_button.config(state=tk.NORMAL)
        self.audio_data = []

        def callback(indata, frames, time, status):
            if self.recording:
                self.audio_data.append(indata.copy())
            else:
                raise sd.CallbackStop()

        self.stream = sd.InputStream(callback=callback, channels=1, samplerate=16000)
        self.stream.start()

    def stop_recording(self):
        self.recording = False
        self.voice_button.config(text="🎙️ Start Recording", state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.stream.stop()
        self.stream.close()
        self.transcribe_audio()

    def transcribe_audio(self):
        print("🎧 Transcribing with Whisper...")
        audio_np = np.concatenate(self.audio_data, axis=0)
        samplerate = 16000

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav.write(f.name, samplerate, (audio_np * 32767).astype(np.int16))
            audio_path = f.name

        try:
            model_size = self.whisper_model_var.get()
            model = whisper.load_model(model_size)
            print(f"[Whisper] Transcribing using model: {model_size}")
            result = model.transcribe(audio_path, verbose=False)
            text = result["text"].strip()

            print(f"[Whisper] Transcribed: {text}")
            self.prompt_input.delete("1.0", tk.END)
            self.prompt_input.insert(tk.END, text)

            self.get_response()  # auto-submit after speech

        except Exception as e:
            print(f"[Whisper Error] {e}")

        finally:
            os.remove(audio_path)
