import os
import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
import uvicorn

from config import BOT_TOKEN

from handlers import instructions, reminders, start
from handlers.start import set_bot_commands
from services.scheduler import schedule_daily_jobs
from services.user_service import load_users
from utils.logger import logger

bot = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
          )
dp = Dispatcher(storage=MemoryStorage())

bot_task = None

async def run_bot():
    """Запуск бота"""
    try:
        start.register_handlers(dp)
        reminders.register_handlers(dp)
        instructions.register_handlers(dp)
        asyncio.create_task(schedule_daily_jobs())

        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook удален, начинается polling")

        await set_bot_commands(bot)

        await dp.start_polling(bot)
    except Exception as exc:
        logger.error(f"Ошибка в основном цикле бота: {exc}", exc_info=True)
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot_task

    try:
        load_users()
        logger.info("Пользователи загружены из JSON")

        bot_task = asyncio.create_task(run_bot())
        logger.info("Бот запущен через FastAPI")

    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}", exc_info=True)
        raise

    yield

    if bot_task:
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            logger.info("Бот корректно остановлен")


app = FastAPI(
    title="BurgerKing Bot",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"status": "running", "service": "BurgerKing Telegram Bot"}


def run_fastapi():
    """Запуск FastAPI сервера с поддержкой переменных окружения"""
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"🚀 Starting server on {host}:{port}")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    run_fastapi()
