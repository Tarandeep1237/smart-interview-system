from flask import Blueprint, jsonify, render_template, session

from backend.services.results_service import get_latest_interview_results


results_routes = Blueprint("results_routes", __name__)


@results_routes.route("/results")
def results_page():
    if "user_id" not in session:
        return render_template("login.html")

    return render_template("results.html")


@results_routes.route("/api/results")
def get_results():
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    success, message, data = get_latest_interview_results(
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