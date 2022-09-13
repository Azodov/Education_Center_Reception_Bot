from aiogram.dispatcher.filters.state import State, StatesGroup

class Admin_Access(StatesGroup):
    admin_panel = State()
    get_new_course_name = State()
    get_new_course_description = State()