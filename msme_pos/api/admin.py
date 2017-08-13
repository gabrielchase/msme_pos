from django.contrib import admin
from api.models import (
    UserProfile,
    MenuItem
)

admin.site.register(UserProfile)
admin.site.register(MenuItem)

