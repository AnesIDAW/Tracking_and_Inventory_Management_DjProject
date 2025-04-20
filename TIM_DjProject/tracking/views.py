from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from inventory.models import Vehicle

@csrf_exempt
def update_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Identify the vehicle by 'id' or 'plate_number'
            plate_number = data.get("plate_number")
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if plate_number:
                vehicle = Vehicle.objects.get(plate_number=plate_number)
            else:
                return JsonResponse({"error": "Vehicle identifier missing"}, status=400)

            # Update vehicle location
            vehicle.latitude = f"{latitude}"
            vehicle.longitude = f"{longitude}"
            vehicle.save()

            return JsonResponse({"success": "Location updated successfully"})
            
        except Vehicle.DoesNotExist:
            return JsonResponse({"error": "Vehicle not found"}, status=404)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request again ☺"}, status=400)
