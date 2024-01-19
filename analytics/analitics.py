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


def first_plot(data):
    salary_dynamics = get_salary_dynamics(data)
    #filtred_salary_dynamics = get_salary_dynamics(filtred_data)
    plt.title(label="Уровень зарплат по годам", fontsize=8)
    #x_axis = np.arange(len(list(salary_dynamics.keys())))
    plt.bar(salary_dynamics.keys(), salary_dynamics.values())
    #plt.bar(x_axis + 0.2, filtred_salary_dynamics.values(), width=0.4)
    plt.legend(['Cредняя З/П C#-программист'], fontsize=8)
    plt.grid(axis='y')
    plt.xticks(list(salary_dynamics.keys()), labels=[x for x in range(2003, 2024)], rotation=90, fontsize=8)
    plt.tick_params(axis='y', labelsize=8)
    plt.savefig('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\images\\salary_dynamics_for_filtred_data')
    plt.show()


def second_plot(data):
    vacancies_dynamics = get_vacancies_dynamics(data)
    #filtred_vacancies_dynamics = get_vacancies_dynamics(filtred_data)
    #x_axis = np.arange(len(list(vacancies_dynamics.keys())))
    plt.title(label="Количество вакансий по годам", fontsize=8)
    plt.bar(vacancies_dynamics.keys(), vacancies_dynamics.values())
    #plt.bar(x_axis + 0.2, filtred_vacancies_dynamics.values(), width=0.4)
    #plt.ylim(0, 20_000)
    plt.legend(['Количество вакансий C#-программист'], fontsize=8)
    plt.xticks(list(vacancies_dynamics.keys()), labels=[x for x in range(2003, 2024)], rotation=90, fontsize=8)
    plt.tick_params(axis='y', labelsize=8)
    plt.savefig('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\images\\vacancies_dynamics_for_filtred_data')
    plt.show()


def third_plot(data):
    top_cities_salary = get_top_cities_salary(data)
    f = []
    for i in list(top_cities_salary.keys()):
        if ' ' in i:
            f.append('\n'.join(i.split(" ")))
        elif '-' in i:
            f.append('-\n'.join(i.split("-")))
        else:
            f.append(i)

    plt.title(label="Уровень зарплат по городам C#-программист", fontsize=8)
    plt.barh(list(top_cities_salary.keys()), top_cities_salary.values())
    plt.yticks(list(top_cities_salary.keys()), f, fontdict={'horizontalalignment': 'right',
                                           'verticalalignment': 'center'})
    plt.tick_params(axis='y', labelsize=6)
    plt.tick_params(axis='x', labelsize=8)
    plt.grid(axis='x')
    plt.gca().invert_yaxis()
    plt.savefig('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\images\\top_salary_for_filtred_data')
    plt.show()



def fourth_plot(data):
    top_cities_vacancies = get_top_cities_vacancies(data)
    top_cities_vacancies['Другие'] = 1 - sum(top_cities_vacancies.values())
    plt.title(label="Доля вакансий по городам для C#-программиста", fontsize=8)
    plt.pie(top_cities_vacancies.values(), labels=top_cities_vacancies.keys(), textprops={'fontsize': 6})
    plt.axis('equal')
    plt.savefig('C:\\Users\\kiril\\PycharmProjects\\Web-App-on-Django\\images\\top_vacancies_for_filtred_data')
    plt.show()


def create_plot():
    data = create_cur_data()
    filtred_data = filter_data(data)

    first_plot(filtred_data)
    second_plot(filtred_data)
    third_plot(filtred_data)
    fourth_plot(filtred_data)

    return -2


if __name__ == '__main__':
    create_plot()
