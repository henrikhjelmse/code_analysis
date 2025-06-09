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

5. **Configure the application:**

   Open `app.py` and update the following variables at the top of the file to match your environment:

   ```python
   listen_to_domain = "http://localhost:5051"  # Change to your domain if needed
   # Ollama config
   ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
   ollama_api_key = os.environ.get("OLLAMA_API_KEY", None)
   ```

   - `listen_to_domain`: Set this to the domain or address where your app will be running.
   - `ollama_host`: Set this if your Ollama server is running on a different host or port.
   - `ollama_api_key`: Set this if your Ollama instance requires an API key.

   You can also set these values using environment variables.

6. Start the application:
   ```bash
   python3 app.py
   # Or using Flask
   flask run --port=5051 --host=0.0.0.0
   ```

7. Access the application at `http://localhost:5051`

## Notes

- Make sure to update the configuration in `app.py` before running the application for the first time.
- For advanced configuration, see comments in `app.py`.
- Ollama must be running and the required models must be pulled before starting the web application.
