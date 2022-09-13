from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    user_main_menu = State()
    user_get_course_info = State()
    user_get_name = State()
    user_get_number = State()
    user_get_number2 = State()
    user_have_experience = State()
    user_get_experience = State()