from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def relevance(request):
    return render(request, "main/about.html")


def geography(request):
    return render(request, "main/about.html")


def recent_vacancies(request):
    return render(request, "main/about.html")