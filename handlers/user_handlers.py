import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from copy import deepcopy
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from database import user_dict_template, users_db
from keyboards import create_bookmarks_kb, create_edit_kb, create_pagination_kb
from lexicon import RU_LEXICON
from services import book


# Этот хэндлер срабатывает на команду /start
# Если его нет, добавляет пользователя в бд
# Отправляет приветственное письмо
async def process_start_command(message: Message):
    await message.answer(RU_LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер срабатывает на команду /help
# Отправляет пользователю сообщение со списком доступных команд
async def process_help_command(message: Message):
    await message.answer(RU_LEXICON[message.text])


# Этот хэндлер срабатывает на команду /beginning
# Отправляет первую страницу книги с кнопками пагинации
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(text=text, reply_markup=create_pagination_kb('backward', f'{users_db[message.from_user.id]["page"]}/{len(book)}', 'forward'))


# Этот хэндлер срабатывает на команду continue
# Отправляет пользователю страницу, на которой пользователь остановился
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )

# Этот хэндлер срабатывает на команду /bookmarks
# Отправляет список закладок, если они есть
# Отправляет сообщение о том, что закладок нет, если их нет)
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=RU_LEXICON[message.text],
            reply_markup=create_bookmarks_kb(
                *users_db[message.from_user.id]['bookmarks']
            )
        )
    else:
        await message.answer(text=RU_LEXICON['no_bookmarks'])

# Этот хэндлер срабатывает на нажатие инлайн-кнопки "вперед"
# Листает книгу вперед
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


# Этот хэндлер срабатывает на нажатие инлайн-кнопки "назад"
# Листает книгу назад
async def process_backward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
# с номером текущей страницы и добавляет закладку
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки')


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
# с закладкой из списка закладок
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )
    await callback.answer()


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
# "Редактировать" под списком закладок
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=RU_LEXICON[callback.data],
        reply_markup=create_edit_kb(
            *users_db[callback.from_user.id]['bookmarks']
        )
    )
    await callback.answer()


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
# "Отменить" во время работы со списком закладок
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=RU_LEXICON['cancel_text'])
    await callback.answer()


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
async def process_del_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=RU_LEXICON['/bookmarks'],
            reply_markup=create_edit_kb(
                *users_db[callback.from_user.id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(text=RU_LEXICON['no_bookmarks'])
    await callback.answer()


# Функция для регистрации хэндлеров пользователя в диспетчере
def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(process_beginning_command, commands=['beginning'])
    dp.register_message_handler(process_continue_command, commands=['continue'])
    dp.register_message_handler(process_bookmarks_command, commands=['bookmarks'])
    dp.register_callback_query_handler(process_forward_press, text="forward")
    dp.register_callback_query_handler(process_backward_press, text="backward")
    dp.register_callback_query_handler(process_page_press, lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
    dp.register_callback_query_handler(process_bookmark_press, lambda x: x.data.isdigit())
    dp.register_callback_query_handler(process_edit_press, text="edit_bookmarks")
    dp.register_callback_query_handler(process_cancel_press, text="cancel")
    dp.register_callback_query_handler(process_del_bookmark_press, lambda x: 'del' in x.data and x.data[:-3].isdigit())
