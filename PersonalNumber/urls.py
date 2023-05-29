from django.urls import path

from . import views

app_name="prn"
urlpatterns = [
    path("", views.index, name="index"),
    path("prn/<str:room_name>/", views.room, name="room"),
    path("mobile_login/", views.log_in_mobile, name="mobile_login"),
    path("mobile_login", views.log_in_mobile, name="mobile_login"),
    path("choose_kasa/", views.choose_kasa, name="choose_kasa"),

]