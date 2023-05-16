from django.db import models


class Mobile_user(models.Model):
    personal_number = models.CharField(max_length=64)
    password = models.CharField(max_length=64)