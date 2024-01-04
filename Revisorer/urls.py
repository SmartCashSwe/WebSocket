from django.urls import path
from .views import (
choose_kassasystem,
    log_in_revisor,
    z_rapport_list,
    check_logged_in,
    bokforing,
    download_file,
    log_out_revisor
    )

app_name="Revisorer"
urlpatterns = [
    path("",                    choose_kassasystem,                  name="index"),
    path("login/",                    log_in_revisor,                  name="login_revisor"),
    path("login/",                    log_in_revisor,                  name="login_revisor"),
    path("logout/",                    log_out_revisor,                  name="logout_revisor"),
    path("check_session/",                    check_logged_in,                  name="login_revisor"),
    path("z_list",                    z_rapport_list,                  name="z_list_revisor"),
    path("bokforing",                    bokforing,                  name="bokforing_revisor"),
    path("download_file", download_file, name="download_file"),

]
