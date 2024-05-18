from flask import render_template, redirect, url_for, jsonify, request, session
from datetime import datetime, timedelta
from models import db, RoleRequest
from collections import deque
import re

class RoleManager:
    def __init__(self):
        self.roles = {
            'secretary_of_strategy': deque(),
            'secretary_of_security': deque(),
            'secretary_of_development': deque(),
            'secretary_of_science': deque(),
            'secretary_of_interior': deque()
        }
        self.current_assignments = {
            'secretary_of_strategy': None,
            'secretary_of_security': None,
            'secretary_of_development': None,
            'secretary_of_science': None,
            'secretary_of_interior': None
        }
        self.assignment_start_times = {
            'secretary_of_strategy': None,
            'secretary_of_security': None,
            'secretary_of_development': None,
            'secretary_of_science': None,
            'secretary_of_interior': None
        }

    def normalize_player_name(self, player):
        # Remove special characters and convert to lowercase
        player = re.sub(r'[^a-zA-Z0-9\[\]]', '', player).lower()
        return player

    def request_role(self, player, role, coordinates=None):
        role_key = role.replace(' ', '_')
        if role_key in self.roles:
            player = self.normalize_player_name(player)
            alliance, player_name = self.parse_player_name(player)
            new_request = RoleRequest(alliance=alliance, player=player_name, role=role, coordinates=coordinates, request_time=datetime.utcnow())
            db.session.add(new_request)
            db.session.commit()
            self.roles[role_key].append(new_request.id)
            print(f'{player} requested the role of {role} with coordinates {coordinates}')

    def assign_role(self, role):
        role_key = role.replace(' ', '_')
        if self.roles[role_key]:
            next_request_id = self.roles[role_key].popleft()
            next_request = RoleRequest.query.get(next_request_id)
            next_request.assign_time = datetime.utcnow()
            db.session.commit()
            self.current_assignments[role_key] = next_request
            self.assignment_start_times[role_key] = next_request.assign_time
            print(f'{next_request.player} has been assigned the role of {role} at {next_request.assign_time}')
            return next_request
        return None

    def release_role(self, role):
        role_key = role.replace(' ', '_')
        player_request = self.current_assignments[role_key]
        self.current_assignments[role_key] = None
        self.assignment_start_times[role_key] = None
        print(f'{player_request.player} has finished the role of {role}')
        return player_request

    def get_remaining_time(self, role):
        role_key = role.replace(' ', '_')
        if role_key in self.assignment_start_times and self.assignment_start_times[role_key]:
            elapsed = datetime.utcnow() - self.assignment_start_times[role_key]
            remaining = timedelta(minutes=5) - elapsed
            if remaining.total_seconds() > 0:
                return int(remaining.total_seconds())
            else:
                self.release_role(role)
        return 0

    def parse_player_name(self, player):
        if player.startswith('[') and ']' in player:
            alliance, player_name = player[1:].split(']', 1)
        else:
            alliance, player_name = None, player
        return alliance, player_name

role_manager = RoleManager()

def init_routes(app):
    @app.route('/')
    def index():
        if 'username' not in session:
            session['username'] = f'user_{datetime.now().timestamp()}'
        
        roles_with_requests = {role: [RoleRequest.query.get(req_id) for req_id in queue] for role, queue in role_manager.roles.items()}
        start_times = {role: (time.isoformat() if time else None) for role, time in role_manager.assignment_start_times.items()}
        return render_template('index.html', roles=roles_with_requests, assignments=role_manager.current_assignments, start_times=start_times)

    @app.route('/request_role', methods=['POST'])
    def request_role():
        player = request.form['player']
        role = request.form['role']
        coordinates = request.form.get('coordinates', None)
        role_manager.request_role(player, role, coordinates)
        return redirect(url_for('index'))

    @app.route('/assign_role/<role>')
    def assign_role(role):
        player_request = role_manager.assign_role(role)
        if player_request:
            remaining_time = role_manager.get_remaining_time(role)
            return jsonify({
                'status': 'success', 
                'player': f'[{player_request.alliance}]{player_request.player}', 
                'remaining_time': remaining_time,
                'role': role.replace('_', ' ')
            })
        return jsonify({'status': 'failure', 'message': 'No player in queue'})

    @app.route('/release_role/<role>')
    def release_role(role):
        player_request = role_manager.release_role(role)
        return jsonify({'status': 'success', 'player': f'[{player_request.alliance}]{player_request.player}'})

    @app.route('/get_remaining_time/<role>')
    def get_remaining_time(role):
        remaining_time = role_manager.get_remaining_time(role)
        return jsonify({'remaining_time': remaining_time})
