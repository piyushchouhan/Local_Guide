from django.urls import path
from . import views

urlpatterns = [
    path('city/<str:city_name>', views.city, name='city')
]