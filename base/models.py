from django.db import models
from users.models import User


class ProjectCSV(models.Model):
    file = models.FileField(upload_to='project_csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CSV uploaded at {self.uploaded_at}"

class Project(models.Model):
    prj_number = models.CharField(max_length=20, unique=True)
    prj_title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.prj_number}: {self.prj_title}"

class ProjectSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')