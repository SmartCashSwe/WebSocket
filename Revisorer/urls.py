from django.urls import path
from .views import (
index
    
    )

app_name="Revisorer"
urlpatterns = [
    path("",                    index,                  name="index"),

]
