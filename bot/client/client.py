from openai import OpenAI
from environs import Env


def get_client(path=None):
    env = Env()
    env.read_env(path)
    api = env('DEEPSEEK_API')
    client = OpenAI(
        api_key=api,  # ключ от deepseek
        base_url="https://api.deepseek.com"  # базовый URL DeepSeek API
    )
    return client


async def ask_deepseek(client, prompt: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты — перинатальный психолог с большим опытом работы. "
                    "Твоё имя — Мария. Ты специализируешься на поддержке женщин "
                    "во время беременности, подготовки к родам и переходу к материнству. "
                    "Твой подход сочетает гуманистическую психологию, КПТ для работы с тревогой "
                    "и методы осознанности."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
