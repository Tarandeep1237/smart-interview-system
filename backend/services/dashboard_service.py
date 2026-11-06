from backend.database.connection import get_db_connection


def get_dashboard_data(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        user_query = """
            SELECT
                id,
                name,
                email
            FROM users
            WHERE id = %s
        """

        cursor.execute(
            user_query,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return False, "User not found.", None


        profile_query = """
            SELECT
                phone,
                education,
                target_role
            FROM profiles
            WHERE user_id = %s
            LIMIT 1
        """

        cursor.execute(
            profile_query,
            (user_id,)
        )

        profile = cursor.fetchone()


        resume_query = """
            SELECT
                id,
                file_name,
                uploaded_at
            FROM resumes
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
            LIMIT 1
        """

        cursor.execute(
            resume_query,
            (user_id,)
        )

        resume = cursor.fetchone()


        interview_query = """
            SELECT
                interviews.id,
                interviews.domain,
                interviews.difficulty,
                interviews.status,
                interviews.started_at,
                interviews.completed_at,

                interview_reports.overall_score,
                interview_reports.strengths,
                interview_reports.areas_for_improvement,
                interview_reports.recommendations

            FROM interviews

            LEFT JOIN interview_reports
                ON interviews.id = interview_reports.interview_id

            WHERE interviews.user_id = %s

            ORDER BY interviews.id DESC

            LIMIT 1
        """

        cursor.execute(
            interview_query,
            (user_id,)
        )

        latest_interview = cursor.fetchone()


        return True, "Dashboard data retrieved successfully.", {
            "user": user,
            "profile": profile,
            "resume": resume,
            "latest_interview": latest_interview
        }


    except Exception as error:

        return False, str(error), None


    finally:

        cursor.close()
        connection.close()