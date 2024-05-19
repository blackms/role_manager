from flask import Blueprint, render_template, jsonify
from models import db
from role_manager import role_manager

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    with db.session() as session:
        roles_with_requests = role_manager.get_roles_with_requests()
        current_assignments = role_manager.current_assignments
        start_times = role_manager.start_times
        remaining_times = {
            role: role_manager.get_remaining_time(role) if role_manager.is_role_assigned(role) else ''
            for role in role_manager.roles.keys()
        }
        return render_template('index.html', roles=roles_with_requests, assignments=current_assignments, start_times=start_times, remaining_times=remaining_times)
