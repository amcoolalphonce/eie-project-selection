from django.contrib import admin
from .models import ProjectCSV, Project, UserProjectSelection


admin.site.register(ProjectCSV)
admin.site.register(Project)
admin.site.register(UserProjectSelection)
