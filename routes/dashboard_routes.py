from flask import Blueprint, render_template, jsonify
from models import db, RoleRequest
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_routes = Blueprint('dashboard', __name__)

@dashboard_routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@dashboard_routes.route('/daily_stats')
def daily_stats():
    return render_template('daily_stats.html')

@dashboard_routes.route('/api/daily_stats', methods=['GET'])
def get_daily_stats():
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    num_requests = db.session.query(func.count(RoleRequest.id)).filter(
        RoleRequest.request_time >= today,
        RoleRequest.request_time < tomorrow
    ).scalar()

    top_players = db.session.query(
        RoleRequest.player, func.count(RoleRequest.id).label('request_count')
    ).filter(
        RoleRequest.request_time >= today,
        RoleRequest.request_time < tomorrow
    ).group_by(RoleRequest.player).order_by(func.count(RoleRequest.id).desc()).limit(10).all()

    top_alliances = db.session.query(
        RoleRequest.alliance, func.count(RoleRequest.id).label('request_count')
    ).filter(
        RoleRequest.request_time >= today,
        RoleRequest.request_time < tomorrow
    ).group_by(RoleRequest.alliance).order_by(func.count(RoleRequest.id).desc()).limit(5).all()

    avg_wait_time = db.session.query(
        func.avg(func.julianday(RoleRequest.assign_time) - func.julianday(RoleRequest.request_time))
    ).filter(
        RoleRequest.request_time >= today,
        RoleRequest.request_time < tomorrow,
        RoleRequest.assign_time != None
    ).scalar()

    avg_wait_time = avg_wait_time * 24 * 60 if avg_wait_time else 0  # Convert days to minutes

    stats = {
        'num_requests': num_requests,
        'top_players': [{'player': player, 'count': count} for player, count in top_players],
        'top_alliances': [{'alliance': alliance, 'count': count} for alliance, count in top_alliances],
        'avg_wait_time': avg_wait_time
    }

    return jsonify(stats)
