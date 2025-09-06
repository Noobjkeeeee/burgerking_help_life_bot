from contextlib import asynccontextmanager
from datetime import datetime, timezone

from db.crud import (
    create_user,
    crud_get_user_by_telegram_id,
    enable_user_reminders as crud_enable_user_reminders,
    get_all_users_with_reminder,
    get_user_first_interaction_date as db_get_user_first_interaction_date,
    update_user_first_interaction_date,
    update_user_reminder_time,
)
from db.database import get_db
from utils.logger import logger


@asynccontextmanager
async def get_session():
    try:
        async for session in get_db():
            yield session
    except Exception as e:
        logger.warning(f"Ошибка при получении сессии БД: {e}", exc_info=True)
        raise


async def save_user_reminder_time(user_id: int, time: str):
    try:
        async with get_session() as session:
            user = await crud_get_user_by_telegram_id(session, str(user_id))
            if user is None:
                await create_user(session, str(user_id), time)
                await update_user_first_interaction_date(
                    session,
                    str(user_id),
                    datetime.now(timezone.utc).date(),
                )
                logger.info(
                    f"Создан новый пользователь с telegram_id={user_id} и временем "
                    f"напоминания {time}"
                )
            else:
                await update_user_reminder_time(session, str(user_id), time)
                logger.info(
                    f"Обновлено время напоминания для пользователя telegram_id={user_id} на "
                    f"{time}"
                )
    except Exception as e:
        logger.warning(
            f"Ошибка при сохранении времени напоминания для пользователя {user_id}: {e}",
            exc_info=True,
        )
        raise


async def get_all_users_with_reminders():
    try:
        async with get_session() as session:
            users = await get_all_users_with_reminder(session)
            return users
    except Exception as e:
        logger.warning(
            f"Ошибка при получении пользователей с напоминаниями: {e}",
            exc_info=True,
        )
        return []


async def get_user_first_interaction_date(user_id: int):
    try:
        async with get_session() as session:
            date = await db_get_user_first_interaction_date(session, str(user_id))
            return date
    except Exception as e:
        logger.warning(
            f"Ошибка при получении даты первого взаимодействия для пользователя "
            f"{user_id}: {e}",
            exc_info=True,
        )
        return None


async def enable_user_reminders(user_id: int):
    try:
        async with get_session() as session:
            user = await crud_enable_user_reminders(session, str(user_id))
            return user
    except Exception as e:
        logger.warning(
            f"Ошибка при включении напоминаний пользователя {user_id}: {e}",
            exc_info=True,
        )
        return None


async def get_user_by_telegram_id(user_id: int):
    try:
        async with get_session() as session:
            user = await crud_get_user_by_telegram_id(session, str(user_id))
            return user
    except Exception as e:
        logger.warning(
            f"Ошибка при получении пользователя {user_id}: {e}", exc_info=True
        )
        return None