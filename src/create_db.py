import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER


def create_database_and_tables(db_name: str) -> None:
    """
    Создаёт базу данных PostgreSQL и необходимые таблицы, если они ещё не существуют.

    Порядок действий:
    1. Подключается к системной базе 'postgres' для проверки существования целевой базы данных.
    2. Создаёт базу данных с именем `db_name`, если она отсутствует.
    3. Подключается к целевой базе данных.
    4. Создаёт таблицы:
        - employers (работодатели)
        - vacancies (вакансии, связанные с работодателями через внешний ключ)

    Аргументы:
        db_name (str): Имя базы данных, которую необходимо создать и инициализировать.
    """
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"База данных '{db_name}' создана.")
    else:
        print(f"База данных '{db_name}' уже существует.")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=db_name, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employers (
            employer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
            title TEXT NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            currency TEXT,
            url TEXT NOT NULL
        );
    """
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы успешно созданы.")
