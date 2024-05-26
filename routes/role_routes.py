from flask import Blueprint, jsonify, request
from models import db, RoleRequest
from role_manager import role_manager
from datetime import datetime

role_routes = Blueprint('roles', __name__)

@role_routes.route('/api/roles', methods=['GET'])
def get_roles():
    roles_with_requests = {}
    current_assignments = {}

    roles = RoleRequest.query.filter_by(status='waiting').all()
    assignments = RoleRequest.query.filter_by(status='assigned').all()

    for role in roles:
        if role.role not in roles_with_requests:
            roles_with_requests[role.role] = []
        roles_with_requests[role.role].append({
            'player': role.player,
            'coordinates': role.coordinates
        })

    for assignment in assignments:
        current_assignments[assignment.role] = {
            'player': assignment.player,
            'remaining_time': 5  # assuming a fixed time for demonstration
        }

    return jsonify({
        'roles': [{'role': role, 'requests': requests} for role, requests in roles_with_requests.items()],
        'assignments': [{'role': role, 'player': assignment['player'], 'remaining_time': assignment['remaining_time']} for role, assignment in current_assignments.items()]
    })

@role_routes.route('/api/request_role', methods=['POST'])
def request_role():
    player_name = request.form['player']
    role = request.form['role']
    coordinates = request.form['coordinates']
    if not coordinates:
        coordinates = None

    alliance, player = player_name.split(']')
    alliance = alliance[1:].lower()
    player = player.lower()
    new_request = RoleRequest(
        alliance=alliance,
        player=player,
        role=role,
        coordinates=coordinates,
        request_time=datetime.utcnow(),
        status='waiting'
    )
    db.session.add(new_request)
    db.session.commit()
    role_manager.add_request(role, new_request)

    return jsonify({'status': 'success'})

@role_routes.route('/assign_role/<role>')
def assign_role(role):
    player_request = role_manager.assign_role(role)
    if player_request:
        player_request.status = 'assigned'
        player_request.assign_time = datetime.utcnow()
        db.session.commit()
        remaining_time = role_manager.get_remaining_time(role)
        return jsonify({
            'status': 'success',
            'player': f'[{player_request.alliance}]{player_request.player}',
            'remaining_time': remaining_time
        })
    return jsonify({'status': 'failure'})

@role_routes.route('/release_role/<role>')
def release_role(role):
    role_manager.release_role(role)
    db.session.commit()
    return jsonify({'status': 'success'})
