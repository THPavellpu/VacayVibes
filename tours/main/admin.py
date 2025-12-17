from django.contrib import admin
from django.utils.html import format_html
from .models import TourPackage


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_active', 'image_thumb')
    list_filter = ('category', 'is_active')
    search_fields = ('title',)

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: auto; object-fit: cover;"/>', obj.image.url)
        return '-'

    image_thumb.short_description = 'Image'
