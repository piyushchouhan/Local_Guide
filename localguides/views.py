import json
from django.forms import ValidationError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from locations.models import Meeting_Location
from tourist.views import send_email_with_geolocation
from .models import User, Location, Gender, Language
from tourist.models import Availability
from localguides.models import Booking,Guide
from django.http import JsonResponse
from django.views.decorators.http import require_POST


from .models import Guide  # Import the Guide model

def index(request):
    return render(request, "localguides/index.html")

def localGuide_signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "localguides/signup.html", {
                "message": "Passwords must match."
            })

        try:
            # Create a new user
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)

            # Retrieve or create a Location instance for the provided location
            location_id = request.POST.get("location")
            location = Location.objects.get(id=location_id)

            # Collect additional fields for the Guide model
            description = request.POST.get("description")
            rate_per_hour = request.POST.get("rate_per_hour")
            contact_info = request.POST.get("contact_info")
            choice_id = request.POST.get("language")
            language = Language.objects.get(id=choice_id)
            gender_id = request.POST.get("gender")
            gender = Gender.objects.get(id=gender_id)
            image = request.FILES.get("image")  # Handle file upload for the image field

            # Create a new Guide instance associated with the user
            guide = Guide(
                user=user,
                location=location,
                description=description,
                rate_per_hour=rate_per_hour,
                contact_info = contact_info,
                language=language,
                gender=gender,
                image=image,
            )
            guide.full_clean()  # Validate the model fields
            guide.save()

        except IntegrityError:
            return render(request, "localguides/signup.html", {
                "message": "Username already taken."
            })
        except ValidationError as e:
            return render(request, "localguides/signup.html", {
                "message": e.message_dict
            })

        login(request, user)
        return HttpResponseRedirect(reverse("localGuide"))
    else:
        locations = Location.objects.all()
        language_choices = Language.objects.all()
        genders = Gender.objects.all()
        # Pass the language choices to the template
        return render(request, "localguides/signup.html", {
            "language_choices": language_choices,
            "locations": locations,
            "genders": genders,
        })


def localGuide_signin_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is associated with a Guide instance
            if Guide.objects.filter(user=user).exists():
                login(request, user)
                return HttpResponseRedirect(reverse("localGuide"))
            else:
                # User is not a guide
                return render(request, "localguides/signin.html", {
                    "message": "Access denied. You are not a local guide."
                })
        else:
            return render(request, "localguides/signin.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "localguides/signin.html")


def localGuide_signout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("localGuide_signIn"))

def lg_detail(request, local_guide_id):
    local_guide = get_object_or_404(Guide, pk = local_guide_id)
    availabilities  = Availability.objects.filter(local_guide = local_guide)
    events = []
    for availability in availabilities:
        events.append({
            'title': 'Booked' if availability.is_booked else 'Available',
            'start': availability.availability_date.strftime('%Y-%m-%d'),  # Format date as 'YYYY-MM-DD'
            'className': 'booked-event' if availability.is_booked else 'available-event',
        })

    context = {
        'local_guide': local_guide,
        'events': json.dumps(events),  # Convert events to a JSON string for JavaScript
    }

    return render(request, 'localguides/lg_detail.html', context)

def about_us(request):
    return render(request, "localguides/about_us.html") 

def privacy(request):
    return render(request, "localguides/privacy.html")

def terms(request):
    return render(request, "localguides/t_c.html")


@login_required
@require_POST
def book_date(request):
    try:
        data = json.loads(request.body)
        print("Received data:", data)
        selected_date = data.get('date')
        guide_id = data.get('guide_id')
        user = request.user

        guide = get_object_or_404(Guide, pk=guide_id)
        availability = get_object_or_404(Availability, local_guide=guide, availability_date=selected_date)

        if availability.is_booked:
            return JsonResponse({'status': 'error', 'message': 'Date already booked'}, status=400)

        availability.is_booked = True
        availability.save()

        booking = Booking.objects.create(user=user, guide=guide, booking_date=selected_date, booking_status='Booked')
        booking_id = booking.id
        request.session['booking_id'] = booking_id 

        return JsonResponse({'status': 'success', 'message': 'Booking successful.', 'booking_id': booking_id})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def get_available_dates(request, guide_id):
    # Fetch availability data for the guide
    dates = Availability.objects.filter(local_guide_id=guide_id, is_booked=False)
    data = [{"title": "Available", "start": date.availability_date} for date in dates]
    return JsonResponse(data, safe=False)

@login_required
def user(request):
    # Get the Guide object related to the logged-in user
    localguide = Guide.objects.get(user=request.user)

    # Filter bookings by the specified guide
    bookings = Booking.objects.filter(guide=localguide)

    # Create a list of tuples (tourist, booking_date, id)
    tourists_with_dates = [(booking.user, booking.booking_date, booking.id) for booking in bookings]
    print(tourists_with_dates)

    return render(request, 'localguides/user.html', {
        'localguide': localguide,
        'tourists_with_dates': tourists_with_dates
    })

def logout_and_redirect(request):
    logout(request)  # Log the user out
    return redirect('index')

@login_required
def edit_lg(request):
     localguide = Guide.objects.get(user=request.user)
     locations = Location.objects.all()
     language_choices = Language.objects.all()
     genders = Gender.objects.all()
     return render(request, 'localguides/edit_user.html',{
                    'localguide': localguide,
                    "locations": locations,
                    "language_choices": language_choices,
                    "genders": genders,
        })

@login_required
def update_lg(request):
    localguide = Guide.objects.get(user=request.user)
    if request.method == 'POST':
         # Update user information based on the form data
         localguide.user.first_name = request.POST.get('first_name')
         localguide.user.last_name = request.POST.get('last_name')
         localguide.user.email  = request.POST.get('email')
         localguide.user.username = request.POST.get('username')
         localguide.user.save()

         location_id = request.POST.get("location")
         location = Location.objects.get(id=location_id)
         localguide.location = location
        
         choice_id = request.POST.get("language")
         language = Language.objects.get(id=choice_id)
         localguide.language = language

         localguide.description = request.POST.get('description')
         localguide.rate_per_hour = request.POST.get('rate_per_hour')

         localguide.contact_info = request.POST.get('contact_info')
         localguide.save()

         return redirect('lgUser')

    locations = Location.objects.all()
    language_choices = Language.objects.all()
    genders = Gender.objects.all()
    return render(request, 'localguides/edit_user.html',{
                    'localguide': localguide,
                    "locations": locations,
                    "language_choices": language_choices,
                    "genders": genders,
        })
    
@login_required
def delete_booking(request, id):
    # Get the booking based on the provided date
    booking = get_object_or_404(Booking, id=id)

    if request.method == 'POST':
        # Delete the booking
        booking.delete()
        # Redirect to some success page or back to the user's profile
        return redirect('lgUser')

@login_required
def send_notification_to_guide(request):
    ml_id = request.session.get('ml_id')
    meet_location = get_object_or_404(Meeting_Location, pk=ml_id)
    booking_id = request.session.get('booking_id')
    booking = get_object_or_404(Booking, pk=booking_id)
    date = booking.booking_date
    guide = get_object_or_404(Guide, pk=booking.guide_id)
    email = guide.user.email
    user = request.user
    f_name = user.first_name
    l_name = user.last_name
    t_email = user.email
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
                        f"Dear {guide.user.first_name},\n\n"
                        f"You booked as a local guide!\n\n"
                        f"Your Tourist name is {f_name} {l_name}.\n"
                        f"Your Tourist email is {t_email}.\n"
                        f"booking date is {date}.\n"
                        f"Click here to view the location on Google Maps: {maps_link}\n\n"
                        "Thanks for booking and we hope you have a great experience!\n\n"
                        "Visit again soon!\n"
                     )

            # Perform email sending logic
            send_mail(
                'Your Tourist detail',
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