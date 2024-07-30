from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """
    Represents a location for a guide.
    """
    location_name = models.CharField(max_length=255)
    location_image = models.ImageField(upload_to='location_images/', null=True, blank=True)

    def __str__(self):
        return self.location_name


class Language(models.Model):
    """
    Represents a language spoken by a guide.
    """
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language


class Gender(models.Model):
    """
    Represents a gender of a guide.
    """
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.gender


class Guide(models.Model):
    """
    Represents a guide.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField()
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    contact_info = models.CharField(max_length=255)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='localguide_images/', null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Booking(models.Model):
    """
    Represents a booking made by a user for a guide.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    booking_status = models.CharField(max_length=255)


class Payment(models.Model):
    """
    Represents a payment made for a booking.
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_status = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)


class TrustedContact(models.Model):
    """
    Represents a trusted contact for a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)


class Review(models.Model):
    """
    Represents a review given by a user for a guide.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField()
