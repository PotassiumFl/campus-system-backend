import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env", override=True)


class LlmError(Exception):
    pass


def _client() -> OpenAI:
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key or api_key == "your_key":
        raise LlmError("LLM_API_KEY is not configured")
    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url, timeout=60.0)


def _model() -> str:
    return os.environ.get("LLM_MODEL", "gpt-4o-mini")


def chat_with_tools(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None,
) -> Any:
    try:
        client = _client()
        kwargs: dict[str, Any] = {
            "model": _model(),
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message
    except LlmError:
        raise
    except Exception as exc:
        raise LlmError(f"LLM request failed: {exc}") from exc


def chat_completion(messages: list[dict[str, Any]]) -> str:
    message = chat_with_tools(messages, tools=None)
    content = message.content
    if content is None or content.strip() == "":
        raise LlmError("LLM returned empty content")
    return content.strip()
