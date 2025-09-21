from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from bot.database import User


async def save_user_to_db(
        session: AsyncSession,
        name: str,
        user_id: int,) -> User:
    existing_user = await session.scalar(
        select(User).where(User.user_id == user_id)
    )
    if existing_user:
        existing_user.name = name
        await session.commit()
        await session.refresh(existing_user)
        return existing_user
    new_user = User(
        user_id=user_id,
        name=name,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user