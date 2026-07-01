import os


class Config:
    # --- Telegram ---
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

        # --- Gemini (Google AI Studio) ---
    GLM_API_KEY = os.environ["GLM_API_KEY"].strip()
    GLM_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    GLM_MODEL = "gemini-2.5-flash"


    # --- GitHub Gist (حافظه‌ی مکالمات بین ری‌استارت‌ها) ---
    GIST_TOKEN = os.environ["GIST_TOKEN"]
    GIST_ID = os.environ["GIST_ID"]  # یک بار دستی گیست خالی بساز و آیدیش رو اینجا بذار
    GIST_FILENAME = "conversations.json"

    # --- کنترل هزینه ---
    MAX_HISTORY_MESSAGES = 8       # فقط ۸ پیام آخر هر کاربر رو نگه می‌داریم
    MAX_OUTPUT_TOKENS = 600        # سقف توکن خروجی هر پاسخ
    REASONING_EFFORT = "low"       # low برای چت معمولی، high فقط اگر لازم شد

    # --- اجرای بات ---
    MAX_RUNTIME_SECONDS = 5 * 3600 + 55 * 60  # ۵ ساعت و ۵۵ دقیقه، قبل از تایم‌اوت گیت‌هاب
    POLL_TIMEOUT = 30  # long polling تلگرام

    SYSTEM_PROMPT = (
        "تو یک دستیار هوش مصنوعی مفید، دقیق و مختصر هستی. "
        "به فارسی روان پاسخ بده مگر کاربر زبان دیگری استفاده کند."
    )
