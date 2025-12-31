from django.contrib import admin
from django.utils.html import format_html
from .models import TourPackage


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'days_nights', 'inclusion_list', 'price', 'is_active', 'image_thumb')
    list_filter = ('category', 'is_active')
    search_fields = ('title',)
    filter_horizontal = ('inclusions',)
    fields = ('title', 'category', 'days', 'nights', 'duration', 'people', 'price', 'inclusions', 'image', 'is_active')

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: auto; object-fit: cover;"/>', obj.image.url)
        return '-'

    image_thumb.short_description = 'Image'

    def days_nights(self, obj):
        if obj.days or obj.nights:
            return f"{obj.days}D {obj.nights}N"
        return obj.duration or '-'

    days_nights.short_description = 'Duration'

    def inclusion_list(self, obj):
        incs = obj.inclusions.all()
        if not incs:
            return '-'
        return ', '.join([i.name for i in incs])

    inclusion_list.short_description = 'Inclusions'


from .models import Inclusion


@admin.register(Inclusion)
class InclusionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'source', 'package', 'created_at')
    list_filter = ('source', 'created_at')
    search_fields = ('email', 'name', 'phone')
    readonly_fields = ('created_at',)
