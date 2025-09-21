from bot.config.config_model import Config, TgBot, DeepSeek
from environs import Env

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        TgBot(bot_token=env("BOT_TOKEN")),
        DeepSeek(api=env("DEEPSEEK_API"))
    )