from django.urls import path
from .views import register, user_login, custom_logout, dashboard, user_logout

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard')
]
