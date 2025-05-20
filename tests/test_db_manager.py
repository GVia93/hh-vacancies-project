import psycopg2
import pytest

from src.config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from src.db_manager import DBManager

TEST_DB_NAME = "test_hh_db"


@pytest.fixture(scope="module")
def db():
    """
    Фикстура для подключения к тестовой БД и возврата DBManager с очищенными таблицами.
    """
    conn = psycopg2.connect(dbname=TEST_DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("DELETE FROM vacancies;")
    cur.execute("DELETE FROM employers;")
    conn.commit()
    cur.close()
    conn.close()

    dbm = DBManager()
    return dbm


def test_insert_employers_and_vacancies(db: DBManager):
    """
    Тестирует метод insert_employers_and_vacancies:
    вставляет тестового работодателя с двумя вакансиями и проверяет, что данные записаны корректно.
    """
    test_data = [
        {
            "id": 999999,
            "name": "TestCompany",
            "vacancies": [
                {
                    "title": "Test Developer",
                    "salary_from": 100000,
                    "salary_to": 150000,
                    "currency": "RUR",
                    "url": "https://example.com/vacancy/1",
                },
                {
                    "title": "Junior Developer",
                    "salary_from": None,
                    "salary_to": 90000,
                    "currency": "RUR",
                    "url": "https://example.com/vacancy/2",
                },
            ],
        }
    ]
    db.insert_employers_and_vacancies(test_data)

    companies = db.get_companies_and_vacancies_count()
    assert any(c[0] == "TestCompany" and c[1] == 2 for c in companies), "Данные не вставлены корректно"


def test_get_all_vacancies(db: DBManager):
    """
    Проверяет, что метод возвращает все вакансии и среди них есть тестовые.
    """
    vacancies = db.get_all_vacancies()
    assert len(vacancies) >= 2
    assert any("Test Developer" in v["title"] for v in vacancies)


def test_get_avg_salary(db: DBManager):
    """
    Проверяет, что средняя зарплата рассчитывается корректно и является положительным числом.
    """
    avg = db.get_avg_salary()
    assert isinstance(avg, float)
    assert avg > 0


def test_get_vacancies_with_higher_salary(db: DBManager):
    """
    Проверяет, что метод возвращает вакансии с зарплатой выше средней.
    """
    vacancies = db.get_vacancies_with_higher_salary()
    assert isinstance(vacancies, list)
    assert all("salary" in v for v in vacancies)


def test_get_vacancies_with_keyword(db: DBManager):
    """
    Проверяет, что поиск по ключевому слову находит соответствующие вакансии.
    """
    results = db.get_vacancies_with_keyword("developer")
    assert isinstance(results, list)
    assert any("developer" in v["title"].lower() for v in results)
