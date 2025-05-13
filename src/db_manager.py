import psycopg2

from src.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


class DBManager:
    """
    Класс для управления взаимодействием с базой данных PostgreSQL,
    включая загрузку данных и выполнение аналитических запросов.
    """

    def __init__(self):
        """
        Инициализирует соединение с базой данных и создаёт курсор.
        """
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def insert_employers_and_vacancies(self, employers_data: list[dict[str, any]]) -> None:
        """
        Загружает данные о работодателях и их вакансиях в базу данных.
        """
        for employer in employers_data:
            self.cur.execute(
                """
                INSERT INTO employers (employer_id, name)
                VALUES (%s, %s)
                ON CONFLICT (employer_id) DO NOTHING;
                """,
                (employer["id"], employer["name"]),
            )

            for vacancy in employer["vacancies"]:
                self.cur.execute(
                    """
                    INSERT INTO vacancies (
                        employer_id, title, salary_from, salary_to, currency, url
                    ) VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        employer["id"],
                        vacancy["title"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["currency"],
                        vacancy["url"],
                    ),
                )

    def get_companies_and_vacancies_count(self) -> list[tuple[str, int]]:
        """
        Возвращает список компаний и количество вакансий у каждой.
        """
        self.cur.execute(
            """
            SELECT e.name, COUNT(v.vacancy_id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
            ORDER BY e.name;
        """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self) -> list[dict[str, any]]:
        """
        Возвращает список всех вакансий с деталями.
        """
        self.cur.execute(
            """
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id;
        """
        )
        rows = self.cur.fetchall()
        return [
            {"company": row[0], "title": row[1], "salary": f"{row[2] or 0}–{row[3] or 0} RUB", "url": row[4]}
            for row in rows
        ]

    def get_avg_salary(self) -> float:
        """
        Вычисляет среднюю зарплату по всем вакансиям.
        """
        self.cur.execute(
            """
            SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0)
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
        """
        )
        result = self.cur.fetchone()
        return result[0] if result and result[0] else 0.0

    def get_vacancies_with_higher_salary(self) -> list[dict[str, any]]:
        """
        Возвращает вакансии с зарплатой выше средней по базе.
        """
        avg_salary = self.get_avg_salary()
        self.cur.execute(
            """
            SELECT title, salary_from, salary_to, url
            FROM vacancies
            WHERE ((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0) > %s;
        """,
            (avg_salary,),
        )
        rows = self.cur.fetchall()
        return [{"title": row[0], "salary": f"{row[1] or 0}–{row[2] or 0} RUB", "url": row[3]} for row in rows]

    def get_vacancies_with_keyword(self, keyword: str) -> list[dict[str, any]]:
        """
        Ищет вакансии по ключевому слову в названии.
        """
        self.cur.execute(
            """
            SELECT title, url
            FROM vacancies
            WHERE LOWER(title) LIKE %s;
        """,
            (f"%{keyword.lower()}%",),
        )
        return [{"title": row[0], "url": row[1]} for row in self.cur.fetchall()]

    def __del__(self):
        """
        Закрывает соединение и курсор при удалении объекта.
        """
        self.cur.close()
        self.conn.close()
