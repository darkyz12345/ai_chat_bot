from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, PollAnswer
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.util import await_only

from bot.database import Course
from sqlalchemy.orm import selectinload
import random

import math

from bot.client.client import ask_deepseek, get_client

# from bot.db.models import User, Question, QuizAnswer, UserPoll
from bot.database import db_funcs
# from bot.states import UserStates
# from bot.redis_utils import is_quiz_active

from bot.keyboards.keyboards import main_menu, get_courses_page, courses_menu, ai_bot_menu

router: Router = Router()

COURSES_PER_PAGE = 3


@router.message(CommandStart())
async def hello(msg: Message, session: AsyncSession):
    user = await db_funcs.save_user_to_db(
        session=session,
        name=msg.from_user.full_name,
        user_id=msg.from_user.id
    )
    await msg.answer(
        f"Привет, {user.name}! 👋\nДобро пожаловать в бота!",
        reply_markup=main_menu()
    )


@router.message(F.text == 'Помощь')
async def help(msg: Message):
    await msg.answer('''Это бот для помощи беременным женщинам
Здесь можно найти полезные курсы для беременных, а также пообщаться с чат-ботом, если есть какие-нибудь страхи по поводу беременности''')


@router.message(F.text == "Курсы")
async def show_courses(msg: Message, session: AsyncSession, state: FSMContext):
    result = await session.execute(select(Course))
    courses = result.scalars().all()
    total_pages = math.ceil(len(courses) / COURSES_PER_PAGE)

    page = 1
    text, _ = await get_courses_page(session, page, courses, COURSES_PER_PAGE, total_pages)

    # сохраняем состояние
    # await state.update_data(page=page, total_pages=total_pages, courses=courses)
    await state.update_data(page=page, total_pages=total_pages)
    await msg.answer(text, reply_markup=courses_menu(page, total_pages))


@router.message(F.text == "<- Назад")
async def prev_page(message: Message, session: AsyncSession, state: FSMContext):
    result = await session.execute(select(Course))
    courses = result.scalars().all()
    data = await state.get_data()
    page = data.get("page", 1)
    total_pages = data.get("total_pages", 3)

    if page > 1:
        page -= 1
        text, _ = await get_courses_page(session, page, courses, COURSES_PER_PAGE, total_pages)
        await state.update_data(page=page)
        await message.answer(text, reply_markup=courses_menu(page, total_pages))

@router.message(F.text == "Вперёд ->")
async def prev_page(message: Message, session: AsyncSession, state: FSMContext):
    result = await session.execute(select(Course))
    courses = result.scalars().all()
    data = await state.get_data()
    page = data.get("page", 1)
    total_pages = data.get("total_pages", 3)

    if page < total_pages:
        page += 1
        text, _ = await get_courses_page(session, page, courses, COURSES_PER_PAGE, total_pages)
        await state.update_data(page=page)
        await message.answer(text, reply_markup=courses_menu(page, total_pages))

@router.message(F.text=='Назад в меню')
async def to_menu(msg: Message):
    await msg.answer('Вы вернулись в главное меню', reply_markup=main_menu())

@router.message(F.text=='Чат-бот')
async def ai_chat(msg: Message):
    await msg.answer('напишите свой вопрос чат-боту.', reply_markup=ai_bot_menu())

@router.message(F.text & ~F.text.in_({"Курсы", "Чат-бот", "Назад в меню", "Помощь"}))
async def chat_with_ai(msg: Message, session: AsyncSession):
    """Хендлер для общения с ИИ"""
    user_text = msg.text

    # ответ от deepseek
    cl = get_client()
    ai_answer = await ask_deepseek(cl, user_text)

    # достаём все курсы
    result = await session.execute(select(Course))
    courses = result.scalars().all()

    if courses:
        if random.random() <= 0.1:
            recommended = random.choice(courses)
            ai_answer += f"\n\n👉 Советую обратить внимание на курс:\n<b>{recommended.title}</b>\n{recommended.link}"

    await msg.answer(ai_answer, parse_mode="HTML")