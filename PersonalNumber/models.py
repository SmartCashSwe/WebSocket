from django.db import models

class Pc_user(models.Model):
    pcIdentifier = models.CharField(max_length=64, unique=True)
    mobile_users = models.JSONField()

class Mobile_user(models.Model):
    personal_number = models.CharField(max_length=64)
    password = models.CharField(max_length=64)