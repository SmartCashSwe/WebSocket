from django.urls import path

from . import views

app_name="prn"
urlpatterns = [
    path("", views.index, name="index"),
    path("prn/<str:room_name>/", views.room, name="room"),
    path("pc/<str:room_name>/", views.pcRoom, name="pcRoom"),
    path("pc_login", views.log_in_pc, name="pc_login"),
    path("pc_login/", views.log_in_pc, name="pc_login"),

]