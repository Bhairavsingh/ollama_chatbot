
<a name="readme-top"></a>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

# 🧠 Ollama Chatbot UI with Whisper Voice Input

A fully interactive, local AI chatbot UI powered by [Ollama](https://ollama.com) and OpenAI’s [Whisper](https://github.com/openai/whisper). Paste or speak your prompt, select models on the fly, and receive formatted LLM responses — all in one beautiful Python GUI.

---
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

## 🚀 Features

### 💬 LLM Interface (via Ollama)
- Interact with local LLMs like `llama3`, `mistral`, `gemma`, etc.
- Model dropdown selector with instant switching
- Terminal logs show which model is used

### 🎙️ Voice Input (powered by Whisper)
- **Start/Stop Recording** mic input
- Select Whisper model (`tiny`, `base`, `small`, etc.)
- Real-time local transcription (no API calls)
- Auto-submit after voice input

### 🎨 Customization
- Prompt font selection (Arial, Courier, etc.)
- Font size control
- Clean, readable response formatting (with paragraph spacing)
- (Optional) Future support for syntax highlighting & markdown

---

## 📁 Folder Structure

```
ollama_chatbot/
├── main.py                # App launcher
├── ui.py                  # GUI logic
├── llm_interface.py       # Handles Ollama interactions
├── README.md              # This file
└── requirements.txt       # Dependency list
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This repo hots all code base for resume recreator. Currently there is only one template of resume format, but we will add more as we go.


### ⚙️ Installation

### 1. 🧱 Clone the repo
```bash
https://github.com/Bhairavsingh/ollama_chatbot.git
cd ollama_chatbot
```

### 2. 🐍 Set up virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. 📦 Install requirements
```bash
pip install -r requirements.txt
```

> If you don’t have a `requirements.txt`, create one:
```bash
pip install openai-whisper sounddevice numpy scipy tkinter ollama
```

### 4. 📥 Make sure your Whisper + Ollama models are ready
```bash
# Pull your desired LLMs with Ollama
ollama pull llama3
ollama pull mistral
# etc.

# Whisper will auto-download selected model on first run
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### 🖥️ Run the app
```bash
python main.py
```

### 👨‍💻 Interface

- Select an LLM model from the dropdown
- (Optional) Choose Whisper model for transcription
- Paste text or press `🎙 Start Recording`
- After speaking, click `🛑 Stop Recording`
- Transcription will auto-fill prompt & submit
- View formatted response in the output box

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🛣️ Roadmap

- [ ] Silence detection to auto-stop voice
- [ ] Markdown rendering & syntax highlighting in responses
- [ ] Chat history saving/export
- [ ] Theme toggle (light/dark)
- [ ] Web-based version with Flask or Streamlit

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🧠 Credits

- [Ollama](https://ollama.com) — local LLM backend
- [Whisper](https://github.com/openai/whisper) — local voice-to-text
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — UI

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📄 License

MIT License © 2025  
Built by [Your Name] — Enjoy your private AI assistant!

<p align="right">(<a href="#readme-top">back to top</a>)</p>


