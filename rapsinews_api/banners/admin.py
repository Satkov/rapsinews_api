from django.contrib import admin
from .models import Banner, Image

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'is_active']
    list_editable = ['is_active']

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            Banner.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "images":
            kwargs["queryset"] = Image.objects.all().order_by("name")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
