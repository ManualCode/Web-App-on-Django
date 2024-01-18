from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def relevance(request):
    return render(request, "main/relevance.html")


def geography(request):
    return render(request, "main/geography.html")


def skills(request):
    return render(request, "main/skills.html")


def recent_vacancies(request):
    return render(request, "main/recent_vacancies.html")