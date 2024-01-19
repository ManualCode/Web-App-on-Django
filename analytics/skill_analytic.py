import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_cur_data(csv='C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\files\\cur_vac.csv'):
    data = pd.read_csv(csv)
    data = data.loc[data['salary'] > 0]
    return data


def filter_data(data):
    data = data[data['name'].str.lower().str.contains("|".join(['c#', 'c sharp', 'шарп', 'с#']), case=False, na=False)]
    return data



def get_top_cities_salary(data):
    skills_dict = {}
    for _, row in data.iterrows():
        if pd.isna(row["key_skills"]):
            continue
        skills = row["key_skills"].split("\n")
        year = row["year"]

        if year not in skills_dict:
            skills_dict[year] = {}

        for skill in skills:
            if skill not in skills_dict[year]:
                skills_dict[year][skill] = 1
            else:
                skills_dict[year][skill] += 1

    # Вычисление топ-20 навыков для каждого года
    top_skills_per_year = {}

    for year in skills_dict:
        top_skills_per_year[year] = sorted(skills_dict[year].items(), key=lambda x: x[1], reverse=True)[:20]

    pd.DataFrame(top_skills_per_year).to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\filtred_skills.csv', index=False)


# if __name__ == '__main__':
#     get_top_cities_salary(filter_data(create_cur_data()))


if __name__ == '__main__':
    df = pd.read_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\filtred_skills.csv')
    df = df.applymap(lambda x: x.replace('\'', '').replace('(', '').replace(')', '').replace(',', ':'))
    df.to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\filtred_skills.csv')