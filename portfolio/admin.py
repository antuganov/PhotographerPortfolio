from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline
from multiupload.admin import MultiUploadAdmin
from .models import Gallery, Image, ImageInGallery


class ImageTabularInline(SortableTabularInline):
    model = ImageInGallery
    extra = 0
    fields = ["image_preview", "image"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        image = obj.image
        preview_size = 150
        if image.file:
            return format_html(
                f'<img src="{image.file.url}" style="max-width:{preview_size}px"/><br>'
            )
        return ""


@admin.register(Gallery)
class GalleryAdmin(SortableAdminMixin, MultiUploadAdmin):
    multiupload_form = True
    multiupload_list = False
    multiupload_maxfilesize = 1000 * 2**20
    multiupload_acceptedformats = ("image/jpeg", "image/png", "image/webp")

    list_display = ["title", "type", "description", "date", "order"]
    inlines = [ImageTabularInline]

    prepopulated_fields = {"slug": ("title",)}

    def main_image_preview(self, obj):
        image = obj.image
        if image is not None:
            return format_html(f'<img src="{image.file.url}">')
        return None

    def process_uploaded_file(self, uploaded, object, request):
        image = Image(file=uploaded)
        image.save()
        image_in_gallery = ImageInGallery(gallery=object, image=image)
        image_in_gallery.save()
        return {
            "url": image.file.url,
            "thumbnail_url": image.file.url,
            "id": image_in_gallery.id,
            "name": uploaded.name,
        }

    def delete_file(self, pk, request):
        image_in_gallery = get_object_or_404(
            ImageInGallery.get_queryset(request), pk=pk
        )
        return image_in_gallery.delete()

    def delete_queryset(self, request, queryset):
        for gallery in queryset:
            gallery.delete()


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def image_preview(self, obj):
        image = obj
        preview_size = 75
        if image.file:
            return format_html(
                f'<img src="{image.file.url}" style="max-width:{preview_size}px"/><br>'
            )
        return ""

    def gallery(self, obj):
        image = ImageInGallery.objects.filter(image=obj).first()
        if image:
            return image.gallery.title
        return None

    list_display = ["image_preview", "description", "gallery"]
    readonly_fields = ["image_preview"]
