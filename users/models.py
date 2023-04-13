from django.db import models

class User (models.Model):
  username = models.CharField(max_length=50)
  password = models.TextField(editable=False,null=False, blank=False)
  x_rapport=models.JSONField(default={"test":""})
  prn=models.JSONField(default=["197504049292"])