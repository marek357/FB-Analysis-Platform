from django.db import models


class Audio(models.Model):
    tytul = models.CharField(max_length=125)
    nagranie = models.FileField()
