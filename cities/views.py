from django.shortcuts import render, get_object_or_404
from localguides.models import Location, Guide,Language, Gender
    
def city(request, city_name):
    location = get_object_or_404(Location, location_name=city_name)
    
    # Get the selected language and gender from the query parameters (if available)
    selected_language = request.GET.get('language')
    selected_gender = request.GET.get('gender')

    # Filter local guides by location
    local_guides = Guide.objects.filter(location=location)

    # Filter local guides by selected language (if provided)
    if selected_language:
        local_guides = local_guides.filter(language__language=selected_language)

    # Filter local guides by selected gender (if provided)
    if selected_gender:
        local_guides = local_guides.filter(gender__gender=selected_gender)
    

    language_choices = Language.objects.all()
    gender_choices = Gender.objects.all()
    return render(request, "cities/city.html", {
        'city': location,
        'local_guides': local_guides,
        'selected_language': selected_language,
        'selected_gender': selected_gender,
        'gender_choices' :gender_choices,
        'language_choices' : language_choices,
    })


