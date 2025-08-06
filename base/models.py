from django.db import models
from users.models import User


class ProjectCSV(models.Model):
    file = models.FileField(upload_to='project_csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CSV uploaded at {self.uploaded_at}"

class Project(models.Model):
    project_title = models.CharField(max_length=255, default='')
    project_number = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.project_title