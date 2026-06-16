from django.contrib import admin
from .models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'is_optional')
    list_filter = ('is_optional',)
    search_fields = ('name',)
    ordering = ('date',)
    readonly_fields = ('created_at', 'updated_at')
