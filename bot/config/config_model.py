from dataclasses import dataclass


@dataclass
class TgBot:
    bot_token: str

@dataclass
class DeepSeek:
    api: str


@dataclass
class Config:
    tg_bot: TgBot
    deepseek: DeepSeek