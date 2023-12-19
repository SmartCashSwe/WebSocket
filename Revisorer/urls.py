from django.urls import path
from .views import (
choose_kassasystem,
    log_in_revisor
    )

app_name="Revisorer"
urlpatterns = [
    path("",                    choose_kassasystem,                  name="index"),
    path("login",                    log_in_revisor,                  name="index"),

]
