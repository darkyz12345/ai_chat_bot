from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.database import Course

import math


# Главное меню
def main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Курсы"), KeyboardButton(text="Чат-бот")],
            [KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True
    )
    return kb


# Меню курсов
def courses_menu(page: int, total_pages: int) -> ReplyKeyboardMarkup:
    if page == 1:
        # Первая страница — нет кнопки "Назад"
        keyboard = [
            [KeyboardButton(text="Вперёд ->")],
            [KeyboardButton(text="Чат-бот")],
            [KeyboardButton(text="Назад в меню")],
            [KeyboardButton(text="Помощь")]
        ]
    elif page == total_pages:
        # Последняя страница — нет кнопки "Вперёд"
        keyboard = [
            [KeyboardButton(text="<- Назад")],
            [KeyboardButton(text="Чат-бот")],
            [KeyboardButton(text="Назад в меню")],
            [KeyboardButton(text="Помощь")]
        ]
    else:
        # Промежуточные страницы — есть обе кнопки
        keyboard = [
            [KeyboardButton(text="<- Назад"), KeyboardButton(text="Вперёд ->")],
            [KeyboardButton(text="Чат-бот")],
            [KeyboardButton(text="Назад в меню")],
            [KeyboardButton(text="Помощь")]
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )



async def get_courses_page(session: AsyncSession, page: int, courses, courses_per_page, total_pages):
    result = await session.execute(select(Course))

    start = (page - 1) * courses_per_page
    end = start + courses_per_page
    page_courses = courses[start:end]

    text = "\n\n".join([f"<b>{c.title}</b>\n{c.link}" for c in page_courses])

    return text, total_pages

def ai_bot_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Курсы")],
            [KeyboardButton(text="Помощь")],
            [KeyboardButton(text="Назад в меню")]
        ],
        resize_keyboard=True
    )
    return kb