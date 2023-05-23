from django.urls import path
from . import views

app_name="kasa"
urlpatterns = [
    path('insertnotification', views.kasa_insertNotification),
    path('get_all', views.get_all_artiklar),
    path('set_access', views.get_all_artiklar),
    path('backup', views.backup),
    path('check-backup', views.check_backup),
    path('sync_pn', views.sync_pn),
    path('get_x', views.get_x),
    path('check_z', views.check_z),
    path('send_z', views.send_z),
    path('get_update', views.get_update),
    path('send_huvudgrupper',views.send_huvudgrupper),
    path("pc_login/", views.log_in_pc, name="pc_login"),
    path("pc_login", views.log_in_pc, name="pc_login"),
    path("get_company", views.get_company, name="get_company"),

]