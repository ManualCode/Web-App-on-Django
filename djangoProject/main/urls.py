from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('relevance', views.relevance),
    path('geography', views.geography),
    path('skills', views.skills),
    path('recent-vacancies', views.recent_vacancies),

]
