from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("localguide", views.index, name="localGuide"),
    path("localguide/signup", views.localGuide_signup_view, name="localGuide_signUp"),
    path("localguide/signout", views.localGuide_signout_view, name="localGuide_signOut"),
    path("localguide/signin", views.localGuide_signin_view, name="localGuide_signIn"),
    path("localguide/<int:local_guide_id>", views.lg_detail, name="guide_detail"),
    path("localguide/about_us", views.about_us, name="about_us"),
    path("localguide/privacy", views.privacy, name="privacy"),
    path("localguide/terms", views.terms, name="terms"),
    path("localguide/book_date", views.book_date, name="book_date"),
    path("localguide/user/", views.user, name="lgUser"),
    path("logout_and_redirect/", views.logout_and_redirect, name='logout_and_redirect'),
    path("localguides/user/edit_profile", views.edit_lg, name="edit_lg"),
    path("localguides/user/update_profile", views.update_lg, name="update_lg"),
    path('localguide/user/<int:id>/', views.delete_booking, name='delete_booking'),
    path('send_notification_to_guide', views.send_notification_to_guide, name="send_notification_to_guide")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)