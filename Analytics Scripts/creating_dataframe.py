import xml.etree.ElementTree as ET
import pandas as pd
import requests
import math
import time


def parse_all_id():
    dictionary = {}
    response = requests.get('https://www.cbr.ru/scripts/XML_valFull.asp')
    root = ET.fromstring(response.text)

    for record in root.findall('Item'):
        id = record.get('ID')
        char_code = record.find('ISO_Char_Code').text
        dictionary[char_code] = id

    return dictionary


def create_dict_of_all_currency(dict_of_id):
    result_dict = {}
    for code in dict_of_id.values():
        response = requests.get(f'https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=24/01/2003&date_req2=01/01/2024&VAL_NM_RQ={code}')
        if response.status_code != 200:
            continue
        dictionary = {}
        root = ET.fromstring(response.text)
        for record in root.findall('Record'):
            date = '-'.join(record.get('Date').split('.')[::-1])
            vunitrate = record.find('VunitRate').text
            dictionary[date] = vunitrate

        result_dict[code] = dictionary

    return result_dict


def calculate_salary(d, salary_from, salary_to, currency, published_at):
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

    if published_at[:10] in d[currency]:
        exchange_rate = float(d[currency][published_at[:10]].replace(',', '.'))
    else:
        exchange_rate = float(d[currency][f'01{published_at[2:10]}'].replace(',', '.'))
    salary = round(salary * exchange_rate, 2)
    if salary <= 1_500_000:
        return salary
    else:
        return 0


def convert_currency_to_id(dictionary, x):
    if x == 'BYR':
        x = 'BYN'
    if not pd.isna(x):
        if x == 'RUR':
            return 'RUR'
        return dictionary[x]
    else:
        return ''


def create_cur_data(csv='C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\files\\vacancies.csv'):
    start = time.time()
    data = pd.read_csv(csv)
    dict_of_id = parse_all_id()
    data['salary_currency'] = data['salary_currency'].apply(lambda x: convert_currency_to_id(dict_of_id, x))
    dict_of_all_currency = create_dict_of_all_currency(dict_of_id)
    data['salary'] = data.apply(lambda row: calculate_salary(dict_of_all_currency, row['salary_from'],
                                                             row['salary_to'], row['salary_currency'],
                                                             row['published_at']), axis=1)
    data['published_at'] = data['published_at'].apply(lambda x: x[:10:])
    data['published_at'] = pd.to_datetime(data['published_at'], format="%Y-%m-%d")
    data['year'] = data['published_at'].dropna().dt.year
    data.drop(['salary_from', 'salary_to', 'salary_currency', 'published_at'], axis=1, inplace=True)
    end = time.time()
    data.to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\files\\cur_vac.csv')
    print(end-start)
    return data


if __name__ == '__main__':
    create_cur_data()