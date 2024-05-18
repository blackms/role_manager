from flask import render_template, redirect, url_for, jsonify, request, session
from datetime import datetime, timedelta
from models import db, RoleRequest
from collections import deque
import re

class RoleManager:
    def __init__(self):
        self.roles = {
            'secretary of strategy': deque(),
            'secretary of security': deque(),
            'secretary of development': deque(),
            'secretary of science': deque(),
            'secretary of interior': deque()
        }
        self.current_assignments = {
            'secretary of strategy': None,
            'secretary of security': None,
            'secretary of development': None,
            'secretary of science': None,
            'secretary of interior': None
        }
        self.assignment_start_times = {
            'secretary of strategy': None,
            'secretary of security': None,
            'secretary of development': None,
            'secretary of science': None,
            'secretary of interior': None
        }

    def normalize_player_name(self, player):
        # Remove special characters and convert to lowercase
        player = re.sub(r'[^a-zA-Z0-9\[\]]', '', player).lower()
        return player

    def request_role(self, player, role, coordinates=None):
        if role in self.roles:
            player = self.normalize_player_name(player)
            alliance, player_name = self.parse_player_name(player)
            new_request = RoleRequest(alliance=alliance, player=player_name, role=role, coordinates=coordinates, request_time=datetime.utcnow())
            db.session.add(new_request)
            db.session.commit()
            self.roles[role].append(new_request.id)
            print(f'{player} requested the role of {role} with coordinates {coordinates}')

    def assign_role(self, role):
        if self.roles[role]:
            next_request_id = self.roles[role].popleft()
            next_request = RoleRequest.query.get(next_request_id)
            next_request.assign_time = datetime.utcnow()
            db.session.commit()
            self.current_assignments[role] = next_request
            self.assignment_start_times[role] = next_request.assign_time
            print(f'{next_request.player} has been assigned the role of {role} at {next_request.assign_time}')
            return next_request
        return None

    def release_role(self, role):
        player_request = self.current_assignments[role]
        self.current_assignments[role] = None
        self.assignment_start_times[role] = None
        print(f'{player_request.player} has finished the role of {role}')
        return player_request

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
        return jsonify({'status': 'success', 'player': f'[{player_request.alliance}]{player_request.player}', 'assign_time': player_request.assign_time.isoformat()})

    @app.route('/release_role/<role>')
    def release_role(role):
        player_request = role_manager.release_role(role)
        return jsonify({'status': 'success', 'player': f'[{player_request.alliance}]{player_request.player}'})
