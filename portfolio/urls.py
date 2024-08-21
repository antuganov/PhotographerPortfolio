from django.urls import path
from . import views

urlpatterns = [
    path("", views.MainPage.as_view(), name="main-page"),
    path("series", views.SeriesView.as_view(), name="series"),
    path("series/<slug:slug>", views.SerieView.as_view(), name="serie"),
    path("about", views.AboutView.as_view(), name="about"),
    path("contact", views.ContactView.as_view(), name="contact"),
    path("success", views.SuccessView.as_view(), name="success"),
]
