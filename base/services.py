# services.py
from django.db import transaction
from django.utils import timezone
from collections import defaultdict
from .models import AllocationRound, UserProjectSelection, ProjectAssignment, Project

class ProjectAllocationService:
    
    @transaction.atomic
    def process_current_round(self):
        """Main method called by admin to process assignments"""
        current_round = self.get_current_round()
        if not current_round or current_round.status != 'OPEN':
            return {"success": False, "message": "No open round to process"}
        
        current_round.status = 'PROCESSING'
        current_round.save()
        
        try:
            results = self._allocate_projects(current_round)
            
            # Check if all students are assigned
            if self._all_students_assigned():
                current_round.status = 'COMPLETED'
            else:
                # Start new round for unassigned students
                self._start_next_round()
                current_round.status = 'COMPLETED'
            
            current_round.processed_at = timezone.now()
            current_round.save()
            
            return {"success": True, "results": results}
            
        except Exception as e:
            current_round.status = 'OPEN'  # Rollback status
            current_round.save()
            raise e
    
    def _allocate_projects(self, round_obj):
        """Core allocation logic using your UserProjectSelection model"""
        results = {
            'assigned': [],
            'rejected': [],
            'conflicts_resolved': []
        }
        
        # Get all pending selections for this round
        selections = UserProjectSelection.objects.filter(
            allocation_round=round_obj,
            status='PENDING'
        ).select_related('user', 'project').order_by('choice_priority', 'selected_at')
        
        # Group selections by project and priority
        project_selections = defaultdict(lambda: defaultdict(list))
        
        for selection in selections:
            if selection.project.is_available:
                project_selections[selection.project][selection.choice_priority].append(selection)
        
        # Process each project
        for project, priority_groups in project_selections.items():
            if not project.is_available:
                continue
                
            # Process priorities in order (1st, 2nd, 3rd)
            for priority in sorted(priority_groups.keys()):
                candidates = priority_groups[priority]
                
                if len(candidates) == 1:
                    # Easy case: only one student wants this project at this priority
                    self._assign_project(candidates[0], results)
                    break  # Project is now taken
                    
                elif len(candidates) > 1:
                    # Conflict: multiple students want same project
                    # Sort by timestamp - earliest wins
                    candidates.sort(key=lambda x: x.selected_at)
                    winner = candidates[0]
                    losers = candidates[1:]
                    
                    self._assign_project(winner, results)
                    
                    # Mark others as rejected
                    for loser in losers:
                        loser.status = 'REJECTED'
                        loser.save()
                        results['rejected'].append({
                            'student': loser.user.username,
                            'project': loser.project.project_number,
                            'priority': loser.choice_priority
                        })
                    
                    results['conflicts_resolved'].append({
                        'project': project.project_number,
                        'winner': winner.user.username,
                        'losers': [l.user.username for l in losers]
                    })
                    break  # Project is now taken
        
        return results
    
    def _assign_project(self, selection, results):
        """Assign a project to a user"""
        # Create assignment
        ProjectAssignment.objects.create(
            user=selection.user,
            project=selection.project,
            assigned_round=selection.allocation_round,
            priority_level=selection.choice_priority
        )
        
        # Update project
        selection.project.is_available = False
        selection.project.assigned_student = selection.user
        selection.project.save()
        
        # Update selection
        selection.status = 'ASSIGNED'
        selection.save()
        
        # Mark other selections by this user as rejected
        UserProjectSelection.objects.filter(
            user=selection.user,
            allocation_round=selection.allocation_round,
            status='PENDING'
        ).exclude(id=selection.id).update(status='REJECTED')
        
        results['assigned'].append({
            'student': selection.user.username,
            'project': selection.project.project_number,
            'priority': selection.choice_priority
        })
    
    def _all_students_assigned(self):
        """Check if all students have assignments"""
        students_with_selections = User.objects.filter(
            userprojectselection__isnull=False
        ).distinct()
        assigned_students = User.objects.filter(
            project_assignment__isnull=False
        ).distinct()
        
        return students_with_selections.count() == assigned_students.count()
    
    def _start_next_round(self):
        """Start a new round for unassigned students"""
        latest_round = AllocationRound.objects.order_by('-round_number').first()
        current_round_num = latest_round.round_number if latest_round else 0
        AllocationRound.objects.create(
            round_number=current_round_num + 1,
            status='OPEN'
        )
    
    def get_current_round(self):
        """Get the current allocation round"""
        return AllocationRound.objects.filter(status='OPEN').first()
    
    def get_or_create_initial_round(self):
        """Get current round or create first one"""
        current_round = self.get_current_round()
        if not current_round:
            current_round = AllocationRound.objects.create(
                round_number=1,
                status='OPEN'
            )
        return current_round