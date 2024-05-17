from flask import Flask, request, render_template, redirect, url_for, jsonify
from collections import deque
from datetime import datetime, timedelta

app = Flask(__name__)

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

    def request_role(self, player, role, coordinates=None):
        if role in self.roles:
            self.roles[role].append((player, coordinates))
            print(f'{player} requested the role of {role} with coordinates {coordinates}')

    def assign_role(self, role):
        if self.roles[role]:
            next_player, coordinates = self.roles[role].popleft()
            self.current_assignments[role] = next_player
            self.assignment_start_times[role] = datetime.now()
            print(f'{next_player} has been assigned the role of {role}')
            return next_player
        return None

    def release_role(self, role):
        player = self.current_assignments[role]
        self.current_assignments[role] = None
        self.assignment_start_times[role] = None
        print(f'{player} has finished the role of {role}')
        return player

role_manager = RoleManager()

@app.route('/')
def index():
    return render_template('index.html', roles=role_manager.roles, assignments=role_manager.current_assignments, start_times=role_manager.assignment_start_times)

@app.route('/request_role', methods=['POST'])
def request_role():
    player = request.form['player']
    role = request.form['role']
    coordinates = request.form.get('coordinates', None)
    role_manager.request_role(player, role, coordinates)
    return redirect(url_for('index'))

@app.route('/assign_role/<role>')
def assign_role(role):
    player = role_manager.assign_role(role)
    return jsonify({'status': 'success', 'player': player})

@app.route('/release_role/<role>')
def release_role(role):
    player = role_manager.release_role(role)
    return jsonify({'status': 'success', 'player': player})

if __name__ == '__main__':
    app.run(debug=True)
