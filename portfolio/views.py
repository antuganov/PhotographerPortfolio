from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, TemplateView, FormView, DetailView
from django.core.mail import send_mail
from django.conf import settings

from .models import ImageInGallery, Gallery
from .forms import ContactForm


class MainPage(ListView):
    template_name = "portfolio/main.html"
    model = ImageInGallery
    context_object_name = "main_gallery"

    # Return images from galleries with type "main"
    def get_queryset(self):
        return ImageInGallery.objects.filter(gallery__type="main")


class SeriesView(ListView):
    template_name = "portfolio/series.html"
    model = Gallery
    context_object_name = "galleries"

    # Return galleries only with type "serie"
    def get_queryset(self):
        return Gallery.objects.filter(type="serie").order_by("-date").all()


class SerieView(DetailView):
    model = Gallery
    template_name = "portfolio/serie.html"
    context_object_name = "serie"
    slug_url_kwarg = "slug"
    slug_field = "slug"


class AboutView(TemplateView):
    template_name = "portfolio/about.html"


class ContactView(FormView):
    form_class = ContactForm
    template_name = "portfolio/contact.html"

    def get_success_url(self):
        return reverse("success")

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        full_message = f"""
            Received message below from {name}, {email}
            ________________________
            {subject}



            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)


class SuccessView(TemplateView):
    template_name = "portfolio/success.html"
