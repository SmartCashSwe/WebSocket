from django.urls import path
from .views import (
choose_kassasystem,
    log_in_revisor,
    z_rapport_list
    )

app_name="Revisorer"
urlpatterns = [
    path("",                    choose_kassasystem,                  name="index"),
    path("login/",                    log_in_revisor,                  name="login_revisor"),
    path("z_list",                    z_rapport_list,                  name="z_list_revisor"),

]
