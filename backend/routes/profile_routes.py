from flask import Blueprint, request, jsonify, session
from backend.services.profile_service import (
    create_or_update_profile,
    get_profile
)


profile_routes = Blueprint("profile_routes", __name__)


@profile_routes.route("/api/profile", methods=["POST"])
def save_profile():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required."
        }), 400

    phone = data.get("phone")
    education = data.get("education")
    target_role = data.get("target_role")

    if not phone or not education or not target_role:
        return jsonify({
            "success": False,
            "message": "Phone, education and target role are required."
        }), 400

    success, message = create_or_update_profile(
        session["user_id"],
        phone,
        education,
        target_role
    )

    if success:
        return jsonify({
            "success": True,
            "message": message
        }), 200

    return jsonify({
        "success": False,
        "message": message
    }), 400


@profile_routes.route("/api/profile", methods=["GET"])
def profile():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    user_profile = get_profile(session["user_id"])

    if not user_profile:
        return jsonify({
            "success": False,
            "message": "Profile not found."
        }), 404

    return jsonify({
        "success": True,
        "profile": user_profile
    }), 200