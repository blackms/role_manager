from flask import Blueprint, jsonify, request
from models import db, RoleRequest
from role_manager import role_manager
from datetime import datetime

role_routes = Blueprint('roles', __name__)

@role_routes.route('/api/roles', methods=['GET'])
def get_roles():
    waiting_requests = db.session.query(RoleRequest).filter_by(status='waiting').all()
    current_assignments = db.session.query(RoleRequest).filter_by(status='assigned').all()

    roles_data = {
        'assignments': [
            {
                'role': assignment.role,
                'player': f"[{assignment.alliance}]{assignment.player}",
                'remaining_time': role_manager.get_remaining_time(assignment.role)  # Ensure this function exists
            }
            for assignment in current_assignments
        ],
        'roles': [
            {
                'role': role,
                'requests': [
                    {
                        'alliance': request.alliance,
                        'player': request.player,
                        'coordinates': request.coordinates
                    }
                    for request in waiting_requests if request.role == role
                ]
            }
            for role in set(req.role for req in waiting_requests)
        ]
    }
    return jsonify(roles_data)

@role_routes.route('/request_role', methods=['POST'])
def request_role():
    player_name = request.form['player']
    role = request.form['role']
    coordinates = request.form['coordinates']
    if not coordinates:
        coordinates = None

    alliance, player = player_name.split(']')
    alliance = alliance[1:]
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
    player_request = db.session.query(RoleRequest).filter_by(role=role, status='waiting').first()
    if player_request:
        player_request.status = 'assigned'
        player_request.assign_time = datetime.utcnow()
        db.session.commit()
        remaining_time = role_manager.get_remaining_time(role)
        return jsonify({'status': 'success', 'player': f'[{player_request.alliance}]{player_request.player}', 'remaining_time': remaining_time})
    return jsonify({'status': 'failure'})

@role_routes.route('/release_role/<role>')
def release_role(role):
    player_request = db.session.query(RoleRequest).filter_by(role=role, status='assigned').first()
    if player_request:
        player_request.status = 'waiting'
        player_request.assign_time = None
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failure'})
