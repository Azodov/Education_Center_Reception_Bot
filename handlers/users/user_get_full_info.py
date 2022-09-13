from aiogram import types
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.user_buttons import get_number
from keyboards.inline.user_inline_buttons import main_menu, back_to_main_menu, yes_or_no, get_result
from states.user_state import UserState
from loader import dp, db, bot


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=UserState.user_get_number)
async def user_get_number(message: types.Message):
    await message.answer(f"Ro'yxatdan o'tish muaffaqiyatli yakunlandi", reply_markup=ReplyKeyboardRemove())

    await message.answer(f"Kerakli bo'limni tanlang!", reply_markup=main_menu)
    try:
        db.add_user(id=message.from_user.id, name=message.from_user.full_name, phone=message.contact.phone_number)
    except Exception as e:
        print(e)
        await bot.send_message(chat_id=ADMINS[0], text=e)
    await UserState.user_main_menu.set()


@dp.callback_query_handler(text_contains="show_courses", state=UserState.user_main_menu)
async def show_courses(call: types.CallbackQuery):
    await call.answer(cache_time=1)

    course = db.select_all_course()
    course_inline_button = InlineKeyboardMarkup(row_width=2)
    for item in course:
        course_inline_button.insert(InlineKeyboardButton(text=item[0], callback_data=f"show_course_{item[0]}"))
    await call.message.edit_text(f"Kurslar ro'yxati", reply_markup=course_inline_button)
    await UserState.user_get_course_info.set()


@dp.callback_query_handler(text_contains="show_course_", state=UserState.user_get_course_info)
async def show_course_info(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    course_name = call.data.split("_")[2]
    await state.update_data(course_name=course_name)
    course_info = db.select_course(name=course_name)
    await call.message.edit_text(f"{course_info[0]}\n\n{course_info[1]}", reply_markup=back_to_main_menu)


@dp.callback_query_handler(text_contains="back_to_main_menu", state=UserState.user_get_course_info)
async def back_to_main_menu_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.delete()
    await call.message.answer(f"Kerakli bo'limni tanlang!", reply_markup=main_menu)
    await UserState.user_main_menu.set()


@dp.callback_query_handler(text_contains="order_course", state=UserState.user_get_course_info)
async def order_course(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Ismingizni kiriting")
    await UserState.user_get_name.set()


@dp.message_handler(state=UserState.user_get_name, content_types=types.ContentTypes.TEXT)
async def user_get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Siz bilan bog'lanishimiz uchun telefon raqamingizni kiriting yoki jo'nating",
                         reply_markup=get_number)
    await UserState.user_get_number2.set()


@dp.message_handler(state=UserState.user_get_number2, content_types=types.ContentTypes.TEXT)
@dp.message_handler(state=UserState.user_get_number2, content_types=types.ContentTypes.CONTACT)
async def user_get_number(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.CONTACT:
        number = message.contact.phone_number
    else:
        number = message.text
    await state.update_data(number=number)
    await message.answer("Siz ushbu kurs haqida malumotga egamisiz?", reply_markup=yes_or_no)
    await UserState.user_have_experience.set()


@dp.callback_query_handler(text_contains="no", state=UserState.user_have_experience)
async def user_have_experience(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    name = data.get("name")
    number = data.get("number")
    course_name = data.get("course_name")
    try:
        db.add_user_course(name=name, number=number, course_name=course_name, test_result="Test Bajarilmadi")
    except Exception as e:
        print(e)
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Kursga buyurtma berdi\n\nIsmi: {name}\nTelefon raqami: {number}\nKurs nomi: {course_name}")
    await call.message.edit_text("Sizning buyurtmangiz qabul qilindi!")
    await call.message.answer(f"Kerakli bo'limni tanlang!", reply_markup=main_menu)
    await UserState.user_main_menu.set()


@dp.callback_query_handler(text_contains="yes", state=UserState.user_have_experience)
async def user_solve_tests(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    test_url = "https://forms.gle/3JZ7Z7Z7Z7Z7Z7Z7Z?id="+str(call.from_user.id)
    await call.message.edit_text("Sizga test beriladi!")
    await call.message.answer("Testni bajarish uchun quydagi manzilga kiring!\n"
                              "Test yakunlangach Natijani olish tugmani bosing!"
                              f"{test_url}", reply_markup=get_result)
    await UserState.user_get_experience.set()

@dp.callback_query_handler(state=UserState.user_get_experience, text_contains="get_result")
async def user_get_experience(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    result = "5 ta savoldan 4 ta to'g'ri javob berdi"
    name = data.get("name")
    number = data.get("number")
    course_name = data.get("course_name")

    try:
        db.add_user_course(name=name, number=number, course_name=course_name, test_result=result)
        await bot.send_message(chat_id=ADMINS[0],
                               text=f"Kursga buyurtma berdi\n\nIsmi: {name}\nTelefon raqami: {number}\nKurs nomi: {course_name} \nNatija: {result}")
        await call.message.edit_text("Sizning buyurtmangiz qabul qilindi! siz bilan tez orada bog'lanamiz!\n"
                                     "Test natijasi: "+result+"ngiz")
        await call.message.answer(f"Kerakli bo'limni tanlang!", reply_markup=main_menu)
        await state.reset_data()
        await state.finish()
        await UserState.user_main_menu.set()
    except Exception as e:
        print(e)
        await call.message.edit_text("Xatolik yuz berdi!")



