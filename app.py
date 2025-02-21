from flask import Flask, request, jsonify, render_template, Response, make_response
from flask_cors import CORS
import ollama
import traceback
import json
import os

#Version
VERSION = "2025-02-21:0"



#start flask app
app = Flask(__name__)
CORS(app)

# Load configuration
with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r', encoding='utf-8') as f:
    config = json.load(f)

def get_ollama_models():
    """Hämtar tillgängliga Ollama-modeller."""
    models = ollama.list()
    return [model["name"] for model in models["models"]]

def get_analysis_prompt(analysis_type, lang="sv"):
    """Returnerar lämplig prompt baserad på analystyp och språk."""
    print(f"DEBUG: Getting prompt for type={analysis_type}, lang={lang}")  # Debug logging
    
    try:
        # Check if analysis type exists in config
        if analysis_type not in config["prompts"]:
            print(f"DEBUG: Analysis type {analysis_type} not found in config")
            return config["prompts"]["html"][lang]["template"]
            
        # Get the prompt configuration for this analysis type
        prompt_config = config["prompts"][analysis_type]
        
        # If it's a dict with language keys
        if isinstance(prompt_config, dict) and ("sv" in prompt_config or "en" in prompt_config):
            if lang in prompt_config:
                print(f"DEBUG: Found {lang} template for {analysis_type}")
                return prompt_config[lang]["template"]
            elif "sv" in prompt_config:
                print(f"DEBUG: Falling back to Swedish template for {analysis_type}")
                return prompt_config["sv"]["template"]
        # If it's the old format with direct template
        elif "template" in prompt_config:
            print(f"DEBUG: Using legacy template format for {analysis_type}")
            return prompt_config["template"]
            
        print(f"DEBUG: No suitable template found for {analysis_type}, falling back to default")
        return config["prompts"]["html"][lang]["template"]
        
    except Exception as e:
        print(f"ERROR: Error getting prompt: {str(e)}")
        return config["prompts"]["html"][lang]["template"]

def analyze_content(code, model, analysis_type, lang="sv"):
    """Analyserar kod med vald Ollama-modell och analystyp."""
    prompt = get_analysis_prompt(analysis_type, lang)
    print(f"DEBUG: Analysis using lang={lang}, type={analysis_type}")
    print(f"DEBUG: Prompt start: {prompt[:100]}...")  # Print start of prompt for verification
    
    return ollama.generate(
        model=model, 
        prompt=f"{prompt}\n{code}", 
        stream=True
    )

@app.route("/")
def index():
    models = get_ollama_models()
    # Get language from query parameter or cookie, default to Swedish
    lang = request.args.get('lang', request.cookies.get('lang', 'sv'))
    
    # Validate language
    if lang not in config['languages']:
        lang = 'sv'
    
    response = make_response(render_template(
        "index.html",
        models=models,
        config=config,
        lang=lang
    ))
    
    # Set language cookie
    response.set_cookie('lang', lang)
    return response

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return "", 200, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }

    try:
        # Basic CORS headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
        
        data = request.json
        if not data:
            return jsonify({"error": config["languages"]["sv"]["ui"]["error"]["noData"]}), 400, headers

        code = data.get("code")
        model = data.get("model", "mistral")
        analysis_type = data.get("analysisType", "html")
        lang = data.get("lang", "sv")  # Get language from request

        print(f"Analyzing with lang={lang}, type={analysis_type}")  # Debug log

        if not code:
            return jsonify({"error": config["languages"][lang]["ui"]["error"]["noCode"]}), 400, headers

        def generate():
            try:
                start_msg = config["languages"][lang]["ui"]["startingAnalysis"]
                yield f"data: {json.dumps({'text': start_msg})}\n\n"
                #add prompt to start of analysis
                yield f"data: {json.dumps({'text': get_analysis_prompt(analysis_type, lang)+'<hr>' }) } \n\n "
                for response in analyze_content(code, model, analysis_type, lang):
                    if response and 'response' in response:
                        chunk = response['response']
                        if chunk:
                            yield f"data: {json.dumps({'text': chunk})}\n\n"
            except Exception as e:
                print(f"Error in generate: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(
            generate(),
            mimetype="text/event-stream",
            headers=headers
        )

    except Exception as e:
        print(f"Error in /analyze: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500, headers

if __name__ == "__main__":
    app.run(debug=False,port=5051,host='0.0.0.0')