import os

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand, BotCommandScopeDefault, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from handlers.reminders import ask_time
from utils.logger import logger


async def set_bot_commands(bot):
    commands = [BotCommand(
        command="start",
        description="Запуск бота и основное меню"
    )]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def cmd_start(message: types.Message):
    try:
        user_name = message.from_user.first_name or "друг"
        welcome_text = (
            f"<b>Привет, {user_name}!</b>\n\n"
            "Спасибо за твое желание не забывать"
            " поддерживать фонд «Я люблю жизнь» "
            "в приложении Burger King!\n\n"
            "Твой голос <b>конвертируется в реальные деньги для фонда</b>,"
            " а чем фонд финансово устойчивее, "
            "тем больше взрослых людей с онкологическим диагнозом"
            " смогут получить поддержку.\n\n"
            "<b>Вместе мы делаем борьбу с болезнью легче"
            " и находимся рядом с нашими подопечными "
            "в самые трудные моменты.</b>\n\n"
            '<i>нажми кнопку "Хочу получать напоминания"</i>'
        )

        IMAGE_PATH = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "pict.jpg")
        )
        photo = FSInputFile(IMAGE_PATH)
        kb = ReplyKeyboardBuilder()
        kb.button(text="Хочу получать напоминания")

        await message.answer_photo(
            photo=photo,
            caption=welcome_text,
            parse_mode="HTML",
            reply_markup=kb.as_markup(resize_keyboard=True),
        )

        logger.info(
            f"Команда /start выполнена пользователем {message.from_user.id}"
        )
    except Exception as e:
        logger.warning(
            f"Ошибка в cmd_start для пользователя {message.from_user.id}: {e}",
            exc_info=True,
        )


async def reminder_entry(message: types.Message):
    try:
        await ask_time(message)
        logger.info(f"Вызов напоминания пользователем {message.from_user.id}")
    except Exception as e:
        logger.warning(
            f"Ошибка в reminder_entry для пользователя"
            f" {message.from_user.id}: {e}",
            exc_info=True,
        )


def register_handlers(dp: Dispatcher):
    try:
        dp.message.register(cmd_start, Command(commands=["start"]))
        dp.message.register(
            reminder_entry, lambda msg: msg.text == "Хочу получать напоминания"
        )
        logger.info("Зарегистрированы обработчики start.py")
    except Exception as e:
        logger.warning(
            f"Ошибка при регистрации обработчиков в start.py: {e}",
            exc_info=True
        )
