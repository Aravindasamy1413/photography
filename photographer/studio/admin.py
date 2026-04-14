from django.contrib import admin
from .models import Booking, FrameOrder, Gallery

admin.site.register(Booking)
admin.site.register(Gallery)

class FrameOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'frame_type', 'status']
    list_editable = ['status']

admin.site.register(FrameOrder, FrameOrderAdmin)