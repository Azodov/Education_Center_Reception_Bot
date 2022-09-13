from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Yangi Kurs qo'shish", callback_data="admin_add_course"),
            InlineKeyboardButton(text="❌ Kursni o'chirish", callback_data="admin_delete_course")
        ],
        [
            InlineKeyboardButton(text="📝 Kursga Yozilganlar ro'yxati", callback_data="admin_get_new_user_list")
        ]
    ]
)
