from django.db import models
from django.utils import timezone
from users.models import User


class ProjectCSV(models.Model):
    file = models.FileField(upload_to='project_csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CSV uploaded at {self.uploaded_at}"

class Project(models.Model):
    project_title = models.CharField(max_length=255, default='')
    project_number = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.project_number
    

class UserProjectSelection(models.Model):
    CHOICE_OPTIONS = [
        (1, '1st Choice'),
        (2, '2nd Choice'), 
        (3, '3rd Choice'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)
    choice_priority = models.IntegerField(choices=CHOICE_OPTIONS, null = True)
    unique_together = ('user', 'choice_priority')

    class Meta:
        verbose_name = 'User Project Selection'
        verbose_name_plural = 'User Project Selections'
        
    def __str__(self):
        return f"{self.project.project_number} - ({self.get_choice_priority_display()})"
    