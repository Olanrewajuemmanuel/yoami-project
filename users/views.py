from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib import messages

from .forms import UserForm

# Create your views here.


def login(request):
    return HttpResponse("Hi")


def register(request):
    template_name = 'users/register.html'
    form = UserForm()
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']

            
            try:
                user = User.objects.create(
                username=email, first_name=first_name, last_name=last_name, email=email, password=password1)
                login(request, user)
                print(request.user.is_authenticated, request.user)
            except:
                raise


    return render(request, template_name, {'form': form})
