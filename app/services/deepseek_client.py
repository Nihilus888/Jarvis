import requests

DEESEEK_API_URL = "http://localhost:11434/api/generate"

PROMPT_TEMPLATE = """
You are Jarvis, an intelligent and helpful AI assistant.
Answer clearly, concisely, and accurately but also with a touch of personality
like Jarvis from Iron Man.

User question:
{user_prompt}

Jarvis:"""


def generate_text_with_deepseek(user_prompt: str) -> str:
    prompt = PROMPT_TEMPLATE.format(user_prompt=user_prompt)
    payload = {
        "model": "deepseek-llm",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(DEESEEK_API_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    text = data.get("response", "")
    return text
