from django.shortcuts import render,redirect
import csv
from .models import ProjectCSV, Project, UserProjectSelection
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProjectSelectionForm
from django.db import transaction


def home(request):
    # Get all projects from the database
    projects = Project.objects.all().order_by('-created_at')
    
    if not projects.exists():
        messages.info(request, "No projects available yet. Please contact an administrator to add projects.")
        return render(request, 'base/home.html', {'page_obj': None})

    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'base/home.html', {'page_obj': page_obj})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'base/login.html')
    return render(request, 'base/login.html')


def custom_logout(request):
    logout(request)
    return redirect('home')


@login_required
def select_projects(request):
    # Get user's current selections to pre-populate form
    current_selections = UserProjectSelection.objects.filter(user=request.user).order_by('choice_priority')
    initial_data = {}
    
    for selection in current_selections:
        if selection.choice_priority == 1:
            initial_data['project_1'] = selection.project.project_number
        elif selection.choice_priority == 2:
            initial_data['project_2'] = selection.project.project_number
        elif selection.choice_priority == 3:
            initial_data['project_3'] = selection.project.project_number
    
    if request.method == 'POST':
        form = ProjectSelectionForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Delete existing selections for this user
                    UserProjectSelection.objects.filter(user=request.user).delete()
                    
                    # Create new selections
                    project_numbers = [
                        form.cleaned_data['project_1'],
                        form.cleaned_data['project_2'], 
                        form.cleaned_data['project_3']
                    ]
                    
                    for priority, project_number in enumerate(project_numbers, 1):
                        project = Project.objects.get(project_number=project_number)
                        UserProjectSelection.objects.create(
                            user=request.user,
                            project=project,
                            choice_priority=priority
                        )
                    
                    messages.success(request, 'Your project selections have been saved successfully!')
                    return redirect('select_projects')  # Redirect to avoid re-submission
                    
            except Exception as e:
                messages.error(request, f'An error occurred while saving your selections: {str(e)}')
    else:
        form = ProjectSelectionForm(initial=initial_data)
    
    context = {
        'form': form,
        'current_selections': current_selections,
    }
    return render(request, 'base/select_projects.html', context)



# user selected projects view
@login_required
def user_selected_projects(request):
    user_selections = UserProjectSelection.objects.filter(user=request.user)
    selected_projects = [selection.project for selection in user_selections]
    
    context = {
        'selected_projects': selected_projects,
        'selection_count': len(selected_projects),
    }
    
    return render(request, 'base/user_selected_projects.html', context)