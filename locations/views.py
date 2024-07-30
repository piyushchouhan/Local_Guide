from django.shortcuts import get_object_or_404, render
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from localguides.models import Booking, Guide,User, Location
from .models import Meeting_Location  # Adjust this import based on your app structure
import pdb

@login_required
def meet_location(request):
    return render(request, 'locations/meet_location.html')
    
@login_required
def process_location_data(request):
    booking_id = request.session.get('booking_id')
    if request.method == 'POST':
        json_data = json.loads(request.body)

        # Extracting relevant information
        formatted_address = json_data['results'][0]['formatted_address']
        location_data = json_data['results'][0]['geometry']['location']

        # Assuming you have the user and guide objects available
        user = request.user
        booking = get_object_or_404(Booking, pk=booking_id)
        guide = get_object_or_404(Guide, pk=booking.guide_id)

        # Creating a new Location object
        location = Meeting_Location(
            user=user,
            guide=guide,
            address=formatted_address,
            latitude=location_data['lat'],
            longitude=location_data['lng']
        )
        
        # Save the Location object to the database
        location.save()
        ml_id = location.id
        request.session['ml_id'] = ml_id


        return JsonResponse({'message': 'Location data stored successfully'})

    return JsonResponse({'error': 'Invalid request method'})


