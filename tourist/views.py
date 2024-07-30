from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
import json
from localguides.models import Booking, Location, Guide, TrustedContact
from django.core.exceptions import ObjectDoesNotExist
from locations.models import Meeting_Location
from tourist.forms import TrustedContactForm


def index(request):
    city = Location.objects.all()[:5]
    return render(request, "tourist/index.html", 
            {'city': city})

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tourist/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "tourist/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tourist/signup.html")

# def signin_view(request):
#     if request.method == "POST":
#         #Attempt to sign user in
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request, "tourist/signin.html", {
#                 "message" : "Invalid username and/or password."
#             })
#     else:
#         return render(request, "tourist/signin.html")

def signin_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is not a guide
            if not Guide.objects.filter(user=user).exists():
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                # User is a guide and should not log in here
                return render(request, "tourist/signin.html", {
                    "message": "Access denied. Local guides should sign in through the guide portal."
                })
        else:
            return render(request, "tourist/signin.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tourist/signin.html")


def signout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("signIn"))

def search_city(request):
    try:
        # Get the query parameter from the AJAX request
        query = request.GET.get('query', '')

        # Query the database for matching city names (case-insensitive)
        matching_cities = Location.objects.filter(location_name__icontains=query)

        # Extract city names from the matching cities
        city_names = [city.location_name for city in matching_cities]

        # Return the city names as JSON data
        return JsonResponse(city_names, safe=False)
    except ObjectDoesNotExist:
        # Handle the case where the Location object doesn't exist
        return JsonResponse([], safe=False)
    except Exception as e:
        # Handle other exceptions (e.g., database connection errors)
        return JsonResponse({'error': str(e)}, status=500)


def autocomplete_city(request):
    try:
        # Get the user's input from the query parameter
        query = request.GET.get('term', '')

        # Query the database for matching city names (case-insensitive)
        matching_cities = Location.objects.filter(location_name__icontains=query)

        # Extract city names from the matching cities
        city_names = [city.location_name for city in matching_cities]

        # Return the city names as JSON data
        return JsonResponse(city_names, safe=False)
    except ObjectDoesNotExist:
        # Handle the case where the Location object doesn't exist
        return JsonResponse([], safe=False)
    except Exception as e:
        # Handle other exceptions (e.g., database connection errors)
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def user (request, user_id):
    tourist = get_object_or_404(User, pk=user_id)
    return render(request, 'tourist/user.html',{
        'user' : tourist
    }) 

def Logout_and_Redirect(request):
    logout(request)  # Log the user out
    return redirect('localGuide')

@login_required
def edit_user(request, user_id):
    tourist = get_object_or_404(User, pk=user_id)
    return render(request, 'tourist/edit_user.html', {'user': tourist})

@login_required
def update_user(request, user_id):
    tourist = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Update user information based on the form data
        tourist.first_name = request.POST.get('first_name')
        tourist.last_name = request.POST.get('last_name')
        tourist.email = request.POST.get('email')
        tourist.username = request.POST.get('username')
        tourist.save()

        return redirect('touristUser', user_id=user_id)

    return render(request, 'tourist/edit_user.html', {'user': tourist})

@login_required
def send_email_with_geolocation(request):
    trusted_contact = TrustedContact.objects.filter(user=request.user).first()
    email = trusted_contact.email

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            email_content = f'Click here to view the location on Google Maps: {maps_link}'

            # Perform email sending logic
            send_mail(
                'Geo Location Of your friend',
                email_content,
                'guidelocal849@gmail.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Email sent successfully.'})
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def add_trusted_contact(request):
    if request.method == 'POST':
        form = TrustedContactForm(request.POST)

        if form.is_valid():
            # Assign the current user to the form before saving
            trusted_contact = form.save(commit=False)
            trusted_contact.user = request.user
            trusted_contact.save()
            return redirect('index') 

    else:
        form = TrustedContactForm()

    return render(request, 'tourist/trusted.html', {'form': form})

@login_required
def send_email_with_geolocation(request):
    trusted_contact = TrustedContact.objects.filter(user=request.user).first()
    email = trusted_contact.email

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            email_content = f'Click here to view the location on Google Maps: {maps_link}'

            # Perform email sending logic
            send_mail(
                'Geo Location Of your friend',
                email_content,
                'guidelocal849@gmail.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Email sent successfully.'})
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def send_notification_to_user(request):
    ml_id = request.session.get('ml_id')
    meet_location = get_object_or_404(Meeting_Location, pk=ml_id)
    booking_id = request.session.get('booking_id')
    booking = get_object_or_404(Booking, pk=booking_id)
    date = booking.booking_date
    guide = get_object_or_404(Guide, pk=booking.guide_id)
    contact_num = guide.contact_info
    user = request.user
    email = user.email
    # Extract latitude and longitude from meet_location
    # Create Google Maps link
    
    if request.method == 'POST':
        try:
            latitude = meet_location.latitude
            longitude = meet_location.longitude
            guide_f_name = guide.user.first_name
            guide_l_name = guide.user.last_name
            maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            email_content = (
                        f"Dear {user.first_name},\n\n"
                        f"Thank you for booking a local guide!\n\n"
                        f"Your local guide's name is {guide_f_name} {guide_l_name}.\n"
                        f"Conatct number of your local guide's is {contact_num}.\n"
                        f"The booking date is {date}.\n\n"
                        f"Click here to view the location on Google Maps: {maps_link}\n\n"
                        "Thanks for booking and we hope you have a great experience!\n\n"
                        "Visit again soon!\n"
                     )

            # Perform email sending logic
            send_mail(
                'Geo Location Of your friend',
                email_content,
                'guidelocal849@gmail.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Email sent successfully.'})
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)