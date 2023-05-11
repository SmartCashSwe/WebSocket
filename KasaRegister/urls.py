from django.urls import path
from .views import (
    kasa_insertNotification,
    get_all_artiklar,
    backup,
    check_backup,
    sync_pn,
    get_x,
    check_z,
    send_z,
    get_update,
    send_huvudgrupper,
    
    )

app_name="kasa"
urlpatterns = [
    path('insertnotification', kasa_insertNotification),
    path('get_all', get_all_artiklar),
    path('set_access', get_all_artiklar),
    path('backup', backup),
    path('check-backup', check_backup),
    path('sync_pn', sync_pn),
    path('get_x', get_x),
    path('check_z', check_z),
    path('send_z', send_z),
    path('get_update', get_update),
    path('send_huvudgrupper',send_huvudgrupper)
]