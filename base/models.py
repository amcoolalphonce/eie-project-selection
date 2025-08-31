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
    is_available = models.BooleanField(default=True)
    assigned_student = models.OneToOneField(User, null = True, blank = True, on_delete= models.CASCADE)


    def __str__(self):
        return self.project_number
    

class UserProjectSelection(models.Model):
    CHOICE_OPTIONS = [
        (1, '1st Choice'),
        (2, '2nd Choice'), 
        (3, '3rd Choice'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)
    choice_priority = models.IntegerField(choices=CHOICE_OPTIONS, null = True)
    allocation_round = models.ForeignKey('AllocationRound', on_delete= models.CASCADE, null = True, blank = True)
    status  = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')


    class Meta:
        verbose_name = 'User Project Selection'
        verbose_name_plural = 'User Project Selections'
        unique_together = ('user', 'choice_priority', 'allocation_round')
        
    def __str__(self):
        return f"{self.project.project_number} - ({self.get_choice_priority_display()})"



class AllocationRound(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open for Selection'),
        ('PROCESSING', 'Processing Assignments'),
        ('COMPLETED', 'Completed'),
    ]
    round_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-round_number']

    def __str__(self):
        return f"Round {self.round_number} - {self.status}"


class ProjectAssignment(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'project_assignment')
    project = models.OneToOneField(Project, on_delete = models.CASCADE,  related_name='assignment')
    assigned_round = models.ForeignKey(AllocationRound, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    priority_level = models.IntegerField() 
    
    def __str__(self):
        return f"{self.user.username} -> {self.project.project_number}"