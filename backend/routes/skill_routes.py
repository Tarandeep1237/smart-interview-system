from flask import Blueprint, jsonify, session

from backend.services.skill_service import get_resume_skills


skill_routes = Blueprint("skill_routes", __name__)


@skill_routes.route("/api/skills", methods=["GET"])
def get_skills():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    success, message, skills = get_resume_skills(
        session["user_id"]
    )

    if success:
        return jsonify({
            "success": True,
            "message": message,
            "skills": skills
        }), 200

    return jsonify({
        "success": False,
        "message": message,
        "skills": []
    }), 404