from django.urls import path
from .views import (
    phone_getNotifications,
    send_to_mobile,
    update_artikel,
    get_z,
    get_company,
    get_x_rapport,
    laggTill_artikel,
    laggTill_huvudgrupp,
    update_artikel,
    update_huvudgrupp,
    index,
    room,
    log_in_mobile,
    choose_kasa,
    log_out
    
    )

app_name="prn"
urlpatterns = [
    path('send_to_mobile',      send_to_mobile,         name="send_to_mobile"),
    path('getnotifications/',   phone_getNotifications, name="phone_getNotifications"),
    path('update_artikel',      update_artikel,         name="update_artikel"),
    path('get_z',               get_z,                  name="get_z"),
    path('get_company',         get_company,            name="get_company"),
    path('get_x_rapport',       get_x_rapport,          name="get_x_rapport"),
    path('laggTill_artikel',    laggTill_artikel,       name="laggTill_artikel"),
    path('laggTill_huvudgrupp', laggTill_huvudgrupp,    name="laggTill_huvudgrupp"),
    path('update_artikel',      update_artikel,         name="update_artikel"),
    path('update_huvudgrupp',   update_huvudgrupp,      name="update_huvudgrupp"),
    path("",                    index,                  name="index"),
    path("prn/<str:room_name>/",room,                   name="room"),
    path("mobile_login/",       log_in_mobile,          name="mobile_login"),
    path("mobile_login",        log_in_mobile,          name="mobile_login"),
    path("choose_kasa/",        choose_kasa,            name="choose_kasa"),
    path("logout/",             log_out,                name="log_out"),

]
