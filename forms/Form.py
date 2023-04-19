from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    """
    Сохранение города при поиске погоды
    """
    city = State()
