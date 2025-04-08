from django.urls import path
from .views import update_location

urlpatterns = [
    path('update-location/', update_location, name='update_location'),
]
