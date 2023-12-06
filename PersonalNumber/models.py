from django.db import models


class Mobile_user(models.Model):
    personal_number = models.CharField(max_length=12)
    certification = models.TextField(blank=True, null=False)