from backend.database.connection import get_db_connection
from backend.ai.skill_extractor import extract_skills


def get_resume_skills(user_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        query = """
            SELECT extracted_text
            FROM resumes
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
            LIMIT 1
        """

        cursor.execute(query, (user_id,))

        resume = cursor.fetchone()

        if not resume:
            return False, "No resume found.", []

        skills = extract_skills(
            resume["extracted_text"]
        )

        return True, "Skills extracted successfully.", skills

    except Exception as error:

        return False, str(error), []

    finally:

        cursor.close()
        connection.close()