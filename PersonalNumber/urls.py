from django.urls import path

from . import views

app_name="prn"
urlpatterns = [
    path("", views.index, name="index"),
    path("prn/<str:room_name>/", views.room, name="room"),
    path("pc/<str:room_name>/", views.pcRoom, name="pcRoom"),
    path("mobile_login/", views.log_in_mobile, name="mobile_login"),
    path("mobile_login", views.log_in_mobile, name="mobile_login"),

]