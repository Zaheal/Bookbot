from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon import RU_LEXICON
from services import book


def create_bookmarks_kb(*args: int) -> InlineKeyboardMarkup:
    bookmarks_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    #Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        bookmarks_kb.add(InlineKeyboardButton(
                            text=f'{button} - {book[button][:100]}',
                            callback_data=str(button)))
    # Добавляем в конце 2 кнопки "Редактировать" и "Отменить"
    bookmarks_kb.add(
        InlineKeyboardButton(
            text=RU_LEXICON['edit_bookmarks_button'],
            callback_data='edit_bookmarks'),
        InlineKeyboardButton(
            text=RU_LEXICON['cancel'],
            callback_data='cancel'
        ))
    return bookmarks_kb


def create_edit_kb(*args: int) -> InlineKeyboardMarkup:
    bookmarks_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    # Наполняем клавиатуру кнопками-закладками
    for button in sorted(args):
        bookmarks_kb.add(
            InlineKeyboardButton(
                text=f'{RU_LEXICON["del"]}{button} - {book[button][:100]}',
                callback_data=f'{button}del'
            ))
    # Добавляем кнопку "Отменить"
    bookmarks_kb.add(InlineKeyboardButton(
        text=RU_LEXICON['cancel'],
        callback_data='cancel'
    ))

    return bookmarks_kb