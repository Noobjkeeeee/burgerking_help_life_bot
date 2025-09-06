from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import VOTING_URL


def voting_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Голосовать", url=VOTING_URL)
    return kb.as_markup()
