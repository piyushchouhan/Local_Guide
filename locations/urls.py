from django.urls import path
from . import views

urlpatterns = [
    path('meetlocation', views.meet_location, name="meet_location"),
    path('process_location_data', views.process_location_data, name='process_location_data'),
]
