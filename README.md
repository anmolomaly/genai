# Grammarly-Lite 📝

Grammarly-Lite is a lightweight, AI-powered writing assistant built with Streamlit and Ollama. It provides a suite of tools for summarization, grammar correction, and creative content generation, all running locally on your machine.

## 🚀 Features

- **Grammar Correction:** Fix spelling, punctuation, and grammar without changing the original intent.
- **Text Summarization:** Condense long articles or documents into short, medium, or detailed summaries.
- **Creative Generation:** Generate stories, emails, or marketing copy based on custom prompts.
- **File Support:** Upload `.pdf` or `.txt` files to extract and process text directly.
- **Local AI:** Powered by Ollama (`llama3`), ensuring your data stays private and local.
- **Customizable:** Adjust output length and tone/style to suit your needs.

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:

1. **Python 3.8+**
2. **Ollama:** [Download and install Ollama](https://ollama.com/)
3. **Pull the Llama3 Model:**
   ```bash
   ollama pull llama3
   ```

## 📦 Installation

1. Clone or download this repository.
2. Navigate to the project directory.
3. Install the required Python packages:
   ```bash
   pip install streamlit pypdf ollama
   ```

## 🏃 How to Run

1. Start the Ollama server (usually runs automatically after installation).
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to the local URL provided (typically `http://localhost:8501`).

## 📁 Project Structure

- `app.py`: The main application and UI logic.
- `llm_engine.py`: Functions for communicating with the Ollama API.
- `pdfreader.py`: Utility for extracting text from PDF and TXT files.
- `llm.py`: Development script for the LLM engine.

## 🎨 UI Aesthetics
The app features a custom "Olive/Dark" theme with glassmorphism-inspired elements for a premium user experience.

---
*Built with ❤️ using Streamlit and Ollama.*
