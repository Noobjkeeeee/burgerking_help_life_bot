from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from services.user_service import (enable_user_reminders,
                                   save_user_reminder_time)
from utils.logger import logger


async def ask_time(message: types.Message):
    try:
        kb = ReplyKeyboardBuilder()
        for time in ["8.00", "13.00", "20.00", "22.00"]:
            kb.button(text=time)
        await message.answer(
            "Теперь мы будем присылать тебе небольшие"
            " приятные напоминания каждый день."
            " Выбери удобное время:",
            reply_markup=kb.as_markup(resize_keyboard=True),
        )
        logger.info(
            f"Пользователю {message.from_user.id} предложено выбрать время напоминаний"
        )
    except Exception as e:
        logger.warning(
            f"Ошибка в ask_time для пользователя {message.from_user.id}: {e}",
            exc_info=True,
        )


async def set_time(message: types.Message):
    try:
        selected_time = message.text

        await save_user_reminder_time(message.from_user.id, selected_time)

        confirmation_text = (
            "Отлично! 😊 Я буду напоминать тебе голосовать"
            " каждый день, пока идет акция .\n"
            "Голосовать просто — это пара кликов,"
            " но большая поддержка для фонда."
        )
        kb = ReplyKeyboardBuilder()
        kb.button(text="Покажи, как голосовать")
        kb.button(text="Хорошо, жду напоминаний")
        await message.answer(
            confirmation_text, reply_markup=kb.as_markup(resize_keyboard=True)
        )

        logger.info(
            f"Пользователь {message.from_user.id} установил время напоминаний: {selected_time}"
        )
    except Exception as e:
        logger.warning(
            f"Ошибка в set_time для пользователя {message.from_user.id}: {e}",
            exc_info=True,
        )


async def additional_response(message: types.Message):
    if message.text == "Хорошо, жду напоминаний":
        try:
            await enable_user_reminders(message.from_user.id)
            await message.answer(
                "Отлично! Завтра я пришлю тебе напоминание о голосовании 😊",
                reply_markup=ReplyKeyboardRemove(),
            )
            logger.info(
                f"Пользователь {message.from_user.id} подтвердил получение напоминаний"
            )
        except Exception as e:
            logger.warning(
                f"Ошибка при отправке дополнительного сообщения пользователю {message.from_user.id}: {e}",
                exc_info=True,
            )


def register_handlers(dp: Dispatcher):
    try:
        dp.message.register(
            ask_time, lambda msg: msg.text == "Хочу получать напоминания"
        )
        dp.message.register(
            set_time, lambda msg: msg.text in ["8.00", "13.00", "20.00", "22.00"]
        )
        dp.message.register(
            additional_response, lambda msg: msg.text == "Хорошо, жду напоминаний"
        )
        logger.info("Зарегистрированы обработчики ask_time и set_time")
    except Exception as e:
        logger.warning(
            f"Ошибка при регистрации обработчиков reminders.py: {e}", exc_info=True
        )
