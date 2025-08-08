from django.shortcuts import render,redirect
import csv
from .models import ProjectCSV, Project, UserProjectSelection
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    if request.method == 'POST':
        return handle_project_selection(request)
    
    list_of_projects = Project.objects.all().order_by('-created_at')
    paginator = Paginator(list_of_projects, 200)  
    page_number = request.GET.get('page')   
    page_obj = paginator.get_page(page_number)
    
    #user's current selections
    user_selections = UserProjectSelection.objects.filter(user=request.user).values_list('project__id', flat=True)
    
    context = {
        'page_obj': page_obj,
        'user_selections': list(user_selections),
        'selection_count': len(user_selections),
        'max_selection': 3,
    }
    return render(request, 'base/project_list.html', context)


def handle_project_selection(request):
    selected_project_ids = request.POST.getlist('selected_projects')
    current_selections = UserProjectSelection.objects.filter(user=request.user)
    current_count = current_selections.count()
    new_selections = len(selected_project_ids)
    
    # If user tries to select more than 3 projects, clear all and start over
    if new_selections > 3:
        current_selections.delete()
        messages.error(request, "You tried to select more than 3 projects. All selections have been cleared. Please select exactly 3 projects.")
        return redirect('select_projects')
    
    # If user has 3 selections and tries to select any new project(s), clear all
    if current_count == 3 and new_selections > 0:
        # Check if the new selection is different from current selections
        current_project_ids = set(current_selections.values_list('project__id', flat=True))
        new_project_ids = set(int(pid) for pid in selected_project_ids)
        
        if new_project_ids != current_project_ids:
            current_selections.delete()
            messages.warning(request, "You already had 3 projects selected. Your previous selections have been cleared. Please select exactly 3 projects.")
            return redirect('select_projects')
    
    # Only allow saving if exactly 3 projects are selected
    if new_selections != 3:
        messages.error(request, "You must select exactly 3 projects.")
        return redirect('select_projects')
    
    try:
        # Clear existing selections and save new ones
        current_selections.delete()

        for project_id in selected_project_ids:
            project = Project.objects.get(id=project_id)
            UserProjectSelection.objects.create(
                user=request.user,
                project=project
            )
        
        messages.success(request, f"Successfully selected 3 projects!")
        
    except Project.DoesNotExist:
        messages.error(request, "One or more selected projects do not exist.")
    except Exception as e:
        messages.error(request, "An error occurred while saving your selections.")
    
    return redirect('select_projects')


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