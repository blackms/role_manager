from collections import defaultdict
from datetime import datetime, timedelta
from models import db, RoleRequest

class RoleManager:
    def __init__(self):
        self.roles = {
            'secretary_of_strategy': [],
            'secretary_of_security': [],
            'secretary_of_development': [],
            'secretary_of_science': [],
            'secretary_of_interior': []
        }
        self.current_assignments = {}
        self.start_times = {}
        self.assignment_duration = 5  # Duration in minutes

    def add_request(self, role, request):
        self.roles[role].append(request)

    def assign_role(self, role):
        if role in self.roles and self.roles[role]:
            player_request = self.roles[role].pop(0)
            self.current_assignments[role] = player_request
            self.start_times[role] = datetime.utcnow()
            return player_request
        return None

    def release_role(self, role):
        if role in self.current_assignments:
            del self.current_assignments[role]
            del self.start_times[role]

    def get_remaining_time(self, role):
        role_request = RoleRequest.query.filter_by(role=role, status='assigned').first()
        if role_request:
            assign_duration = timedelta(minutes=5)  # 5 minutes for the role assignment
            time_elapsed = datetime.utcnow() - role_request.assign_time
            remaining_time = assign_duration - time_elapsed
            if remaining_time.total_seconds() > 0:
                return remaining_time.total_seconds() / 60  # return in minutes
            else:
                self.release_role(role)
                return 0
        return 0

    def get_roles_with_requests(self):
        roles_with_requests = defaultdict(list)
        for role, queue in self.roles.items():
            roles_with_requests[role] = queue
        return roles_with_requests

    def is_role_assigned(self, role):
        return role in self.current_assignments

role_manager = RoleManager()
