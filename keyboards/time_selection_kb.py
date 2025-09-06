from aiogram.utils.keyboard import ReplyKeyboardBuilder


def time_selection_keyboard():
    kb = ReplyKeyboardBuilder()
    for time in ["8.00", "13.00", "20.00", "22.00"]:
        kb.button(text=time)
    return kb.as_markup(resize_keyboard=True)
