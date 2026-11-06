from backend.database.connection import get_db_connection


def generate_recommendation(overall_score):
    if overall_score >= 80:
        return (
            "Excellent performance. Continue practicing advanced "
            "technical problems and focus on maintaining consistency "
            "across different interview topics."
        )

    if overall_score >= 60:
        return (
            "Good performance. Strengthen your weaker technical areas "
            "and practice more interview questions to improve accuracy "
            "and confidence."
        )

    if overall_score >= 40:
        return (
            "Average performance. Focus on improving conceptual "
            "understanding, completeness of answers, and technical "
            "accuracy through regular practice."
        )

    return (
        "More preparation is recommended. Strengthen your fundamental "
        "concepts, practice explaining technical topics clearly, and "
        "attempt more mock interviews."
    )


def complete_interview(interview_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        interview_query = """
            SELECT
                id,
                status
            FROM interviews
            WHERE id = %s
              AND user_id = %s
        """

        cursor.execute(
            interview_query,
            (interview_id, user_id)
        )

        interview = cursor.fetchone()

        if not interview:
            return False, "Interview not found.", None

        evaluation_query = """
            SELECT
                evaluations.overall_score,
                evaluations.strengths,
                evaluations.areas_for_improvement
            FROM questions

            INNER JOIN responses
                ON questions.id = responses.question_id

            INNER JOIN evaluations
                ON responses.id = evaluations.response_id

            WHERE questions.interview_id = %s

            ORDER BY questions.question_order ASC
        """

        cursor.execute(
            evaluation_query,
            (interview_id,)
        )

        evaluations = cursor.fetchall()

        if not evaluations:
            return False, "No evaluated answers found.", None

        overall_score = sum(
            float(item["overall_score"])
            for item in evaluations
        ) / len(evaluations)

        strengths = []

        for item in evaluations:
            if item["strengths"]:
                strengths.append(item["strengths"])

        areas_for_improvement = []

        for item in evaluations:
            if item["areas_for_improvement"]:
                areas_for_improvement.append(
                    item["areas_for_improvement"]
                )

        strengths_text = "\n".join(
            f"- {strength}"
            for strength in strengths
        )

        improvements_text = "\n".join(
            f"- {improvement}"
            for improvement in areas_for_improvement
        )

        recommendation = generate_recommendation(
            overall_score
        )

        report_query = """
            INSERT INTO interview_reports
            (
                interview_id,
                overall_score,
                strengths,
                areas_for_improvement,
                recommendations
            )
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                overall_score = VALUES(overall_score),
                strengths = VALUES(strengths),
                areas_for_improvement = VALUES(areas_for_improvement),
                recommendations = VALUES(recommendations)
        """

        cursor.execute(
            report_query,
            (
                interview_id,
                overall_score,
                strengths_text,
                improvements_text,
                recommendation
            )
        )

        update_interview_query = """
            UPDATE interviews
            SET
                status = %s,
                completed_at = NOW()
            WHERE id = %s
              AND user_id = %s
        """

        cursor.execute(
            update_interview_query,
            (
                "completed",
                interview_id,
                user_id
            )
        )

        connection.commit()

        return True, "Interview completed successfully.", {
            "interview_id": interview_id,
            "overall_score": round(overall_score, 2),
            "strengths": strengths_text,
            "areas_for_improvement": improvements_text,
            "recommendations": recommendation
        }

    except Exception as error:
        connection.rollback()

        return False, str(error), None

    finally:
        cursor.close()
        connection.close()