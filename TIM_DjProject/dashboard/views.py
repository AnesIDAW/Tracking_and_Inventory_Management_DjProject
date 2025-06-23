from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from inventory.models import Product, Vehicle
from users.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ClientProfileForm
from django.utils import timezone
from django.db.models import Q
from uuid import uuid4
from django.http import HttpResponse
from django.http import FileResponse
from django.contrib import messages
import time
import traceback

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('dashboard:client_dashboard')

    total_products = Product.objects.count()
    in_transit = Product.objects.filter(status='in_transit').count()
    delivered = Product.objects.filter(status='delivered').count()
    total_vehicles = Vehicle.objects.count()
    vehicles = Vehicle.objects.all()

    context = {
        'total_products': total_products,
        'in_transit': in_transit,
        'delivered': delivered,
        'total_vehicles': total_vehicles,
        'vehicles': vehicles,
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
def reports(request):
    return render(request, 'dashboard/reports.html')

@login_required
def support_center(request):
    return render(request, 'dashboard/support_center.html')

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
def product_handler(request):
    message = None
    rfid_prefill = request.GET.get("rfid_tag", "")

    if request.method == "POST":
        action = request.POST.get("action")
        identification_method = request.POST.get("identification_method")

        if action == "deliver":
            tag = request.POST.get("rfid_tag") or request.POST.get("qr_code")
            if not tag:
                return render(request, "dashboard/staff_product_handler.html", {
                    "message": "Tag (RFID or QR Code) is required."
                })

            try:
                if identification_method == "qr code":
                    product = Product.objects.get(qr_code=tag)
                else:
                    product = Product.objects.get(rfid_tag=tag)

                product.status = 'delivered'
                product.last_scanned_time = timezone.now()
                product.save()

                messages.success(request, "Product marked as delivered!")
                return redirect('dashboard:staff_product_handler')

            except Product.DoesNotExist:
                message = "Product with this tag was not found."

        elif action == "add":
            try:
                name = request.POST.get("name")
                client = CustomUser.objects.get(username=request.POST.get("client"))
                warehouse = request.POST.get("warehouse")
                vehicle_plate = request.POST.get("vehicle")
                vehicle = Vehicle.objects.get(plate_number=vehicle_plate) if vehicle_plate else None

                receiver_name = request.POST.get("receiver_name")
                receiver_email = request.POST.get("receiver_email")
                receiver_phone = request.POST.get("receiver_phone")

                if identification_method == "qr code":
                    qr_code = str(uuid4())
                    product = Product.objects.create(
                        name=name,
                        identification_method="qr code",
                        qr_code=qr_code,
                        client=client,
                        warehouse_location=warehouse,
                        vehicle=vehicle,
                        receiver_name=receiver_name,
                        receiver_email=receiver_email,
                        receiver_phone_number=receiver_phone
                    )
                else:
                    rfid = request.POST.get("rfid_tag")
                    if not rfid:
                        raise ValueError("RFID is required.")
                    product = Product.objects.create(
                        name=name,
                        identification_method="rfid",
                        rfid_tag=rfid,
                        client=client,
                        warehouse_location=warehouse,
                        vehicle=vehicle,
                        receiver_name=receiver_name,
                        receiver_email=receiver_email,
                        receiver_phone_number=receiver_phone
                    )

                # Force ticket PDF generation (save handles this)
                product.save()

                # DEBUG: Print to console
                print("✅ Product created:", product)
                print("📄 Ticket PDF path:", product.ticket_pdf)

                return redirect('dashboard:download_ticket', pk=product.pk)

            except Exception as e:
                # DEBUG: print full traceback
                print("❌ Error creating product:")
                traceback.print_exc()
                message = f"Error: {str(e)}"

    return render(request, "dashboard/staff_product_handler.html", {
        "message": message,
        "rfid_prefill": rfid_prefill
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def download_ticket(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.ticket_pdf:
        return HttpResponse("PDF not available", status=404)

    return FileResponse(product.ticket_pdf.open(), content_type='application/pdf')

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
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    return redirect('dashboard:staff_product_list')  # Make sure this name matches your URL
