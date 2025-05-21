from src.db_manager import DBManager


def show_menu() -> None:
    """
    Выводит в консоль главное меню доступных действий для пользователя.
    """
    print("\nМеню:")
    print("1 — Показать компании и количество вакансий")
    print("2 — Показать все вакансии")
    print("3 — Показать среднюю зарплату по вакансиям")
    print("4 — Показать вакансии с зарплатой выше средней")
    print("5 — Поиск вакансий по ключевому слову")
    print("0 — Выход")


def handle_user_input(db: DBManager) -> None:
    """
    Обрабатывает ввод пользователя и вызывает соответствующие методы DBManager.
    """
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            print("\nКомпании и количество вакансий:")
            results = db.get_companies_and_vacancies_count()
            for name, count in results:
                print(f"{name}: {count} вакансий")

        elif choice == "2":
            print("\nВсе вакансии:")
            results = db.get_all_vacancies()
            for vacancy in results:
                print(f"{vacancy['company']} | {vacancy['title']} | {vacancy['salary']} | {vacancy['url']}")

        elif choice == "3":
            avg = db.get_avg_salary()
            print(f"\nСредняя зарплата по вакансиям: {avg:.2f} RUB")

        elif choice == "4":
            print("\nВакансии с зарплатой выше средней:")
            results = db.get_vacancies_with_higher_salary()
            for v in results:
                print(f"{v['title']} | {v['salary']} | {v['url']}")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ").strip()
            results = db.get_vacancies_with_keyword(keyword)
            if not results:
                print("Ничего не найдено.")
            else:
                print(f"\nВакансии по ключевому слову '{keyword}':")
                for v in results:
                    print(f"{v['title']} | {v['url']}")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Попробуйте снова.")
