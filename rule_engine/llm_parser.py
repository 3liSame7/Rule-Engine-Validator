import os
import requests
import re
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-8b-8192"  # or "mixtral-8x7b-32768"

MANDATORY_KEYS = {"field", "operator", "value"}

def parse_rule_with_groq(prompt: str):
    if not GROQ_API_KEY:
        raise EnvironmentError("GROQ_API_KEY not found in environment variables")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that extracts rules as JSON."},
            {"role": "user", "content": prompt}
        ],
        "model": MODEL,
        "temperature": 0.1,
        "max_tokens": 512
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"LLM API Error: {response.status_code} — {response.text}")

    result = response.json()
    try:
        raw_output = result["choices"][0]["message"]["content"]
        return {"parsed_rule": extract_and_validate_json(raw_output)}
    except Exception as e:
        raise Exception(f"LLM parsing error: {str(e)}")


def extract_and_validate_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?", "", text).strip()

    braces = 0
    json_start = None
    for i, char in enumerate(text):
        if char == '{':
            if json_start is None:
                json_start = i
            braces += 1
        elif char == '}':
            braces -= 1
            if braces == 0 and json_start is not None:
                json_str = text[json_start:i+1]
                break
    else:
        raise ValueError("No complete JSON object found in model output.")

    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise Exception(f"LLM API Error: Failed to parse JSON: {e}")

    missing_keys = MANDATORY_KEYS - parsed.keys()
    if missing_keys:
        raise Exception(f"LLM API Error: Missing required keys: {missing_keys}")

    return parsed
