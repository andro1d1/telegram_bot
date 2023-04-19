import os
import random
import aiogram.utils.markdown as md
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from forms.Form import Form
from forms.FormExchange import FormExchange
import utils.keyboards as kb
from utils.exchange import get_rate
from utils.cred_helper import get_value
from utils.weather import get_weather

bot = Bot(token=get_value('TOKEN')) # Токен бота

dp = Dispatcher(bot, storage=MemoryStorage()) # Диспетчер для бота, нужен для хэндлеров

CURRENCIES = ['MGA', 'AFN', 'PAB', 'THB', 'VEF', 'MKD',
              'RSD', 'ZWD', 'USD', 'EUR', 'RUB', 'JPY', 
              'TRY', 'GBP', 'AUD', 'CAD', 'KRW'] # не полный список валют, для примера

@dp.message_handler(commands="start")
async def starting(message: types.Message):
    """
    Получение команды /start
    """
    await message.answer(f"Привет, {message.from_user.full_name}. Я умею кое-что. \nСмотри в меню доступные функции.", reply_markup=kb.main_menu)

async def create_poll(chat_id):
    """
    Создание опроса с вопросом question и вариантами ответов options
    """
    question = 'Какой цвет получится, если смешать желтый и синий?' # вопрос
    options = ['Красный', 'Зеленый', 'Черный'] # варианты ответов
    await bot.send_poll(chat_id, question=question, options=options, type=types.PollType.QUIZ, correct_option_id=1) # correct_option_id - выбрать правильный

@dp.message_handler(lambda message: message.text in ['Текущая погода', 'Конвертация валюты', 'Картинка ¯\_(ツ)_/¯', 'Текущий квиз'])
async def message_mainmenu(message: types.Message):
    """
    Обработка команд, присутствующих в главном меню
    """
    if message.text == 'Текущая погода':
        await Form.city.set()
        await message.reply("Введите название города")
    elif message.text == 'Конвертация валюты':
        await FormExchange.from_curr.set()
        await message.answer("Введите сокращение исходной валюты")   
    elif message.text == 'Картинка ¯\_(ツ)_/¯':
        photo = open("pics/" + random.choice(os.listdir("pics")), 'rb')
        await message.answer_photo(photo, caption=":)")
    elif message.text == 'Текущий квиз':
        chat_id = message.chat.id
        await create_poll(chat_id)

@dp.message_handler(state=Form.city)
async def process_weather(message: types.Message, state: FSMContext):
    """
    Передача значения города в функцию get_weather() и вывод полученной информации
    """
    await state.finish()
    await message.reply(get_weather(message.text))

@dp.message_handler(lambda message: message.text in CURRENCIES, state=FormExchange.from_curr)
async def process_from_curr(message: types.Message, state: FSMContext):
    """
    Обработка исходной валюты, готовность принять необходимую
    """
    async with state.proxy() as data:
        data['from_curr'] = message.text

    await FormExchange.next()
    await message.answer("Введите сокращение необходимой валюты")

@dp.message_handler(lambda message: message.text not in CURRENCIES, state=FormExchange.from_curr)
async def process_from_curr_invalid(message: types.Message, state: FSMContext):
    """
    Обработка исходной валюты, если не состоит в списке валют, необходимо ввести снова
    """
    return await message.answer("Введено неверное сокращение. Повторите снова")

@dp.message_handler(lambda message: message.text not in CURRENCIES, state=FormExchange.to_curr)
async def process_to_curr_invalid(message: types.Message, state: FSMContext):
    """
    Обработка необходимой валюты, если не состоит в списке валют, необходимо ввести снова
    """
    return await message.answer("Введено неверное сокращение. Повторите снова")

@dp.message_handler(lambda message: message.text in CURRENCIES, state=FormExchange.to_curr)
async def process_to_curr(message: types.Message, state: FSMContext):
    """
    Обработка необходимой валюты, готовность принять количество валюты
    """
    await FormExchange.next()
    await state.update_data(to_curr=message.text)
    await message.answer("Введите количество исходной валюты")

@dp.message_handler(lambda message: not message.text.isdigit(), state=FormExchange.amount)
async def process_exchange_invalid(message: types.Message):
    """
    Обработка количества исходной валюты, если не число, выводится соответствующее значение.
    """
    return await message.answer("Введите число!")

@dp.message_handler(state=FormExchange.amount)
async def process_exchange(message: types.Message, state: FSMContext):
    """
    Обработка полученной информации и передача в функции get_rate(), бот отправляет сообщение с полученной суммой.
    """
    async with state.proxy() as data:
        data['amount'] = message.text
        await bot.send_message(message.chat.id, md.text(
                                md.text('С учетом курса на сегодняшний день вы получите'), md.text(get_rate(data['from_curr'],data['to_curr'],data['amount']), md.text(data['to_curr']), sep=' ')), reply_markup=kb.main_menu)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True) # Запуск бота