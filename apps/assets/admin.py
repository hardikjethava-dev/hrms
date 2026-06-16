from django.contrib import admin
from .models import Asset, AssetAllocation

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_code', 'name', 'category', 'status')
    list_filter = ('status', 'category')
    search_fields = ('asset_code', 'name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AssetAllocation)
class AssetAllocationAdmin(admin.ModelAdmin):
    list_display = ('asset', 'employee', 'allocated_date', 'returned_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'asset__name')
    readonly_fields = ('created_at', 'updated_at')
