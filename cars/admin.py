from django.contrib import admin
from .models import Manufacturer, Car, Review, TestDriveRequest

admin.site.register(Car)
admin.site.register(Manufacturer)
admin.site.register(Review)

@admin.register(TestDriveRequest)
class TestDriveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'full_name', 'phone', 'preferred_date', 'created_at')
    list_filter = ('preferred_date', 'created_at')
    search_fields = ('full_name', 'phone', 'car__model', 'car__brand__name')