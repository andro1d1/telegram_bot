import json
import requests
from pathlib import Path
from utils.cred_helper import get_value

winddirections = ("С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ")

def get_weather(city:str):
    """
    Returns current weather in city
    """
    with open(Path(Path().cwd(), 'settings', 'cities.json'), 'r', encoding='utf-8') as j:
        cities = json.load(j)
    print(Path(Path().cwd(), 'settings', 'cities.json'))
    try:
        api_key = get_value('OPEN_WEATHER_API')
        res = requests.get("https://api.openweathermap.org/data/2.5/weather", params={'q': cities[city.lower()], 'units': 'metric', 'lang': 'ru', 'appid': api_key})
        data = res.json()
        direction = int((data['wind']['deg'] + 22.5) // 45 % 8)
        result = f"Состояние: {(data['weather'][0]['description'])}\nТекущая температура: {data['main']['temp']}°C\nВетер: {data['wind']['speed']} м/с {winddirections[direction]}"
    except KeyError:
        result = "Вы ошиблись. Повторите снова."
    return result