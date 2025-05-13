import time

import requests

BASE_URL = "https://api.hh.ru"
EMPLOYER_IDS: list[int] = [
    80,  # Альфа-Банк
    3529,  # Сбер
    78638,  # Тинькофф
    3776,  # МТС
    1740,  # Яндекс
    2748,  # Ozon
    2180,  # ВТБ
    649691,  # Wildberries
    9392522,  # VK (Mail.ru Group)
    3127,  # Tele2
]


def get_employers_with_vacancies() -> list[dict[str, any]]:
    """Получает данные о работодателях и их вакансиях с hh.ru.

    Returns:
        Список словарей, содержащих данные о работодателях и их вакансиях.
    """
    employers_data: list[dict[str, any]] = []

    for employer_id in EMPLOYER_IDS:
        employer_resp = requests.get(f"{BASE_URL}/employers/{employer_id}")
        if employer_resp.status_code != 200:
            print(f"Не удалось получить данные о работодателе {employer_id}")
            continue

        employer: dict[str, any] = employer_resp.json()

        vacancies: list[dict[str, any]] = []
        page: int = 0
        pages: int = 1

        while page < pages:
            resp = requests.get(
                f"{BASE_URL}/vacancies", params={"employer_id": employer_id, "page": page, "per_page": 100}
            )
            if resp.status_code != 200:
                break

            data = resp.json()
            pages = data.get("pages", 1)

            for item in data.get("items", []):
                salary = item.get("salary")
                vacancies.append(
                    {
                        "title": item["name"],
                        "salary_from": salary["from"] if salary and salary["from"] else None,
                        "salary_to": salary["to"] if salary and salary["to"] else None,
                        "currency": salary["currency"] if salary else None,
                        "url": item["alternate_url"],
                    }
                )

            page += 1
            time.sleep(0.1)

        employers_data.append({"id": employer["id"], "name": employer["name"], "vacancies": vacancies})

    return employers_data
