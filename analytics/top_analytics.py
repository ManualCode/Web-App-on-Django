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


def get_salary_dynamics(data):
    return data.fillna(0).groupby('year')['salary'].mean().astype(float).round().to_dict()


def get_vacancies_dynamics(data):
    return data.groupby('year')['name'].count().to_dict()


def get_top_cities_salary(selected_data):
    df_area_salaries = selected_data.groupby(['area_name']).agg({'salary': 'mean', 'name': 'count'}).dropna()\
        .astype(float).round().astype(int).sort_values(by=['salary', 'area_name'], ascending=(False, True))
    df_area_salaries['name'] = df_area_salaries['name'] / df_area_salaries['name'].sum()
    df_area_salaries = df_area_salaries[df_area_salaries.name * 100 >= 1]
    city_salary = {key: value for key, value in list(df_area_salaries.to_dict()['salary'].items())[:10]}
    return city_salary


def get_top_cities_vacancies(selected_data):
    df_area_vacancies = selected_data.groupby(['area_name']).agg({'name': 'count'})\
        .sort_values(by=['name', 'area_name'], ascending=(False, True))
    df_area_vacancies['name'] = df_area_vacancies['name'] / df_area_vacancies['name'].sum()
    df_area_vacancies = df_area_vacancies[df_area_vacancies.name * 100 >= 1]
    city_vacancy_ratio = {key: round(value, 4) for key, value in list(df_area_vacancies.to_dict()['name'].items())[:10]}

    return city_vacancy_ratio


def create_20(data, year):
    plt.title(label=f"Топ навыков за {year} для C#-программист", fontsize=8)
    d = [(' '.join(x.split())).replace(' ', '\n') for x in data[0]]
    plt.bar(data[0], data[1])
    plt.legend([f"Частота употребления в вакансии"], fontsize=8)
    plt.xticks(data[0], rotation=30, ha='right', fontsize=6)
    plt.tick_params(axis='y', labelsize=8)
    plt.savefig(f'C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\images\\graphs_for_geography\\top_20_{i}_filtred')
    plt.show()
    plt.close()


if __name__ == '__main__':
    df = pd.read_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\filtred_skills.csv', index_col=0)

    for i in range(2015, 2024):
        key = []
        value = []
        for j in df[str(i)].to_list():
            m = j.split(': ')
            key.append(m[0])
            value.append(m[1])

        create_20([key[::-1], value[::-1]], i)


    data = create_cur_data()
    f_data = filter_data(data)
    g_s_d = get_salary_dynamics(data)
    g_s_f_d = get_salary_dynamics(f_data)

    df = pd.DataFrame(list(g_s_d.items()), columns=['Год', 'Зарплата'])
    df.insert(loc=2, column='Зарплата C#-программист', value=g_s_f_d.values())
    df.insert(loc=3, column='Кол-во вакнсий', value=get_vacancies_dynamics(data).values())
    df.insert(loc=4, column='Кол-во вакнсий C#-программист', value=get_vacancies_dynamics(f_data).values())
    df.to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\first.csv')

    df = pd.DataFrame(list(get_top_cities_salary(data).items()), columns=['Город', 'Зарплата'])
    df.to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\second.csv')

    df = pd.DataFrame(list(get_top_cities_salary(f_data).items()), columns=['Город', 'Зарплата C#-программист'])
    df.to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\second2.csv')


    df = pd.DataFrame(list(get_top_cities_vacancies(data).items()), columns=['Город', 'Доля вакансий'])
    # df.insert(loc=2, column='Доля вакансий C#-программист', value=get_top_cities_vacancies(f_data).values())
    df.to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\third.csv')

    df = pd.DataFrame(list(get_top_cities_vacancies(f_data).items()), columns=['Город', 'Доля вакансий C#-программист'])
    df.to_csv('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\djangoProject\\main\\static\\deps\\data_for_tables\\fourth.csv')





