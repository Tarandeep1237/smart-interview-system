from flask import Blueprint, jsonify, render_template, session

from backend.services.dashboard_service import get_dashboard_data


dashboard_routes = Blueprint("dashboard_routes", __name__)


@dashboard_routes.route("/dashboard")
def dashboard_page():

    if "user_id" not in session:
        return render_template("login.html")

    return render_template("dashboard.html")


@dashboard_routes.route("/api/dashboard")
def get_dashboard():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    success, message, data = get_dashboard_data(
        session["user_id"]
    )


    if not success:
        return jsonify({
            "success": False,
            "message": message
        }), 404


    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), 200