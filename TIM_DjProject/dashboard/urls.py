from django.urls import path
from .views import *
from users.views import user_logout

app_name = "dashboard"

urlpatterns = [
    path('staff/', admin_dashboard, name='admin_dashboard'),
    path('client/', client_dashboard, name='client_dashboard'),
    path('history/', delivery_history, name='delivery_history'),
    path('reports/', reports, name='reports'),
    path('support-center/', support_center, name='support_center'),
    path('hub-info/', hub_info, name='hub_info'),
    path('client/settings/', client_settings, name='client_settings'),
    path('client/delete/', delete_account, name='delete_account'),
    path('logout/', user_logout, name='client_logout'),
    path('add-product/',product_handler, name='staff_product_handler'),
    path('products/', staff_product_list, name='staff_product_list'),
    path('products/<int:pk>/delete/', delete_product, name='delete_product'),
    path('ticket/<int:pk>/download/', download_ticket, name='download_ticket'), 
]
