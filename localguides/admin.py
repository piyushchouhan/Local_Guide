from django.contrib import admin
from .models import User, Guide, Language,Location, Gender

admin.site.register(Guide)
admin.site.register(Language)
admin.site.register(Location)
admin.site.register(Gender)
