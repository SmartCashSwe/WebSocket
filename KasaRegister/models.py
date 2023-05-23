from django.db import models
from datetime import datetime
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
import secrets


def get_file_path(instance, filename):
    print(instance.company_name)
    now=datetime.now()
    return os.path.join("dropbox",f"{instance.company_name}/{now.year}{now.month}{now.day}/",filename)

def get_id_path(instance, filename):
    print(instance.name)
    now=datetime.now()
    return os.path.join("file",f"{instance.name}/",filename)


class KasaUser(models.Model):
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    prn = models.TextField( null=True, blank=True)
    adress=models.TextField(null=False, max_length=200, blank=False, default='{"adress":"", "postnummer":""}')
    fcm_token = models.TextField()
    notifications = models.TextField()
    org_num = models.TextField(unique=False)
    company_name = models.TextField()
    backup=models.FileField( upload_to=get_file_path, null=True, blank=True)
    backup2=models.FileField(upload_to=get_file_path, null=True,blank=True)
    backup3=models.FileField(upload_to=get_file_path, null=True,blank=True)
    xRapport=models.JSONField(default={"test":""})
    z_rapport=models.JSONField(blank=True, null=True, default={"test":""})
    all_products=models.JSONField(default=[])
    kassa_list=models.JSONField(default={"LäggTillArtikel":[], "UppdateraArtikel":[], "LäggTillHuvudgrupp":[],"UppdateraHuvudgrupp":[]})
    huvudgrupper=models.JSONField(default=[])

    def backup_name(self):
        if self.backup!=None and self.backup!="":
            return os.path.basename(self.backup.name)
        else:
            return ""

    def __str__(self):
        return self.company_name +" | "+ self.org_num
    
        
class IdFiles(models.Model):
    name=models.CharField(null=False, blank=False, max_length=50)
    the_file=models.FileField(upload_to=get_id_path, null=False, blank=False)
    
    def __str__(self):
        return self.name
    

class Licence(models.Model):
    valid_until=models.DateField(auto_now=True, blank=False, null=False)
    licence=models.CharField(auto_created=True, max_length=12)
    kasa=models.OneToOneField(KasaUser,  on_delete=models.PROTECT, blank=True, null=True  )
    def save(self, *args, **kwargs):
        if len(self.licence)<12:
            self.licence= secrets.token_hex(6)

        super(Licence, self).save(*args, **kwargs) # Call the real save() method