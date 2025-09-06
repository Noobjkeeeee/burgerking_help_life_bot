import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from db.database import init_db
from handlers import instructions, reminders, start
from handlers.start import set_bot_commands
from services.scheduler import schedule_daily_jobs
from utils.logger import logger

bot = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
          )
dp = Dispatcher(storage=MemoryStorage())


async def main():
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
        logger.warning(f"Ошибка в основном цикле бота: {exc}", exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(init_db())
        logger.info("База данных инициализирована успешно")
    except Exception as e:
        logger.warning(f"Ошибка инициализации базы данных: {e}", exc_info=True)
    try:
        asyncio.run(main())
    except Exception as e:
        logger.warning(f"Ошибка при запуске бота: {e}", exc_info=True)
