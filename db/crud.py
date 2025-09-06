from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import User
from utils.logger import logger


async def crud_get_user_by_telegram_id(session: AsyncSession, telegram_id: str):
    try:
        result = await session.execute(
            select(User).filter(User.telegram_user_id == telegram_id)
        )
        user = result.scalars().first()
        logger.info(
            f"Получен пользователь с telegram_id={telegram_id}: {user}"
        )
        return user
    except Exception as e:
        logger.warning(
            f"Ошибка при получении пользователя с telegram_id={telegram_id}: {e}",
            exc_info=True,
        )
        return None


async def create_user(
    session: AsyncSession,
    telegram_id: str,
    reminder_time: str = None,
    first_interaction_date: date = None,
):
    try:
        user = User(
            telegram_user_id=telegram_id,
            reminder_time=reminder_time,
            first_interaction_date=first_interaction_date,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        logger.info(f"Создан пользователь с telegram_id={telegram_id}")
        return user
    except Exception as e:
        logger.warning(
            f"Ошибка при создании пользователя с telegram_id={telegram_id}: {e}",
            exc_info=True,
        )
        return None


async def update_user_reminder_time(
    session: AsyncSession, telegram_id: str, reminder_time: str
):
    try:
        user = await crud_get_user_by_telegram_id(session, telegram_id)
        if user:
            user.reminder_time = reminder_time
            await session.commit()
            await session.refresh(user)
            logger.info(
                f"Обновлено время напоминания для пользователя {telegram_id} на "
                f"{reminder_time}"
            )
        else:
            logger.warning(
                f"Пользователь с telegram_id={telegram_id} не найден для обновления"
            )
        return user
    except Exception as e:
        logger.warning(
            f"Ошибка при обновлении времени напоминания пользователя {telegram_id}: {e}",
            exc_info=True,
        )
        return None


async def update_user_first_interaction_date(
    session: AsyncSession, telegram_id: str, interaction_date: date
):
    try:
        user = await crud_get_user_by_telegram_id(session, telegram_id)
        if user:
            user.first_interaction_date = interaction_date
            await session.commit()
            await session.refresh(user)
            logger.info(
                f"Установлена дата первого взаимодействия для пользователя "
                f"{telegram_id}: {interaction_date}"
            )
        else:
            logger.warning(
                f"Пользователь с telegram_id={telegram_id} не найден для установки "
                f"даты первого взаимодействия"
            )
        return user
    except Exception as e:
        logger.warning(
            f"Ошибка при обновлении даты первого взаимодействия пользователя "
            f"{telegram_id}: {e}",
            exc_info=True,
        )
        return None


async def get_user_first_interaction_date(session: AsyncSession, telegram_id: str):
    try:
        result = await session.execute(
            select(User.first_interaction_date).filter(
                User.telegram_user_id == telegram_id
            )
        )
        date_val = result.scalar_one_or_none()
        return date_val
    except Exception as e:
        logger.warning(
            f"Ошибка при получении даты первого взаимодействия пользователя "
            f"{telegram_id}: {e}",
            exc_info=True,
        )
        return None


async def get_all_users_with_reminder(session: AsyncSession):
    try:
        result = await session.execute(
            select(User).filter(User.reminder_time.isnot(None))
        )
        users = result.scalars().all()
        return users
    except Exception as e:
        logger.warning(
            f"Ошибка при получении пользователей с напоминаниями: {e}",
            exc_info=True,
        )
        return []


async def enable_user_reminders(session: AsyncSession, telegram_id: str):
    try:
        user = await crud_get_user_by_telegram_id(session, telegram_id)
        if user:
            user.reminders_enabled = True
            await session.commit()
            await session.refresh(user)
            logger.info(f"Пользователю {telegram_id} включены напоминания")
        return user
    except Exception as e:
        logger.warning(
            f"Ошибка при включении напоминаний пользователю {telegram_id}: {e}",
            exc_info=True,
        )
        return None