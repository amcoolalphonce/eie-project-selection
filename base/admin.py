from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import ProjectCSV, Project, UserProjectSelection
import csv
import io
from django.core.exceptions import ValidationError


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_number', 'project_title', 'created_at')
    search_fields = ('project_number', 'project_title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    
    actions = ['import_from_csv']
    
    def import_from_csv(self, request, queryset):
        """Admin action to import projects from CSV"""
        # This is a placeholder action - the actual import will be done via management command
        messages.info(request, 'Please use the management command: python manage.py import_projects_csv <file.csv>')
        return
    
    import_from_csv.short_description = "Import projects from CSV (use management command)"
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add CSV upload instructions"""
        extra_context = extra_context or {}
        extra_context['show_csv_info'] = True
        return super().changelist_view(request, extra_context)


@admin.register(ProjectCSV)
class ProjectCSVAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)


@admin.register(UserProjectSelection)
class UserProjectSelectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'selected_at')
    list_filter = ('selected_at', 'user')
    search_fields = ('user__username', 'user__email', 'project__project_title', 'project__project_number')
    readonly_fields = ('selected_at',)
    ordering = ('-selected_at',)
