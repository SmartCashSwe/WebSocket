from django.db import models

# Create your models here.
class Revisor(models.Model):
    email=models.EmailField(null=False, blank=False, unique=True, max_length=256),
    password=models.CharField(null=True, max_length=256)
