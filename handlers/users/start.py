from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.user_buttons import get_number
from keyboards.inline.admin_inline_buttons import admin_main_menu
from keyboards.inline.user_inline_buttons import main_menu
from states.Admin_State import Admin_Access
from states.user_state import UserState
from loader import dp, db


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    if int(message.from_user.id) == int(ADMINS[0]):
        await message.answer("Admin panelga xush kelibsiz!", reply_markup=admin_main_menu)
        await Admin_Access.admin_panel.set()


    elif not db.select_user(id=message.from_user.id):
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n"
                             f"Botga xush kelibsiz!\n"
                             f"Botdan foydalanish uchun Telefon raqamingizni jo'nating!", reply_markup=get_number)
        await UserState.user_get_number.set()
    else:
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n", reply_markup=main_menu)
        await UserState.user_main_menu.set()
