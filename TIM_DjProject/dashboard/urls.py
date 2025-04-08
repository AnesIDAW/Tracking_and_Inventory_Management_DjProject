from django.urls import path
from .views import admin_dashboard, client_dashboard ,vehicle_locations
from tracking.views import update_location

app_name = "dashboard"
post_name = client_dashboard

urlpatterns = [
    #path('admin/', admin_dashboard, name='admin_dashboard'),

    path('client/', client_dashboard, name='client_dashboard'),
    path("api/vehicle-locations/", vehicle_locations, name="vehicle_locations"),
    path('update-location/', update_location, name="update_location")
]
