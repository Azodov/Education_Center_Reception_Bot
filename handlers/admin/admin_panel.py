from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin_inline_buttons import admin_main_menu
from loader import dp, db
from states.Admin_State import Admin_Access


@dp.callback_query_handler(text="admin_add_course", state=Admin_Access.admin_panel)
async def admin_add_course(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Yangi kurs nomini kiriting!")
    await Admin_Access.get_new_course_name.set()


@dp.message_handler(state=Admin_Access.get_new_course_name, content_types=types.ContentTypes.TEXT)
async def admin_add_course_name(message: types.Message, state: FSMContext):
    await state.update_data(course_name=message.text)
    await message.answer("Kurs haqida batafsil ma'lumot kiriting!")
    await Admin_Access.get_new_course_description.set()


@dp.message_handler(state=Admin_Access.get_new_course_description, content_types=types.ContentTypes.TEXT)
async def admin_add_course_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    course_name = data.get("course_name")
    course_description = message.text
    db.add_course(name=course_name, description=course_description)
    await message.answer("Yangi kurs muvaffaqiyatli qo'shildi!", reply_markup=admin_main_menu)
    await state.reset_data()
    await state.finish()
    await Admin_Access.admin_panel.set()


@dp.callback_query_handler(text="admin_delete_course", state=Admin_Access.admin_panel)
async def admin_delete_course(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    course = db.select_all_course()
    course_button = InlineKeyboardMarkup(row_width=1)

    for i in course:
        course_button.add(InlineKeyboardButton(text=i[0], callback_data=f"delete_course_{i[0]}"))

    course_button.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_panel"))

    await call.message.edit_text("O'chirish uchun kursni tanlang!", reply_markup=course_button)


@dp.callback_query_handler(text_contains="delete_course_", state=Admin_Access.admin_panel)
async def admin_delete_course(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    course_name = call.data.split("_")[2]
    try:
        db.delete_course(name=course_name)
        await call.message.edit_text(f"{course_name} kursi muvaffaqiyatli o'chirildi!", reply_markup=admin_main_menu)
        await Admin_Access.admin_panel.set()
    except Exception as e:
        print(e)
        await call.message.edit_text("Xatolik yuz berdi!", reply_markup=admin_main_menu)
        await Admin_Access.admin_panel.set()


@dp.callback_query_handler(text="admin_get_new_user_list", state=Admin_Access.admin_panel)
async def admin_get_new_user_list(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    course = db.select_all_course()
    course_button = InlineKeyboardMarkup(row_width=1)

    for i in course:
        course_button.add(InlineKeyboardButton(text=i[0], callback_data=f"get_new_user_list_{i[0]}"))
    course_button.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_panel"))

    await call.message.edit_text("Kursni tanlang!", reply_markup=course_button)


@dp.callback_query_handler(text_contains="get_new_user_list_", state=Admin_Access.admin_panel)
async def admin_get_new_user_list(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    course_name = call.data.split("_")[4]
    course_id = db.select_last_orders()
    await call.message.edit_text(f"{course_name} kursi uchun ro'yxatdan o'tgan foydalanuvchilar ro'yxati:")
    for i in course_id:
        if i[2] == str(course_name):
            await call.message.answer(f"Ism: {i[0]}\nRaqam: {i[1]}\nKurs: {i[2]}\nTest_Natijasi: {i[3]}")

    await call.message.answer("Kerakli bo'limni tanlang!", reply_markup=admin_main_menu)
    await Admin_Access.admin_panel.set()


@dp.callback_query_handler(text="admin_panel", state=Admin_Access.admin_panel)
async def admin_panel(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text("Admin paneliga xush kelibsiz!", reply_markup=admin_main_menu)
    await state.finish()
    await state.reset_data()
    await Admin_Access.admin_panel.set()
