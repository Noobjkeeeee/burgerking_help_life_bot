import os

from aiogram import Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import VOTING_URL
from utils.logger import logger

VIDEO_PATH = os.path.join(
    os.path.dirname(__file__), "..", "instruction_video.mp4"
)
VIDEO_PATH = os.path.normpath(VIDEO_PATH)


async def show_instructions(message: types.Message):
    try:
        instruction_text = (
            "Чтобы поддержать фонд «Я люблю жизнь»:\n"
            "1. Открой приложение Burger King с телефона\n"
            "2. Найди баннер «Тебе выбирать, кому помогать» на главной странице\n"
            "3. Выбери фонд «Я люблю жизнь» и нажмите «Голосовать» ✅\n\n"
            "Если у тебя нет приложения, скачай его по ссылке:\n"
            "[App Store](https://apps.apple.com/ru/app/%D0%B1%D1%83%D1%80%D0%B3%D0%B5%D1%80-%D0%BA%D0%B8%D0%BD%D0%B3-%D0%B0%D0%BA%D1%86%D0%B8%D0%B8-%D0%B4%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BA%D0%B0/id1257821028?mt=)\n"
            "[Google Play](https://play.google.com/store/apps/details?id=ru.burgerking)\n\n"
        )
        kb = InlineKeyboardBuilder()
        kb.button(text="ГОЛОСУЮ", url=VOTING_URL)

        await message.answer(
            instruction_text, reply_markup=kb.as_markup(), parse_mode="Markdown"
        )

        video = FSInputFile(VIDEO_PATH)
        await message.answer_video(video,
                                   caption="Видеоинструкция к голосованию"
                                   )

        logger.info(
            f"Показана текстовая и видео инструкция пользователю {message.from_user.id}"
        )

    except Exception as e:
        logger.warning(
            f"Ошибка при показе инструкции пользователю {message.from_user.id}: {e}",
            exc_info=True,
        )


def register_handlers(dp: Dispatcher):
    try:
        dp.message.register(
            show_instructions, lambda msg: msg.text == "Покажи, как голосовать"
        )
        logger.info("Зарегистрирован обработчик команды 'Покажи, как голосовать'")
    except Exception as e:
        logger.warning(
            f"Ошибка при регистрации обработчиков в instructions.py: {e}", exc_info=True
        )
