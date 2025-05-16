from src.create_db import create_database_and_tables
from src.hh_api import get_employers_with_vacancies
from src.db_manager import DBManager
from src.config import DB_NAME
from src.user_interface import handle_user_input


def main():
    # 1. Создание базы данных и таблиц (если их нет)
    create_database_and_tables(DB_NAME)

    # 2. Подтверждение от пользователя
    confirm = input("\nХотите загрузить данные с hh.ru и обновить базу? (y/n): ").strip().lower()
    if confirm == "y":
        # 2.1 Получение данных с hh.ru
        employers_data = get_employers_with_vacancies()

        # 2.2 Сохранение данных в базу
        db = DBManager()
        db.insert_employers_and_vacancies(employers_data)
        print("База данных успешно обновлена.")
    else:
        db = DBManager()
        print("Пропущено обновление базы.")

    # 3. Запуск пользовательского меню
    handle_user_input(db)


if __name__ == "__main__":
    main()
