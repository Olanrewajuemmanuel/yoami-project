from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages

from .forms import UserLoginForm, UserRegistrationForm
from .decorators import decorators
from cart.models import Cart

# Create your views here.

@decorators.redirect_if_loggedin
def user_login(request):
    template_name = 'users/login.html'
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('store_main:index')
            messages.error(
                request, "Error logging you in. Username or password may be incorrect.")
            messages.error(request, None)  # clear messages
    else:
        form = UserLoginForm()
    return render(request, template_name, {'form': form})

@decorators.redirect_if_loggedin
def user_register(request):
    template_name = 'users/register.html'
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password1 = make_password(form.cleaned_data['password1']) # hashing algorithm from Django
            
            try:
                user = User.objects.create(
                    email=email, first_name=first_name, last_name=last_name, password=password1)
                user.username = email

                # Create a user cart
                print(user)
                Cart.objects.create(user=user)
                user.save()

                # login user and redirect
                login(request, user)
                return redirect('store_main:index') 
                
            except IntegrityError:
                messages.error(
            request, "Unsuccessful registration. Email has already been used.")
                messages.error(request, None)

            

        messages.error(
            request, "Unsuccessful registration. Please try again later.")
        messages.error(request, None)
    else:
        # any other type of request
        form = UserRegistrationForm()
    return render(request, template_name, {'form': form})


def user_logout(request):
    logout(request)
    return redirect('store_main:index')
