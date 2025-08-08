from django.core.management.base import BaseCommand
from base.models import Project
import csv
import os


class Command(BaseCommand):
    help = 'Import projects from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {csv_file_path}')
            )
            return
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Check for different CSV formats
                fieldnames = reader.fieldnames or []
                
                # Define possible column mappings
                column_mappings = [
                    {'project_number': 'project_number', 'project_title': 'project_title'},
                    {'project_number': 'PRJ', 'project_title': 'TITLE'},
                    {'project_number': 'prj_number', 'project_title': 'prj_title'},
                    {'project_number': 'number', 'project_title': 'title'},
                ]
                
                # Find the correct mapping
                mapping = None
                for possible_mapping in column_mappings:
                    if all(col in fieldnames for col in possible_mapping.values()):
                        mapping = possible_mapping
                        break
                
                if not mapping:
                    self.stdout.write(
                        self.style.ERROR(f'CSV must contain columns for project number and title. Found columns: {", ".join(fieldnames)}')
                    )
                    return
                
                self.stdout.write(
                    self.style.SUCCESS(f'Detected CSV format: {mapping["project_number"]}/{mapping["project_title"]}')
                )
                
                projects_created = 0
                projects_updated = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        project_number = row.get(mapping['project_number'], '').strip()
                        project_title = row.get(mapping['project_title'], '').strip()
                        
                        if not project_number or not project_title:
                            errors.append(f'Row {row_num}: Project number and title are required')
                            continue
                        
                        # Check if project already exists
                        project, created = Project.objects.get_or_create(
                            project_number=project_number,
                            defaults={'project_title': project_title}
                        )
                        
                        if created:
                            projects_created += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'Created: {project_number} - {project_title}')
                            )
                        else:
                            # Update existing project
                            project.project_title = project_title
                            project.save()
                            projects_updated += 1
                            self.stdout.write(
                                self.style.WARNING(f'Updated: {project_number} - {project_title}')
                            )
                            
                    except Exception as e:
                        errors.append(f'Row {row_num}: {str(e)}')
                
                # Show summary
                self.stdout.write('\n' + '='*50)
                self.stdout.write('IMPORT SUMMARY')
                self.stdout.write('='*50)
                
                if projects_created > 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created {projects_created} new projects.')
                    )
                if projects_updated > 0:
                    self.stdout.write(
                        self.style.WARNING(f'Updated {projects_updated} existing projects.')
                    )
                if errors:
                    self.stdout.write(
                        self.style.ERROR(f'Encountered {len(errors)} errors:')
                    )
                    for error in errors[:10]:  # Show first 10 errors
                        self.stdout.write(f'  - {error}')
                    if len(errors) > 10:
                        self.stdout.write(f'  ... and {len(errors) - 10} more errors.')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing CSV file: {str(e)}')
            ) 