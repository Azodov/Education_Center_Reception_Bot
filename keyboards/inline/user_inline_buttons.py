from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Kursga yozilish", callback_data="order_course"),
            InlineKeyboardButton(text="📚 Kurslar", callback_data="show_courses")
        ],
        [
            InlineKeyboardMarkup(text="Bizning manzil", callback_data="show_address"),
            InlineKeyboardMarkup(text="Biz bilan bog'lanish", callback_data="show_contacts")
        ],
        [
            InlineKeyboardMarkup(text="📢 Yangiliklar", callback_data="show_news"),
            InlineKeyboardMarkup(text="📣 Biz haqimizda", callback_data="show_about")
        ]
    ]
)

back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Kursga yozilish", callback_data="order_course")
        ],
        [
            InlineKeyboardButton(text="🏠 Asosiy menyuga qaytish", callback_data="back_to_main_menu"),
        ]
    ]
)

yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data="yes"),
            InlineKeyboardButton(text="Yo'q", callback_data="no")
        ]
    ]
)

get_result = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Natijani olish", callback_data="get_result")
        ]
    ]
)
