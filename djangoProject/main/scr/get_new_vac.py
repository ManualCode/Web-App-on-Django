import math
import re
import requests


def calculate_salary(salary_from, salary_to, currency):
    if salary_from is None:
        salary = math.floor(salary_to)
    elif salary_to is None:
        salary = math.floor(salary_from)
    else:
        salary = (salary_from + salary_to) / 2

    return f'{str(salary)} {currency}'


def get_vacancies():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "c# OR c charp OR с# OR шарп",
        "period": "1"
    }
    response = requests.get(url, params=params)
    data = response.json()

    vacancies = []
    for item in data.get("items", []):
        vacancy_id = item.get("id")
        vacancy_url = f"https://api.hh.ru/vacancies/{vacancy_id}"
        vacancy_response = requests.get(vacancy_url)
        vacancy_data = vacancy_response.json()
        vacancy = {
            "id": item.get('id'),
            "name": item.get("name"),
            "Описание(SPASE)вакансии": (re.sub(re.compile('<.*?>'), '', vacancy_data.get("description"))).replace('&quot;', ''),
            "Навыки": ", ".join(skill.get("name") for skill in vacancy_data.get("key_skills", [])),
            "Компания": item.get("employer", {}).get("name"),
            "Оклад": calculate_salary(item.get("salary").get("from"),
                                      item.get("salary").get("to"),
                                      item.get("salary").get("currency"))
            if item.get("salary") is not None else 'Неизвестно',
            "Название(SPASE)региона": item.get("area", {}).get("name"),
            "Дата(SPASE)публикации(SPASE)вакансии": item.get("published_at")
        }
        vacancies.append(vacancy)

    return sorted(vacancies, key=lambda x: x["Дата(SPASE)публикации(SPASE)вакансии"])