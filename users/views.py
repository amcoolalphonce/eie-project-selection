from django.shortcuts import render, redirect
from  .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from base.models import Project, ProjectSelection
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


@login_required
def select_projects(request):
    user = request.user
    projects = Project.objects.all()
    selected_projects = ProjectSelection.objects.filter(user=user).select_related('project')
    selected_project_ids = set(sel.project.id for sel in selected_projects)

    if request.method == 'POST':
        selected_ids = request.POST.getlist('projects')
        if len(selected_ids) + selected_projects.count() > 3:
            messages.error(request, 'You can only select up to 3 projects in total.')
        else:
            for pid in selected_ids:
                if int(pid) not in selected_project_ids:
                    try:
                        project = Project.objects.get(id=pid)
                        ProjectSelection.objects.create(user=user, project=project, timestamp=timezone.now())
                    except Project.DoesNotExist:
                        continue
            messages.success(request, 'Your project selections have been saved.')
        return redirect('users:select_projects')

    return render(request, 'base/select_projects.html', {
        'projects': projects,
        'selected_project_ids': selected_project_ids,
        'selected_projects': selected_projects,
    })
