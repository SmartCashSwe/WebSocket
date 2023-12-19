from django.db import models
import os

TYPECHOICES=(
    ("MonthSie4","MonthSie4"),
    ("MonthPdf","MonthPdf"),
    ("ZSie4","ZSie4"),
    ("ZPdf","ZPdf"),
    )

def get_rapport_path(instance, filename):
    return os.path.join("file",f"{instance.name}/",filename)

# Create your models here.
class Revisor(models.Model):
    email=models.EmailField(null=True, blank=True, unique=True, max_length=256)
    password=models.CharField(null=True, max_length=256)
    file=models.FileField(upload_to=get_rapport_path, null=True, blank=True)
    
    
