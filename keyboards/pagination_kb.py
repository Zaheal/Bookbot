from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import RU_LEXICON

# Функция, генерирующая клавиатуру для страницы книги
def create_pagination_kb(*buttons: str) -> InlineKeyboardMarkup:
    pagination_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    pagination_kb.row(*[InlineKeyboardButton(RU_LEXICON[button] if button in RU_LEXICON else button,
                        callback_data=button) for button in buttons])
    return pagination_kb