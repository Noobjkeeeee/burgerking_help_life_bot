from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Хочу получать напоминания")
    kb.button(text="Покажи, как голосовать")
    kb.button(text="Хорошо, жду напоминаний")
    return kb.as_markup(resize_keyboard=True)
