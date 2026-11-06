from backend.database.connection import get_db_connection
from backend.ai.question_generator import generate_questions
from backend.services.skill_service import get_resume_skills


def create_interview(user_id, domain, difficulty):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        resume_query = """
            SELECT id
            FROM resumes
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
            LIMIT 1
        """

        cursor.execute(resume_query, (user_id,))
        resume = cursor.fetchone()

        if not resume:
            return False, "Please upload a resume before starting an interview.", None

        success, message, skills = get_resume_skills(user_id)

        if not success:
            return False, message, None

        questions = generate_questions(
            skills,
            domain,
            difficulty,
            5
        )

        if not questions:
            return False, "No questions were generated.", None

        interview_query = """
            INSERT INTO interviews
            (user_id, resume_id, domain, difficulty, status)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            interview_query,
            (
                user_id,
                resume["id"],
                domain,
                difficulty,
                "in_progress"
            )
        )

        interview_id = cursor.lastrowid

        question_query = """
            INSERT INTO questions
            (interview_id, question_text, question_type, question_order)
            VALUES (%s, %s, %s, %s)
        """

        question_ids = []

        for index, question in enumerate(questions, start=1):
            cursor.execute(
                question_query,
                (
                    interview_id,
                    question,
                    "technical",
                    index
                )
            )

            question_ids.append(cursor.lastrowid)

        connection.commit()

        return True, "Interview created successfully.", {
            "interview_id": interview_id,
            "domain": domain,
            "difficulty": difficulty,
            "question_ids": question_ids,
            "questions": questions
        }

    except Exception as error:
        connection.rollback()
        return False, str(error), None

    finally:
        cursor.close()
        connection.close()