from django.contrib import admin

# Register your models here.
from .models import Donation,Rating
admin.site.register(Donation)
admin.site.register(Rating)