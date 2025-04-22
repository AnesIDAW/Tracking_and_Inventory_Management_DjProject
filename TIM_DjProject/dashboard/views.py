from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from inventory.models import Product, Vehicle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ClientProfileForm


# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard:client_dashboard')

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

# Client Dashboard View
@csrf_exempt
@login_required
def client_dashboard(request):
    print(request.user.is_staff)
    if request.user.is_superuser or request.user.groups.filter(name='Staff').exists():
        return redirect('dashboard:admin_dashboard')

    client_products = Product.objects.filter(client=request.user)

    total_orders = client_products.count()
    in_transit_count = client_products.filter(status='in_transit').count()
    delivered_count = client_products.filter(status='delivered').count()
    returned_count = client_products.filter(status='returned').count()


    context = {
        'client_products': client_products,
        'total_orders': total_orders,
        'in_transit_count': in_transit_count,
        'delivered_count': delivered_count,
        'returned_count': returned_count,
    }
    return render(request, 'dashboard/client_dashboard.html', context)

@csrf_exempt
def vehicle_locations(request):
    vehicles = Vehicle.objects.all()  # Fetch vehicles from iventory app

    # Debugging: Print fetched vehicles to Django console
    print("Fetched Vehicles:", list(vehicles))

    if not vehicles.exists():
        return JsonResponse({"error": "No vehicles found"})  # Debugging output
    
    data = [
        {
            "vehicle_name": v.name,
            "longitude": v.longitude,
            "latitude" : v.latitude,  
            "plate_number": v.plate_number,
        }
        for v in vehicles
    ]
    return JsonResponse({"vehicles": data})

@login_required
def delivery_history(request):
    delivered_products = Product.objects.filter(client=request.user, status='delivered')

    context = {
        'delivered_products': delivered_products
    }
    return render(request, 'dashboard/delivery_history.html', context)

@login_required
def hub_info(request):
    return render(request, 'dashboard/hub_info.html')

@login_required
def client_settings(request):
    user = request.user
    if request.method == 'POST':
        form = ClientProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard:client_settings')
    else:
        form = ClientProfileForm(instance=user)


    return render(request, 'dashboard/client_settings.html', {'form': form})

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('users:login')

"""   
@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')
"""