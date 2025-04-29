from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from inventory.models import Vehicle

@csrf_exempt
def vehicle_locations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"[VEHICLE LOCATION] Received data: {data}")
        plate_number = data.get('plate_number')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        try:
            vehicle = Vehicle.objects.get(plate_number=plate_number)
            vehicle.latitude = latitude
            vehicle.longitude = longitude
            vehicle.save()

            return JsonResponse({"message": "Vehicle location updated successfully"})
        except Vehicle.DoesNotExist:
            return JsonResponse({"error": "Vehicle not found"}, status=404)
        
    elif request.method == 'GET':
        vehicles = Vehicle.objects.all()
        data = []
        for v in vehicles:
            data.append({
                "vehicle_name": v.name,
                "longitude": v.longitude,
                "latitude": v.latitude,
                "plate_number": v.plate_number,
            })
        return JsonResponse({"vehicles": data})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

"""
@csrf_exempt
def rfid_scan_receiver(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            rfid_tag = data.get("rfid_tag")

            if not rfid_tag:
                return JsonResponse({"error": "RFID tag missing"}, status=400)

            print(f"[RFID SCAN] Received tag: {rfid_tag}")

            return JsonResponse({
                "redirect_url": f"/dashboard/add-product/?rfid_tag={rfid_tag}"
            })
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        # Just for testing
        return JsonResponse({"message": "Hello! Please POST RFID data to this endpoint."})

    return JsonResponse({"error": "Method not allowed"}, status=405)
"""
    
latest_rfid_tag = None  # global variable

@csrf_exempt
def rfid_scan_receiver(request):
    global latest_rfid_tag
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            rfid_tag = data.get("rfid_tag")

            if not rfid_tag:
                return JsonResponse({"error": "RFID tag missing"}, status=400)

            latest_rfid_tag = rfid_tag  # Store it
            print(f"[RFID SCAN] Received tag: {rfid_tag}")

            return JsonResponse({"status": "received"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def latest_rfid(request):
    global latest_rfid_tag
    return JsonResponse({"rfid_tag": latest_rfid_tag})
