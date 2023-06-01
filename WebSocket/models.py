from django.db import models
import os

class KasaSoftware(models.Model):
    file= models.FileField(upload_to="enox")