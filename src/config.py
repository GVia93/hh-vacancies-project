import os

from dotenv import load_dotenv

load_dotenv()

# Параметры подключения к PostgreSQL
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


BASE_URL = "https://api.hh.ru"
EMPLOYER_IDS: list[int] = [
    80,  # Альфа-Банк
    3529,  # СБЕР
    78638,  # Т-Банк
    3776,  # МТС
    1740,  # Яндекс
    2748,  # Ростелеком
    2180,  # Ozon
    649691,  # Эд-АйТи
    3127,  # МегаФон
    84585,  # Авито
]
