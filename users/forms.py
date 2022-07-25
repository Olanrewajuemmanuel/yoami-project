from django import forms
from django.core.exceptions import ValidationError
from django.core import validators


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=1024, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), min_length=8, validators=[validators.MinLengthValidator], label='Password')
    password2 = forms.CharField(
        max_length=1024, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Verify password')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match")


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=1024, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
