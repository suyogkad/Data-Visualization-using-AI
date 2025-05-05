# app/ai.py
import os
import requests
from flask import current_app

def polish_prompt(raw_prompt: str) -> str:
    """
    Sends a rephrase instruction to the HF inference API.
    Falls back to raw_prompt on error or invalid output.
    """
    instruction = (
        "Please rephrase the following suggestion into a "
        "concise user instruction:\n\n"
        f"\"{raw_prompt}\"\n\n"
        "Rephrased instruction:"
    )

    url = current_app.config["HF_API_URL"]
    headers = {
        "Authorization": f"Bearer {current_app.config['HUGGINGFACE_API_TOKEN']}"
    }
    payload = {
        "inputs": instruction,
        "parameters": {"max_new_tokens": 64, "temperature": 0.3}
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list) and data and "generated_text" in data[0]:
            candidate = data[0]["generated_text"].strip()
        elif isinstance(data, dict) and "generated_text" in data:
            candidate = data["generated_text"].strip()
        else:
            return raw_prompt

        # Only use if it’s meaningfully different
        if len(candidate) > len(raw_prompt) + 5 and raw_prompt not in candidate:
            return candidate

    except Exception:
        pass

    return raw_prompt
