import time
import logging
import requests

from config import Config
from storage import load_conversations, save_conversations, append_message, reset_conversation
from glm_client import get_glm_reply

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("bot")


def get_updates(offset: int | None):
    params = {"timeout": Config.POLL_TIMEOUT}
    if offset is not None:
        params["offset"] = offset
    resp = requests.get(f"{Config.TELEGRAM_API}/getUpdates", params=params, timeout=Config.POLL_TIMEOUT + 10)
    resp.raise_for_status()
    return resp.json()["result"]


def send_message(chat_id: int, text: str):
    requests.post(
        f"{Config.TELEGRAM_API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=15,
    )


def handle_message(update: dict, conversations: dict) -> dict:
    message = update.get("message")
    if not message or "text" not in message:
        return conversations

    chat_id = str(message["chat"]["id"])
    text = message["text"].strip()

    if text == "/reset":
        conversations = reset_conversation(conversations, chat_id)
        send_message(int(chat_id), "تاریخچه‌ی مکالمه پاک شد.")
        return conversations

    if text == "/start":
        send_message(int(chat_id), "سلام! من یک دستیار هوش مصنوعی روی GLM-5.2 هستم. بپرس.")
        return conversations

    conversations = append_message(conversations, chat_id, "user", text)

    try:
        reply = get_glm_reply(conversations[chat_id])
    except Exception as e:
        log.exception("GLM request failed")
        send_message(int(chat_id), "خطا در ارتباط با مدل. لطفاً دوباره امتحان کن.")
        return conversations

    conversations = append_message(conversations, chat_id, "assistant", reply)
    send_message(int(chat_id), reply)
    return conversations


def main():
    log.info("Bot starting...")
    conversations = load_conversations()
    offset = None
    start_time = time.time()
    # هر چند پیام یک‌بار گیست را ذخیره می‌کنیم تا درخواست‌های API زیاد نشود
    updates_since_save = 0

    while time.time() - start_time < Config.MAX_RUNTIME_SECONDS:
        try:
            updates = get_updates(offset)
        except requests.exceptions.RequestException:
            log.warning("getUpdates failed, retrying in 5s")
            time.sleep(5)
            continue

        for update in updates:
            offset = update["update_id"] + 1
            conversations = handle_message(update, conversations)
            updates_since_save += 1

        if updates_since_save >= 3:
            save_conversations(conversations)
            updates_since_save = 0

    # ذخیره‌ی نهایی قبل از خروج (برای ری‌استارت بعدی توسط cron)
    save_conversations(conversations)
    log.info("Runtime limit reached, exiting cleanly for restart.")


if __name__ == "__main__":
    main()
