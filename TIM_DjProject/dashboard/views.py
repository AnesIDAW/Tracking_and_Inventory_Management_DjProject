from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from inventory.models import Product, Vehicle
from users.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ClientProfileForm
from django.utils import timezone
from django.db.models import Q

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
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
    if request.user.is_superuser:
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


@login_required
@user_passes_test(lambda u: u.is_staff)
def rfid_product_handler(request):
    message = None
    rfid_prefill = request.GET.get("rfid_tag", "")  # Pre-fill if sent from ESP32

    if request.method == "POST":
        action = request.POST.get("action")
        rfid = request.POST.get("rfid_tag")

        if not rfid:
            message = "RFID is required."
            return render(request, "dashboard/staff_product_handler.html", {"message": message})

        if action == "deliver":
            try:
                product = Product.objects.get(rfid_tag=rfid)
                product.status = 'delivered'
                product.last_scanned_time = timezone.now()
                product.save()
                message = f"Product '{product.name}' marked as delivered."
            except Product.DoesNotExist:
                message = "Product with this RFID not found."
        
        elif action == "add":
            name = request.POST.get("name")
            client_username = request.POST.get("client")
            warehouse = request.POST.get("warehouse")
            vehicle_plate = request.POST.get("vehicle")

            try:
                client = CustomUser.objects.get(username=client_username)
            except CustomUser.DoesNotExist:
                return render(request, "dashboard/staff_product_handler.html", {
                    "message": "Client not found by username."
                })

            vehicle = None
            if vehicle_plate:
                try:
                    vehicle = Vehicle.objects.get(plate_number=vehicle_plate)
                except Vehicle.DoesNotExist:
                    return render(request, "dashboard/staff_product_handler.html", {
                        "message": "Vehicle not found by plate number."
                    })

            try:
                product = Product.objects.create(
                    name=name,
                    rfid_tag=rfid,
                    client=client,
                    warehouse_location=warehouse,
                    vehicle=vehicle,
                    status='stored'
                )
                message = f"Product '{name}' added successfully."
            except Exception as e:
                message = f"Error creating product: {str(e)}"

        # ✅ After successful POST: redirect to clean page without rfid in URL
        return redirect('dashboard:staff_product_handler')

    # For GET
    return render(request, "dashboard/staff_product_handler.html", {
        "message": message,
        "rfid_prefill": rfid_prefill
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def staff_product_list(request):
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(rfid_tag__icontains=query) |
            Q(client__username__icontains=query)
        )

    if status_filter:
        products = products.filter(status=status_filter)

    context = {
        "products": products,
        "query": query,
        "status_filter": status_filter,
    }
    return render(request, "dashboard/staff_products_list.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('dashboard:staff_products_list')  # Make sure this name matches your URL
