from django.shortcuts import render
import csv
from .models import ProjectCSV
from django.core.paginator import Paginator
from django.contrib import messages

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
