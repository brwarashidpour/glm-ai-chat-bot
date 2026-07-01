from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.GLM_API_KEY, base_url=Config.GLM_BASE_URL)


def get_glm_reply(history: list[dict]) -> str:
    """
    history: لیستی از پیام‌های {"role": "user"/"assistant", "content": "..."}
    سیستم‌پرامپت اینجا اضافه می‌شود و به GLM فرستاده می‌شود.
    """
    messages = [{"role": "system", "content": Config.SYSTEM_PROMPT}] + history

    response = client.chat.completions.create(
        model=Config.GLM_MODEL,
        messages=messages,
        max_tokens=Config.MAX_OUTPUT_TOKENS,
        temperature=0.7,
        extra_body={"reasoning_effort": Config.REASONING_EFFORT},
    )
    return response.choices[0].message.content
