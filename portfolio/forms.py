from django import forms
from django.core.validators import MaxLengthValidator, EmailValidator


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=255,
        label="Name",
        validators=[MaxLengthValidator(255)],
        widget=forms.TextInput(
            attrs={"placeholder": "Name", "class": "form-control form__input"}
        ),
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        validators=[EmailValidator],
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control form__input"}
        ),
    )
    subject = forms.CharField(
        required=True,
        max_length=255,
        label="Subject",
        validators=[MaxLengthValidator(255)],
        widget=forms.TextInput(
            attrs={"placeholder": "Subject", "class": "form-control form__input"}
        ),
    )
    message = forms.CharField(
        required=True,
        label="Message",
        validators=[MaxLengthValidator(5000)],
        widget=forms.Textarea(
            attrs={"placeholder": "Message", "class": "form-control form__input"}
        ),
    )
