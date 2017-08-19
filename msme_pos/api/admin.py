from django.contrib import admin
from api.models import (
    UserProfile,
    MenuItem,
    ItemOrder
)

admin.site.register(UserProfile)
admin.site.register(MenuItem)
admin.site.register(ItemOrder)

