import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base

logger = logging.getLogger("my_bot")

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"

try:
    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    logger.info("Асинхронный движок базы данных успешно создан")
except Exception as e:
    logger.warning(
        f"Ошибка при создании асинхронного движка базы данных: {e}",
        exc_info=True
    )
    raise


async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as exc:
        logger.warning(f"Ошибка в создании сессии БД: {exc}", exc_info=True)
        raise


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Инициализация базы данных завершена успешно")
    except Exception as exc:
        logger.warning(
            f"Ошибка при инициализации базы данных: {exc}", exc_info=True
        )
        raise
