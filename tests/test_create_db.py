import psycopg2
import pytest

from src.config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from src.create_db import create_database_and_tables

TEST_DB_NAME = "test_hh_db"


@pytest.fixture(scope="module")
def connection():
    """
    Фикстура создаёт базу данных и подключается к ней один раз на весь модуль тестов.
    Возвращает объект соединения с тестовой БД.
    """
    create_database_and_tables(TEST_DB_NAME)
    conn = psycopg2.connect(dbname=TEST_DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    yield conn
    conn.close()


def test_employers_table_exists(connection):
    """
    Проверяет, что таблица 'employers' существует в схеме test_hh_db.
    """
    cur = connection.cursor()
    cur.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'employers'
        );
    """
    )
    result = cur.fetchone()[0]
    cur.close()
    assert result, "Таблица employers не создана"


def test_vacancies_table_exists(connection):
    """
    Проверяет, что таблица 'vacancies' существует в схеме test_hh_db.
    """
    cur = connection.cursor()
    cur.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'vacancies'
        );
    """
    )
    result = cur.fetchone()[0]
    cur.close()
    assert result, "Таблица vacancies не создана"


def test_foreign_key_exists(connection):
    """
    Проверяет, что в таблице 'vacancies' существует внешний ключ на 'employers'.
    """
    cur = connection.cursor()
    cur.execute(
        """
        SELECT constraint_name
        FROM information_schema.table_constraints
        WHERE table_name = 'vacancies' AND constraint_type = 'FOREIGN KEY';
    """
    )
    result = cur.fetchone()
    cur.close()
    assert result is not None, "Связь FOREIGN KEY между vacancies и employers отсутствует"
