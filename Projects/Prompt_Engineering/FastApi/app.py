from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI()

# Allow all origins for simplicity, restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NextGenAI - Hadas Prompt Engineering Study</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        .api-keys {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .api-keys input {
            width: 30%;
            padding: 10px;
            font-size: 16px;
        }
        .prompt-practice {
            margin-bottom: 20px;
        }
        .prompt-practice textarea {
            width: 100%;
            height: 100px;
            padding: 10px;
            font-size: 16px;
        }
        .prompt-practice button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        .prompt-practice button:hover {
            background-color: #0056b3;
        }
        .response-output {
            white-space: pre-wrap;
            background-color: #f9f9f9;
            padding: 10px;
            border: 1px solid #ddd;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>NextGenAI - Hadas Prompt Engineering Study</h1>
    <div class="api-keys">
        <input type="text" id="openai-api-key" placeholder="OpenAI API Key">
        <input type="text" id="anthropic-api-key" placeholder="Anthropic API Key">
        <input type="text" id="google-api-key" placeholder="Google API Key">
    </div>
    <div class="prompt-practice">
        <textarea id="prompt" placeholder="Enter your prompt here..."></textarea>
        <button onclick="submitPrompt()">Submit</button>
    </div>
    <div id="output" class="response-output"></div>
    <script>
        async function submitPrompt() {
            const prompt = document.getElementById('prompt').value;
            const openaiApiKey = document.getElementById('openai-api-key').value;

            const response = await fetch('/submit_prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt, openaiApiKey })
            });

            const data = await response.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return html_template

@app.post("/submit_prompt")
async def submit_prompt(request: Request):
    data = await request.json()
    prompt = data.get('prompt')
    openai_api_key = data.get('openaiApiKey')
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/engines/davinci-codex/completions',
            headers={'Authorization': f'Bearer {openai_api_key}'},
            json={
                'prompt': prompt,
                'max_tokens': 100
            }
        )
        response_json = response.json()
    except Exception as e:
        response_json = {'error': str(e)}

    return response_json

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
