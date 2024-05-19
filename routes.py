from flask import render_template, request, jsonify
from models import db, RoleRequest
from role_manager import role_manager
from datetime import datetime
import sqlalchemy as sa
import logging
from role_manager import RoleManager

# Configura il logging
logging.basicConfig(level=logging.DEBUG)

role_manager = RoleManager()

def init_routes(app):
    @app.route('/')
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

    @app.route('/request_role', methods=['POST'])
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

    @app.route('/assign_role/<role>')
    def assign_role(role):
        player_request = role_manager.assign_role(role)
        if player_request:
            player_request.status = 'assigned'
            player_request.assign_time = datetime.utcnow()
            db.session.commit()
            remaining_time = role_manager.get_remaining_time(role)
            return jsonify({'status': 'success', 'player': f'[{player_request.alliance}]{player_request.player}', 'remaining_time': remaining_time})
        return jsonify({'status': 'failure'})

    @app.route('/release_role/<role>')
    def release_role(role):
        role_manager.release_role(role)
        return jsonify({'status': 'success'})

    @app.route('/get_initial_state')
    def get_initial_state():
        roles_with_requests = role_manager.get_roles_with_requests()
        current_assignments = role_manager.current_assignments
        start_times = role_manager.start_times
        remaining_times = {
            role: role_manager.get_remaining_time(role) if role_manager.is_role_assigned(role) else ''
            for role in role_manager.roles.keys()
        }
        return jsonify({'roles': roles_with_requests, 'assignments': current_assignments, 'start_times': remaining_times})

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/api/dashboard/most_requested_role', methods=['GET'])
    def most_requested_role():
        results = db.session.query(
            RoleRequest.role,
            sa.func.count(RoleRequest.id).label('count')
        ).group_by(RoleRequest.role).order_by(sa.desc('count')).all()

        logging.debug(f"Most requested roles: {results}")

        result_list = [{'role': result.role, 'count': result.count} for result in results]

        return jsonify(result_list)

    @app.route('/api/dashboard/top_requester', methods=['GET'])
    def top_requester():
        results = db.session.query(
            RoleRequest.player,
            sa.func.count(RoleRequest.id).label('count')
        ).group_by(RoleRequest.player).order_by(sa.desc('count')).limit(10).all()

        logging.debug(f"Top requesters: {results}")

        result_list = [{'player': result.player, 'count': result.count} for result in results]

        return jsonify(result_list)

    @app.route('/api/dashboard/role_distribution', methods=['GET'])
    def role_distribution():
        results = db.session.query(
            RoleRequest.role,
            sa.func.count(RoleRequest.id).label('count')
        ).group_by(RoleRequest.role).all()

        logging.debug(f"Role distribution: {results}")

        result_list = [{'role': result.role, 'count': result.count} for result in results]

        return jsonify(result_list)

    @app.route('/api/dashboard/requests_per_day', methods=['GET'])
    def requests_per_day():
        results = db.session.query(
            sa.func.strftime('%Y-%m-%d', RoleRequest.request_time).label('day'),
            sa.func.count(RoleRequest.id).label('count')
        ).group_by(
            sa.func.strftime('%Y-%m-%d', RoleRequest.request_time)
        ).all()

        logging.debug(f"Requests per day: {results}")

        result_list = [{'day': datetime.strptime(result.day, '%Y-%m-%d').isoformat(), 'count': result.count} for result in results]

        return jsonify(result_list)
    
    @app.route('/api/dashboard/alliance_distribution', methods=['GET'])
    def alliance_distribution():
        results = db.session.query(
            RoleRequest.alliance,
            sa.func.count(RoleRequest.id).label('count')
        ).group_by(RoleRequest.alliance).all()

        logging.debug(f"Alliance distribution: {results}")

        result_list = [{'alliance': result.alliance, 'count': result.count} for result in results]

        return jsonify(result_list)
