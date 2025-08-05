from django.shortcuts import render
import csv
from .models import ProjectCSV
from django.http import HttpResponse
#messages
from django.contrib import messages

def home(request):
    latest_csv = ProjectCSV.objects.last()
    
    if not latest_csv:
        messages.error(request, "No CSV file uploaded yet.")
    
    projects = []
    

    with latest_csv.file.open('r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            project = {
                'PROJECT NUMBER': row.get('NUMBER', ''),
                'PROJECT TITLE': row.get('TITLE', ''), 
    
            }
            projects.append(project)
            print(project)
    
    return render(request, 'base/results.html', {'projects': projects})
