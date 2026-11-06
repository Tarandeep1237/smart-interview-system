import os

from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename

from backend.services.resume_service import save_resume
from backend.services.skill_service import get_resume_skills
from backend.database.connection import get_db_connection


resume_routes = Blueprint(
    "resume_routes",
    __name__
)


UPLOAD_FOLDER = "uploads/resumes"


ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@resume_routes.route(
    "/api/resume/upload",
    methods=["POST"]
)
def upload_resume():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    if "resume" not in request.files:

        return jsonify({
            "success": False,
            "message": "Resume file is required."
        }), 400


    file = request.files["resume"]


    if file.filename == "":

        return jsonify({
            "success": False,
            "message": "No file selected."
        }), 400


    if not allowed_file(file.filename):

        return jsonify({
            "success": False,
            "message": "Only PDF and DOCX files are allowed."
        }), 400


    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


    filename = secure_filename(
        file.filename
    )


    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    file.save(file_path)


    success, message = save_resume(
        session["user_id"],
        filename,
        file_path
    )


    if success:

        return jsonify({
            "success": True,
            "message": message,
            "file_name": filename
        }), 201


    return jsonify({
        "success": False,
        "message": message
    }), 400


@resume_routes.route(
    "/api/resume",
    methods=["GET"]
)
def get_resume():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    try:

        query = """
            SELECT
                id,
                file_name,
                file_path,
                uploaded_at
            FROM resumes
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
            LIMIT 1
        """


        cursor.execute(
            query,
            (session["user_id"],)
        )


        resume = cursor.fetchone()


        if not resume:

            return jsonify({
                "success": False,
                "message": "No resume uploaded yet."
            }), 404


        success, message, skills = get_resume_skills(
            session["user_id"]
        )


        if not success:

            return jsonify({
                "success": False,
                "message": message
            }), 400


        return jsonify({
            "success": True,
            "resume": {
                "id": resume["id"],
                "file_name": resume["file_name"],
                "file_path": resume["file_path"],
                "uploaded_at": str(
                    resume["uploaded_at"]
                )
            },
            "skills": skills
        }), 200


    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


    finally:

        cursor.close()
        connection.close()