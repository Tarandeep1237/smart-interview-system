from flask import Blueprint, request, jsonify, session, render_template

from backend.services.interview_service import create_interview
from backend.database.connection import get_db_connection
from backend.services.evaluation_service import evaluate_response
from backend.services.report_service import complete_interview


interview_routes = Blueprint("interview_routes", __name__)


@interview_routes.route("/interview/setup")
def interview_setup_page():
    if "user_id" not in session:
        return render_template("login.html")

    return render_template("interview_setup.html")


@interview_routes.route("/interview")
def interview_page():
    if "user_id" not in session:
        return render_template("login.html")

    return render_template("interview.html")


@interview_routes.route("/api/interview/start", methods=["POST"])
def start_interview():
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

    domain = data.get("domain")
    difficulty = data.get("difficulty")

    if not domain or not difficulty:
        return jsonify({
            "success": False,
            "message": "Domain and difficulty are required."
        }), 400

    allowed_difficulties = {"easy", "medium", "hard"}

    if difficulty not in allowed_difficulties:
        return jsonify({
            "success": False,
            "message": "Invalid difficulty."
        }), 400

    success, message, interview = create_interview(
        session["user_id"],
        domain,
        difficulty
    )

    if success:
        return jsonify({
            "success": True,
            "message": message,
            "interview": interview
        }), 201

    return jsonify({
        "success": False,
        "message": message
    }), 400


@interview_routes.route("/api/interview/answer", methods=["POST"])
def submit_answer():
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

    question_id = data.get("question_id")
    answer_text = data.get("answer")

    if not question_id or not answer_text:
        return jsonify({
            "success": False,
            "message": "Question ID and answer are required."
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        question_query = """
            SELECT
                questions.id,
                questions.interview_id
            FROM questions
            INNER JOIN interviews
                ON questions.interview_id = interviews.id
            WHERE questions.id = %s
              AND interviews.user_id = %s
        """

        cursor.execute(
            question_query,
            (question_id, session["user_id"])
        )

        question = cursor.fetchone()

        if not question:
            return jsonify({
                "success": False,
                "message": "Question not found."
            }), 404

        response_query = """
            INSERT INTO responses
            (question_id, answer_text)
            VALUES (%s, %s)
        """

        cursor.execute(
            response_query,
            (question_id, answer_text)
        )

        response_id = cursor.lastrowid

        connection.commit()

    except Exception as error:
        connection.rollback()

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:
        cursor.close()
        connection.close()

    success, message, evaluation = evaluate_response(response_id)

    if not success:
        return jsonify({
            "success": False,
            "message": message,
            "response_id": response_id
        }), 500

    return jsonify({
        "success": True,
        "message": "Answer submitted and evaluated successfully.",
        "response_id": response_id,
        "evaluation": evaluation
    }), 201


@interview_routes.route("/api/interview/complete", methods=["POST"])
def finish_interview():
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

    interview_id = data.get("interview_id")

    if not interview_id:
        return jsonify({
            "success": False,
            "message": "Interview ID is required."
        }), 400

    success, message, report = complete_interview(
        interview_id,
        session["user_id"]
    )

    if not success:
        return jsonify({
            "success": False,
            "message": message
        }), 400

    return jsonify({
        "success": True,
        "message": message,
        "report": report
    }), 200