# HH Vacancies Project

Проект по сбору и анализу вакансий с сайта [hh.ru](https://hh.ru) с сохранением данных в PostgreSQL и управлением через текстовый интерфейс.

## Цель проекта

- Получить вакансии от 10 популярных российских работодателей через API hh.ru.
- Сохранить данные в PostgreSQL.
- Реализовать аналитику и фильтрацию через `DBManager`.
- Предоставить удобный CLI для взаимодействия с пользователем.

---

## Технологии

- Python 3.11+
- PostgreSQL
- psycopg2
- requests
- python-dotenv
- Poetry

---

## Структура проекта

```
hh_vacancies_project/
├── .env                  # Переменные окружения (не коммитить)
├── .gitignore
├── README.md
├── pyproject.toml        # Poetry: зависимости и настройки
├── main.py               # Точка входа
└── src/
    ├── config.py         # Параметры подключения и ID компаний
    ├── hh_api.py         # Получение данных через API hh.ru
    ├── create_db.py      # Создание БД и таблиц
    ├── db_manager.py     # Класс DBManager для работы с БД
    └── user_interface.py # CLI интерфейс
```

---

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/hh_vacancies_project.git
cd hh_vacancies_project
```

2. Установите Poetry и зависимости:
```bash
poetry install
```

3. Создайте файл `.env` и укажите параметры PostgreSQL:
```
DB_NAME=hh_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. Запустите приложение:
```bash
poetry run python main.py
```

---

## Возможности CLI

- Показать компании и количество вакансий
- Просмотреть все вакансии
- Узнать среднюю зарплату
- Найти вакансии с зарплатой выше средней
- Поиск по ключевым словам

---

## Особенности реализации

- Автоматическое создание БД и таблиц
- Внешние ключи между компаниями и вакансиями
- Безопасная работа с переменными окружения
- Реализация принципов SOLID
- Типизированный и документированный код
