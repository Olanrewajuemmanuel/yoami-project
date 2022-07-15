from django import forms
from django.core.exceptions import ValidationError
from django.core import validators


    
class UserForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    password1 = forms.CharField(max_length=1024, widget=forms.PasswordInput, min_length=8, validators=[validators.MinLengthValidator])
    password2 = forms.CharField(max_length=1024, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match")


