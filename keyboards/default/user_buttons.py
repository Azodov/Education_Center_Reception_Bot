from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


get_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni jo'natish", request_contact=True)
        ]
    ],
    resize_keyboard=True
)

