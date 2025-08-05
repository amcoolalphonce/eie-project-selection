from django.db import models


class ProjectCSV(models.Model):
    file = models.FileField(upload_to='project_csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CSV uploaded at {self.uploaded_at}"