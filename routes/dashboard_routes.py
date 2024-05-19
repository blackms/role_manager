from flask import Blueprint, jsonify
from models import db, RoleRequest
import sqlalchemy as sa
import logging
from datetime import datetime

dashboard_routes = Blueprint('dashboard', __name__)

@dashboard_routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@dashboard_routes.route('/api/dashboard/most_requested_role', methods=['GET'])
def most_requested_role():
    results = db.session.query(
        RoleRequest.role,
        sa.func.count(RoleRequest.id).label('count')
    ).group_by(RoleRequest.role).order_by(sa.desc('count')).all()

    logging.debug(f"Most requested roles: {results}")

    result_list = [{'role': result.role, 'count': result.count} for result in results]

    return jsonify(result_list)

@dashboard_routes.route('/api/dashboard/top_requester', methods=['GET'])
def top_requester():
    results = db.session.query(
        RoleRequest.player,
        sa.func.count(RoleRequest.id).label('count')
    ).group_by(RoleRequest.player).order_by(sa.desc('count')).limit(10).all()

    logging.debug(f"Top requesters: {results}")

    result_list = [{'player': result.player, 'count': result.count} for result in results]

    return jsonify(result_list)

@dashboard_routes.route('/api/dashboard/role_distribution', methods=['GET'])
def role_distribution():
    results = db.session.query(
        RoleRequest.role,
        sa.func.count(RoleRequest.id).label('count')
    ).group_by(RoleRequest.role).all()

    logging.debug(f"Role distribution: {results}")

    result_list = [{'role': result.role, 'count': result.count} for result in results]

    return jsonify(result_list)

@dashboard_routes.route('/api/dashboard/requests_per_day', methods=['GET'])
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

@dashboard_routes.route('/api/dashboard/alliance_distribution', methods=['GET'])
def alliance_distribution():
    results = db.session.query(
        RoleRequest.alliance,
        sa.func.count(RoleRequest.id).label('count')
    ).group_by(RoleRequest.alliance).all()

    logging.debug(f"Alliance distribution: {results}")

    result_list = [{'alliance': result.alliance, 'count': result.count} for result in results]

    return jsonify(result_list)
