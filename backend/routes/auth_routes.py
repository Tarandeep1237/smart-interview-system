from flask import Blueprint, request, jsonify, session

from backend.services.auth_service import (
    register_user,
    login_user
)


auth_routes = Blueprint(
    "auth_routes",
    __name__
)


@auth_routes.route(
    "/api/register",
    methods=["POST"]
)
def register():

    data = request.get_json()


    if not data:

        return jsonify({
            "success": False,
            "message": "Request body is required."
        }), 400


    name = data.get("name")
    email = data.get("email")
    password = data.get("password")


    if not name or not email or not password:

        return jsonify({
            "success": False,
            "message": "Name, email and password are required."
        }), 400


    success, message = register_user(
        name,
        email,
        password
    )


    if not success:

        return jsonify({
            "success": False,
            "message": message
        }), 400


    # Automatically log in the newly registered user.
    login_success, login_message, user = login_user(
        email,
        password
    )


    if not login_success:

        return jsonify({
            "success": False,
            "message": (
                "Registration succeeded, "
                "but automatic login failed."
            )
        }), 500


    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]
    session["user_role"] = user["role"]


    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "user": user
    }), 201


@auth_routes.route(
    "/api/login",
    methods=["POST"]
)
def login():

    data = request.get_json()


    if not data:

        return jsonify({
            "success": False,
            "message": "Request body is required."
        }), 400


    email = data.get("email")
    password = data.get("password")


    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400


    success, message, user = login_user(
        email,
        password
    )


    if success:

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        session["user_role"] = user["role"]


        return jsonify({
            "success": True,
            "message": message,
            "user": user
        }), 200


    return jsonify({
        "success": False,
        "message": message
    }), 401