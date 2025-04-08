from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import Product, Vehicle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    return render(request, 'dashboard/Custom_Dashboard_Client.html', context)

@csrf_exempt
@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('admin_dashboard')

    client_products = Product.objects.filter(client=request.user)

    context = {
        'client_products': client_products,
    }
    return render(request, 'dashboard/client_dashboard.html', context)

@csrf_exempt
def vehicle_locations(request):
    vehicles = Vehicle.objects.all()  # Fetch vehicles from tracking app

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
