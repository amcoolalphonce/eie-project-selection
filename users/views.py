from django.shortcuts import render, redirect
from  .models import User
#use my forms
from django.contrib.auth.forms import UserCreationForm
# messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 



# register view
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
