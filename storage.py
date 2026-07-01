"""
حافظه‌ی مکالمات را در یک GitHub Gist نگه می‌داریم، چون هر بار که Job در
GitHub Actions ری‌استارت می‌شود، حافظه‌ی محلی (RAM) از بین می‌رود.
ساختار فایل conversations.json:
{
  "123456789": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}],
  "987654321": [...]
}
"""
import json
import requests
from config import Config

GIST_API = f"https://api.github.com/gists/{Config.GIST_ID}"
HEADERS = {
    "Authorization": f"Bearer {Config.GIST_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def load_conversations() -> dict:
    resp = requests.get(GIST_API, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    files = resp.json()["files"]
    content = files[Config.GIST_FILENAME]["content"]
    return json.loads(content) if content.strip() else {}


def save_conversations(data: dict) -> None:
    payload = {
        "files": {
            Config.GIST_FILENAME: {"content": json.dumps(data, ensure_ascii=False, indent=2)}
        }
    }
    resp = requests.patch(GIST_API, headers=HEADERS, json=payload, timeout=15)
    resp.raise_for_status()


def append_message(data: dict, chat_id: str, role: str, content: str) -> dict:
    history = data.get(chat_id, [])
    history.append({"role": role, "content": content})
    # فقط آخرین N پیام را برای کنترل هزینه نگه میداریم
    data[chat_id] = history[-Config.MAX_HISTORY_MESSAGES:]
    return data


def reset_conversation(data: dict, chat_id: str) -> dict:
    data[chat_id] = []
    return data
