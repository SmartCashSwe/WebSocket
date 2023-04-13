from django.db import models

# Create your models here.
from django.db import models

class Prn(models.Model):
    prn = models.CharField(max_length=20, unique=True)
    password = models.TextField()

    def __str__(self):
        return self.prn