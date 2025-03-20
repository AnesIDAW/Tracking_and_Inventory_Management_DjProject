from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import Product
from tracking.models import Vehicle

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('client_dashboard')

    total_products = Product.objects.count()
    in_transit = Product.objects.filter(status='in_transit').count()
    delivered = Product.objects.filter(status='delivered').count()
    total_vehicles = Vehicle.objects.count()

    context = {
        'total_products': total_products,
        'in_transit': in_transit,
        'delivered': delivered,
        'total_vehicles': total_vehicles,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('admin_dashboard')

    client_products = Product.objects.filter(client=request.user)

    context = {
        'client_products': client_products,
    }
    return render(request, 'dashboard/client_dashboard.html', context)
