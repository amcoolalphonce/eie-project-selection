from django.shortcuts import render,redirect
import csv
from .models import ProjectCSV, Project, UserProjectSelection
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    latest_csv = ProjectCSV.objects.last()
    
    if not latest_csv:
        messages.error(request, "No CSV file uploaded yet.")
        return render(request, 'base/home.html', {'page_obj': None})

    projects = []
    with latest_csv.file.open('r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            project = {
                'PRJ_NUMBER': row.get('prj_number', ''),
                'PRJ_TITLE': row.get('prj_title', ''),
            }
            projects.append(project)

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
def project_list(request):
    if request.method == 'POST':
        return handle_project_selection(request)
    
    
    list_of_projects = Project.objects.all()
    paginator = Paginator(list_of_projects, 10)  
    page_number = request.GET.get('page')   
    page_obj = paginator.get_page(page_number)
    return render(request, 'base/project_list.html', {'page_obj': page_obj})
    
    user_selections = UserProjectSelection.objects.filter(user=request.user).values_list('project__project_title', flat=True)
    
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
    if new_selections > 3:
        messages.error(request, "You can only select a maximum of 3 projects.")
        return redirect('project_list')
    
    try:
        current_selections.delete()

        for project_id in selected_project_ids:
            project = Project.objects.get(id=project_id)
            UserProjectSelection.objects.create(
                user=request.user,
                project=project
            )
        
        messages.success(request, f"Successfully selected {new_selections} project(s)!")
        
    except Project.DoesNotExist:
        messages.error(request, "One or more selected projects do not exist.")
    except Exception as e:
        messages.error(request, "An error occurred while saving your selections.")
    
    return redirect('project_list')