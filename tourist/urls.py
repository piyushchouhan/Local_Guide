from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signUp"),
    path("signin", views.signin_view, name="signIn"),
    path("signout", views.signout_view, name="signOut"),
    path("cityname", views.search_city, name="search_city" ),
    path("autocomplete_city", views.autocomplete_city, name='autocomplete_city'),
    path("user/<int:user_id>", views.user, name="touristUser"),
    path("Logout_and_Redirect", views.Logout_and_Redirect, name="Logout_and_Redirect"),
    path("user/<int:user_id>/edit_user", views.edit_user, name="edit_user"),
    path("user/update_user/<int:user_id>", views.update_user, name="update_user"),
    path('send_email/', views.send_email_with_geolocation, name='send_email_with_geolocation'),
    path('add_trusted_contact/', views.add_trusted_contact, name='add_trusted_contact'),
    path('send_notification_to_user', views.send_notification_to_user, name="send_notification_to_user")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)