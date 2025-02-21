# Web Code Analyzer with Ollama Integration

A web-based code analysis tool that uses Ollama AI models to analyze different types of code and provide structured feedback.

## Features

- Multiple language support (Swedish/English)
- Dark/Light theme
- Support for multiple code types:
  - HTML/SEO Analysis
  - CSS Analysis
  - JavaScript Analysis
  - PHP Analysis
  - Python Analysis
  - Java Analysis
  - C# Analysis
  - C++ Analysis
  - Shell Script Analysis
  - Bash Script Analysis
- Real-time streaming analysis
- URL analysis support
- Syntax highlighting
- Responsive design

## Installation

1. Clone the repository

2. Install the requirements:
   ```bash
   # Using pip3
   pip3 install -r requirements.txt

   # Or using pip with Python 3
   python3 -m pip install -r requirements.txt

   # On Windows
   py -3 -m pip install -r requirements.txt
   ```

3. Install and start Ollama:
   ```bash
   # On Linux/MacOS
   curl https://ollama.ai/install.sh | sh
   ollama serve

   # On Windows
   # Download and install from https://ollama.ai/download
   # Then start Ollama from the Windows Start Menu
   ```

4. Pull required models:
   ```bash
   ollama pull mistral
   # Or your preferred model
   ```

5. Start the application:
   ```bash
   # Using Python directly
   python3 app.py

   # Or using Flask
   flask run --port=5051 --host=0.0.0.0
   ```

6. Access the application at `http://localhost:5051`
