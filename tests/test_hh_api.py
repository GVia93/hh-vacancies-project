from unittest.mock import patch

from src.config import EMPLOYER_IDS
from src.hh_api import get_employers_with_vacancies


@patch("src.hh_api.requests.get")
def test_get_employers_with_vacancies_success(mock_get):
    """
    Тест успешного получения работодателя и вакансий.
    """
    employer_data = {"id": 123, "name": "Test Corp"}
    vacancies_data = {
        "pages": 1,
        "items": [
            {
                "name": "Python Developer",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "alternate_url": "https://hh.ru/vacancy/1",
            },
            {"name": "Data Analyst", "salary": None, "alternate_url": "https://hh.ru/vacancy/2"},
        ],
    }

    mock_get.side_effect = [MockResponse(employer_data, 200), MockResponse(vacancies_data, 200)]

    EMPLOYER_IDS.clear()
    EMPLOYER_IDS.append(123)

    result = get_employers_with_vacancies()

    assert len(result) == 1
    assert result[0]["id"] == 123
    assert result[0]["name"] == "Test Corp"
    assert len(result[0]["vacancies"]) == 2
    assert result[0]["vacancies"][0]["title"] == "Python Developer"
    assert result[0]["vacancies"][1]["salary_from"] is None


@patch("src.hh_api.requests.get")
def test_employer_not_found(mock_get):
    """
    Тест обработки случая, когда работодатель не найден (404).
    """
    mock_get.return_value = MockResponse({}, 404)

    EMPLOYER_IDS.clear()
    EMPLOYER_IDS.append(999)

    result = get_employers_with_vacancies()
    assert result == []


class MockResponse:
    """
    Мок-объект ответа requests.
    """

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
