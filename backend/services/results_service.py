from backend.database.connection import get_db_connection


def get_latest_interview_results(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        interview_query = """
            SELECT
                id,
                domain,
                difficulty,
                status,
                started_at,
                completed_at
            FROM interviews
            WHERE user_id = %s
            ORDER BY id DESC
            LIMIT 1
        """

        cursor.execute(
            interview_query,
            (user_id,)
        )

        interview = cursor.fetchone()

        if not interview:
            return False, "No interview history found.", None

        results_query = """
            SELECT
                questions.id AS question_id,
                questions.question_text,
                questions.question_order,

                responses.id AS response_id,
                responses.answer_text,

                evaluations.relevance_score,
                evaluations.correctness_score,
                evaluations.completeness_score,
                evaluations.technical_accuracy_score,
                evaluations.overall_score,
                evaluations.feedback,
                evaluations.strengths,
                evaluations.areas_for_improvement

            FROM questions

            LEFT JOIN responses
                ON questions.id = responses.question_id

            LEFT JOIN evaluations
                ON responses.id = evaluations.response_id

            WHERE questions.interview_id = %s

            ORDER BY questions.question_order ASC
        """

        cursor.execute(
            results_query,
            (interview["id"],)
        )

        results = cursor.fetchall()

        report_query = """
            SELECT
                id,
                interview_id,
                overall_score,
                strengths,
                areas_for_improvement,
                recommendations,
                generated_at
            FROM interview_reports
            WHERE interview_id = %s
            LIMIT 1
        """

        cursor.execute(
            report_query,
            (interview["id"],)
        )

        report = cursor.fetchone()

        return True, "Interview results retrieved successfully.", {
            "interview": interview,
            "results": results,
            "report": report
        }

    except Exception as error:
        return False, str(error), None

    finally:
        cursor.close()
        connection.close()