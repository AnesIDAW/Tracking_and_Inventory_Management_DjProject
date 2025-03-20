from django.urls import path
from .views import admin_dashboard, client_dashboard

urlpatterns = [
    #path('admin/', admin_dashboard, name='admin_dashboard'),
    path('client/', client_dashboard, name='client_dashboard'),
]
