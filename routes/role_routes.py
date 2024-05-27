import logging
from flask import Blueprint, jsonify, request
from models import db, RoleRequest
from role_manager import role_manager
from datetime import datetime, timedelta

role_routes = Blueprint('roles', __name__)

logger = logging.getLogger(__name__)


def get_remaining_time(role):
    role_request = RoleRequest.query.filter_by(
        role=role, status='assigned').first()
    if role_request:
        # 5 minutes for the role assignment
        assign_duration = timedelta(minutes=5)
        time_elapsed = datetime.utcnow() - role_request.assign_time
        remaining_time = assign_duration - time_elapsed
        if remaining_time.total_seconds() > 0:
            logger.info(f"Remaining time for role {role}: {
                        remaining_time.total_seconds() / 60} minutes")
            return remaining_time.total_seconds() / 60  # return in minutes
        else:
            role_request.status = 'finished'
            db.session.commit()
            logger.info(f"Role {role} time expired and marked as finished")
            return 0
    logger.warning(f"No assigned role found for {role}")
    return 0


@role_routes.route('/api/roles', methods=['GET'])
def get_roles():
    roles_with_requests = {}
    current_assignments = {}

    roles = RoleRequest.query.filter_by(status='waiting').all()
    assignments = RoleRequest.query.filter_by(status='assigned').all()

    print("Roles in waiting status:", roles)
    print("Roles in assigned status:", assignments)

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
            'remaining_time': get_remaining_time(assignment.role)
        }

    print("Roles with requests:", roles_with_requests)
    print("Current assignments:", current_assignments)

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
    alliance = alliance[1:].lower()  # convert to lowercase
    player = player.lower()  # convert to lowercase
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

    logger.info(f"Inserted new role request: {new_request}")

    return jsonify({'status': 'success'})


@role_routes.route('/api/assign_role/<role>', methods=['GET'])
def assign_role(role):
    logger.info(f"Attempting to assign role: {role}")
    player_request = RoleRequest.query.filter_by(
        role=role, status='waiting').first()
    if player_request:
        player_request.status = 'assigned'
        player_request.assign_time = datetime.utcnow()
        db.session.commit()

        remaining_time = get_remaining_time(role)
        logger.info(f"Assigned role: {player_request}")

        return jsonify({
            'status': 'success',
            'player': f'[{player_request.alliance}]{player_request.player}',
            'remaining_time': remaining_time
        })
    else:
        logger.warning(f"No waiting request found for role: {role}")
    return jsonify({'status': 'failure'})


@role_routes.route('/api/release_role/<role>', methods=['GET'])
def release_role(role):
    logger.info(f"Attempting to release role: {role}")
    role_request = RoleRequest.query.filter_by(role=role, status='assigned').first()
    if role_request:
        role_request.status = 'finished'
        db.session.commit()
        logger.info(f"Released role: {role_request}")
        return jsonify({'status': 'success'})
    else:
        logger.warning(f"No assigned role found to release: {role}")
    return jsonify({'status': 'failure'})
