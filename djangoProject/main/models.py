from django.db import models


class Vacancy(models.Model):
    name = models.CharField(max_length=100)
    key_skills = models.CharField(max_length=1000)
    salary = models.IntegerField()
    area_name = models.CharField(max_length=100)
    Year = models.IntegerField()

    class Meta:
        db_table = 'vacancy'
