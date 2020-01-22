from django.contrib import admin

# Register your models here.

from .models import UserUpload

admin.site.register(UserUpload)
