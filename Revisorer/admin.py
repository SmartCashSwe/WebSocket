from django.contrib import admin
from Revisorer.models import Revisor
# Register your models here.

from django.contrib.sessions.models import Session
...
admin.site.register(Session)


admin.site.register(Revisor)
