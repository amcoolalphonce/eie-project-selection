from django import forms
from .models import Project, UserProjectSelection

class ProjectSelectionForm(forms.Form):
    project_1 = forms.CharField(
        max_length=255,
        label="1st Choice Project Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter project number'})
    )
    project_2 = forms.CharField(
        max_length=255,
        label="2nd Choice Project Number", 
        widget=forms.TextInput(attrs={'placeholder': 'Enter project number'})
    )
    project_3 = forms.CharField(
        max_length=255,
        label="3rd Choice Project Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter project number'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        project_1 = cleaned_data.get('project_1')
        project_2 = cleaned_data.get('project_2')
        project_3 = cleaned_data.get('project_3')
        
        # 3 must be selected
        if not all([project_1, project_2, project_3]):
            raise forms.ValidationError("All three project numbers must be provided.")
        
        # Check for duplicates
        projects = [project_1, project_2, project_3]
        if len(set(projects)) != len(projects):
            raise forms.ValidationError("You cannot select the same project number multiple times.")
        
        # Validate that all project numbers exist in the database
        for i, project_num in enumerate(projects, 1):
            try:
                Project.objects.get(project_number=project_num)
            except Project.DoesNotExist:
                raise forms.ValidationError(f"Project number '{project_num}' does not exist.")
        
        return cleaned_data