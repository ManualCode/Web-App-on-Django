import pandas as pd
from django.shortcuts import render
from .scr import get_new_vac


def index(request):
    return render(request, 'main/index.html')


def relevance(request):
    df = pd.read_csv('main/static/deps/data_for_tables/first.csv', index_col=0)
    return render(request, "main/relevance.html", {'frame': df})


def geography(request):
    df1 = pd.read_csv('main/static/deps/data_for_tables/second.csv', index_col=0)
    df2 = pd.read_csv('main/static/deps/data_for_tables/second2.csv', index_col=0)
    df3 = pd.read_csv('main/static/deps/data_for_tables/third.csv', index_col=0)
    df4 = pd.read_csv('main/static/deps/data_for_tables/fourth.csv', index_col=0)

    return render(request, "main/geography.html", {'frame1': df1, 'frame2': df2,
                                                   'frame3': df3, 'frame4': df4})


def skills(request):
    df = pd.read_csv('main/static/deps/data_for_tables/skills.csv', index_col=0)
    fdf = pd.read_csv('main/static/deps/data_for_tables/filtred_skills.csv', index_col=0)
    years = [str(x) for x in range(2015, 2024)]
    return render(request, "main/skills.html", {'frame': df, 'filtred_frame': fdf, 'years': years})


def recent_vacancies(request):
    data = get_new_vac.get_vacancies()
    return render(request, "main/recent_vacancies.html", {'data': data})
