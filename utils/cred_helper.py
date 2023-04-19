import json
from pathlib import Path

def get_value(key):
    """
    Получает нужные API/TOKEN из json
    """
    with open(Path(Path().cwd(), 'secrets', 'credentials.json'), 'r', encoding='utf-8') as j:
        return json.load(j)[key]