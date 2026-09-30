"""Ollama local LLM integration service.

Enables local AI inference using Ollama (http://localhost:11434) as the base model
for executive summary generation, root-cause analysis, and customer feedback insights.
Auto-detects available models and falls back cleanly if Ollama is not running.
"""

import logging
import requests
import os
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")


def is_ollama_available() -> bool:
    """Check if local Ollama server is running and accessible."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def get_available_models() -> List[str]:
    """Retrieve list of locally pulled Ollama models."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return [m.get("name", "").split(":")[0] for m in data.get("models", [])]
    except Exception:
        pass
    return []


def select_best_model() -> str:
    """Select the best available installed model, or default to configured model."""
    models = get_available_models()
    if not models:
        return DEFAULT_OLLAMA_MODEL

    preferred = ["llama3.2", "llama3", "mistral", "gemma", "phi3", "llama2", "qwen"]
    for pref in preferred:
        for installed in models:
            if pref in installed.lower():
                return installed
    return models[0]


def generate_ollama_completion(prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> Optional[str]:
    """Send a prompt to local Ollama server and return the completion text.

    Args:
        prompt: User text prompt.
        system_prompt: System instruction.
        model: Specific Ollama model name, auto-detected if None.

    Returns:
        Completion text or None if request fails.
    """
    if not is_ollama_available():
        logger.info("Ollama server not reachable at %s", OLLAMA_BASE_URL)
        return None

    selected_model = model or select_best_model()
    payload: Dict[str, Any] = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
        }
    }
    if system_prompt:
        payload["system"] = system_prompt

    try:
        logger.info("Generating Ollama completion using model '%s'...", selected_model)
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=90
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("response", "").strip()
        else:
            logger.warning("Ollama API returned status %d: %s", resp.status_code, resp.text)
    except Exception as exc:
        logger.warning("Failed to reach Ollama completion endpoint: %s", exc)

    return None
