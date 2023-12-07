from django.db import models


class Mobile_user(models.Model):
    personal_number = models.CharField(max_length=265, unique=True, null=False, blank=False)
    certification = models.TextField(blank=True, null=False)