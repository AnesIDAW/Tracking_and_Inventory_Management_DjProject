from django.urls import path
from .views import *
from tracking.views import update_location
from users.views import user_logout

app_name = "dashboard"

urlpatterns = [
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('client/', client_dashboard, name='client_dashboard'),
    path("api/vehicle-locations/", vehicle_locations, name="vehicle_locations"),
    path('update-location/', update_location, name="update_location"),
    path('history/', delivery_history, name='delivery_history'),
    path('hub-info/', hub_info, name='hub_info'),
    path('client/settings/', client_settings, name='client_settings'),
    path('client/delete/', delete_account, name='delete_account'),
    path('logout/', user_logout, name='client_logout'), 
]
