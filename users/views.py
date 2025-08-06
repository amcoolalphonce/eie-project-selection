from django.shortcuts import render, redirect
from  .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from base.models import Project
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

def register(request):  
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error creating account. Please try again.')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

