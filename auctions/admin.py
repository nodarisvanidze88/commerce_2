from django.contrib import admin
from .models import Catrgory, Listing, User

# Register your models here.

admin.site.register(Catrgory)
admin.site.register(Listing)
admin.site.register(User)
