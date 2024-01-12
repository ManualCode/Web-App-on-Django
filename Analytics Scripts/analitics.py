from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd
import requests
import math
import time


def calculate_salary(row):
    salary_from = row['salary_from']
    salary_to = row['salary_to']
    currency = row['salary_currency']
    published_at = row['published_at']

    if pd.isna(salary_from) and pd.isna(salary_to):
        return 0
    if pd.isna(salary_from):
        salary = math.floor(salary_to)
    elif pd.isna(salary_to):
        salary = math.floor(salary_from)
    else:
        salary = (salary_from + salary_to) / 2
    if currency == 'RUR':
        return salary

    date = pd.to_datetime(published_at, format="%Y-%m-%d")
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp', params={'date_req': date.strftime('%d/%m/%Y')})
    if response.status_code == 200:
        # df = pd.read_xml(StringIO(response.text), xpath='.//Valute')
        # exchange_rate = float(df[df['CharCode'] == currency]['VunitRate'].values[0].replace(',', '.'))
        root = ET.fromstring(response.text)
        valute = root.find(f".//Valute[CharCode='{currency}']")
        exchange_rate = float(valute.find("VunitRate").text.replace(',', '.'))
        #print((salary, currency, published_at, '-->', exchange_rate))
        if pd.isna(exchange_rate):
            return 0

        return salary * exchange_rate
    else:
        return 0


def calculate_salary_parallel(data):
    with ThreadPoolExecutor() as executor:
        results = executor.map(calculate_salary, data)
    return list(results)


def create_cur_data(csv='C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\files\\vacancies.csv'):
    data = pd.read_csv(csv, nrows=10000)
    start = time.time()
    #data['salary'] = data.apply(lambda row: calculate_salary(row['salary_from'], row['salary_to'], row['salary_currency'], row['published_at']), axis=1)
    data['salary'] = calculate_salary_parallel(data.to_dict('records'))
    data['published_at'] = data['published_at'].apply(lambda x: x[:10:])
    data['published_at'] = pd.to_datetime(data['published_at'], format="%Y-%m-%d")
    data['year'] = data['published_at'].dropna().dt.year
    data.to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\files\\vac.csv')
    end = time.time()
    print((end-start) * 10**3)
    return data


def filter_data(data):
    data = data[data['name'].str.lower().str.contains("|".join(['с#']), case=False, na=False)]
    return data


def get_salary_dynamics(data):
    salary_dynamics = data.fillna(0).groupby('year')['salary'].mean().astype(float).round().to_dict()

    if len(salary_dynamics) != 21:
        dict = {}
        for i in range(2003, 2024):
            if i in salary_dynamics:
                dict[i] = salary_dynamics[i]
            else:
                dict[i] = 0

        salary_dynamics = dict

    return salary_dynamics


def get_vacancies_dynamics(data):
    vacancy_dynamics = data.groupby('year')['name'].count().to_dict()
    if len(vacancy_dynamics) != 21:
        dict = {}
        for i in range(2003, 2024):
            if i in vacancy_dynamics:
                dict[i] = vacancy_dynamics[i]
            else:
                dict[i] = 0

        vacancy_dynamics = dict
    return vacancy_dynamics


def get_top_cities_salary(selected_data):
    df_area_salaries = selected_data.groupby(['area_name']).agg({'salary': 'mean', 'name': 'count'}).dropna().astype(float).round().astype(int).sort_values(by=['salary', 'area_name'], ascending=(False, True))
    df_area_salaries['name'] = df_area_salaries['name'] / df_area_salaries['name'].sum()
    df_area_salaries = df_area_salaries[df_area_salaries.name * 100 >= 1]
    city_salary = {key: value for key, value in list(df_area_salaries.to_dict()['salary'].items())[:10]}
    return city_salary


def get_top_cities_vacancies(selected_data):
    df_area_vacancies = selected_data.groupby(['area_name']).agg({'name': 'count'}).sort_values(by=['name', 'area_name'], ascending=(False, True))
    df_area_vacancies['name'] = df_area_vacancies['name'] / df_area_vacancies['name'].sum()
    df_area_vacancies = df_area_vacancies[df_area_vacancies.name * 100 >= 1]
    city_vacancy_ratio = {key: round(value, 4) for key, value in list(df_area_vacancies.to_dict()['name'].items())[:10]}

    return city_vacancy_ratio


def create_plot():
    data = create_cur_data()
    filtred_data = filter_data(data)
    fig, sub = plt.subplots(2, 2)

    #   1 ГРАФИК
    salary_dynamics = get_salary_dynamics(data)
    filtred_salary_dynamics = get_salary_dynamics(filtred_data)
    sub[0, 0].set_title(label="Уровень зарплат по годам", fontsize=8)
    sub[0, 0].bar(salary_dynamics.keys(), salary_dynamics.values())
    sub[0, 0].bar(salary_dynamics.keys(), filtred_salary_dynamics.values())
    sub[0, 0].legend(['средняя з/п', 'з/п C#'], fontsize=8)
    sub[0, 0].grid(axis='y')
    sub[0, 0].set_xticks([x for x in range(2003, 2024)], labels=[x for x in range(2003, 2024)],
                         rotation=90, fontsize=8)
    sub[0, 0].tick_params(axis='y', labelsize=8)

    #           2 ГРАФИК
    vacancies_dynamics = get_vacancies_dynamics(data)
    filtred_vacancies_dynamics = get_vacancies_dynamics(filtred_data)
    sub[0, 1].set_title(label="Количество вакансий по годам", fontsize=8)
    sub[0, 1].bar(vacancies_dynamics.keys(), vacancies_dynamics.values())
    sub[0, 1].bar(vacancies_dynamics.keys(), filtred_vacancies_dynamics.values())
    sub[0, 1].legend(['Количество вакансий', f'Количество вакансий C#'], fontsize=8)
    sub[0, 1].set_xticks([x for x in range(2003, 2024)], labels=[x for x in range(2003, 2024)],
                         rotation=90, fontsize=8)
    sub[0, 1].tick_params(axis='y', labelsize=8)

    #           3 ГРАФИК
    top_cities_salary = get_top_cities_salary(data)
    f = []
    for i in list(top_cities_salary.keys()):
        if ' ' in i: f.append('\n'.join(i.split(" ")))
        elif '-' in i: f.append('-\n'.join(i.split("-")))
        else: f.append(i)

    sub[1, 0].set_title(label="Уровень зарплат по городам", fontsize=8)
    sub[1, 0].barh(list(top_cities_salary.keys()), top_cities_salary.values())
    sub[1, 0].set_yticklabels(f, fontdict={'horizontalalignment': 'right',
                                                           'verticalalignment': 'center'})
    sub[1, 0].tick_params(axis='y', labelsize=6)
    sub[1, 0].tick_params(axis='x', labelsize=8)
    sub[1, 0].grid(axis='x')
    sub[1, 0].invert_yaxis()

    #           4 ГРАФИК
    top_cities_vacancies = get_top_cities_vacancies(data)
    top_cities_vacancies['Другие'] = 1 - sum(top_cities_vacancies.values())
    sub[1, 1].set_title(label="Доля вакансий по городам", fontsize=8)
    sub[1, 1].pie(top_cities_vacancies.values(), labels=top_cities_vacancies.keys(),
                  textprops={'fontsize': 6})
    sub[1, 1].axis('equal')
    fig.tight_layout()
    fig.show()
    return sub


print(create_cur_data())
