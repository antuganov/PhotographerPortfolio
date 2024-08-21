from django.db import models
from django.core.files.images import get_image_dimensions
from django.urls import reverse
from datetime import date


class Image(models.Model):
    file = models.FileField(upload_to="images/")
    description = models.TextField(blank=True, null=True)
    width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    height = models.PositiveIntegerField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        width, height = get_image_dimensions(self.file)
        self.width = width
        self.height = height

        super().save(*args, **kwargs)

    def __str__(self):
        return self.file.name.rsplit("/", 1)[-1]


class Gallery(models.Model):
    GALLERY_TYPES = (("main", "Main Page"), ("serie", "Serie"))

    images = models.ManyToManyField(
        Image, through="ImageInGallery", related_name="galleries"
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    title_image = models.FileField(upload_to="images/", blank=True)
    type = models.CharField(max_length=10, choices=GALLERY_TYPES, default="serie")
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    date = models.DateField(default=date.today, blank=True, null=True)
    slug = models.SlugField(default="", null=False, db_index=True, unique=True)
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, db_index=True
    )

    @property
    def first_image_in_gallery(self):
        try:
            return self.imageingallery_set.order_by("order").first().image.file.url
        except AttributeError:
            return None

    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ["order"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("serie", kwargs={"slug": self.slug})

    def delete(self, *args, **kwargs):
        for image_in_gallery in self.imageingallery_set.all():
            image_in_gallery.delete()
        super().delete(*args, **kwargs)


class ImageInGallery(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, db_index=True
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.image} in {self.gallery.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
