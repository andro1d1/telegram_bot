from aiogram.dispatcher.filters.state import State, StatesGroup

class FormExchange(StatesGroup):
    """
    Сохранение данных при конвертации валют
    """
    from_curr = State()
    to_curr = State()
    amount = State()