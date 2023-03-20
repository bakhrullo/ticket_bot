from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStartState(StatesGroup):
    get_name = State()
    get_contact = State()
    get_code = State()


class UserMenuState(StatesGroup):
    get_menu = State()


class UserQuesState(StatesGroup):
    get_ques = State()


class UserBuyState(StatesGroup):
    get_sec = State()
    get_row = State()
    get_place = State()
    get_conf = State()
    get_pay_type = State()
    get_query = State()
    get_success = State()
