from django.contrib import admin

from .models import SKU


@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "unit", "barcode", "updated_at"]
    search_fields = ["name", "barcode", "category"]
    list_filter = ["category"]
