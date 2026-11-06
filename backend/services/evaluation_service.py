from backend.database.connection import get_db_connection
from backend.ai.answer_evaluator import evaluate_answer


def evaluate_response(response_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT
                responses.id AS response_id,
                responses.answer_text,
                questions.question_text
            FROM responses
            INNER JOIN questions
                ON responses.question_id = questions.id
            WHERE responses.id = %s
        """

        cursor.execute(query, (response_id,))
        response = cursor.fetchone()

        if not response:
            return False, "Response not found.", None

        evaluation = evaluate_answer(
            question=response["question_text"],
            answer=response["answer_text"]
        )

        insert_query = """
            INSERT INTO evaluations
            (
                response_id,
                relevance_score,
                correctness_score,
                completeness_score,
                technical_accuracy_score,
                overall_score,
                feedback,
                strengths,
                areas_for_improvement
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (
                response_id,
                evaluation["relevance_score"],
                evaluation["correctness_score"],
                evaluation["completeness_score"],
                evaluation["technical_accuracy_score"],
                evaluation["overall_score"],
                evaluation["feedback"],
                evaluation["strengths"],
                evaluation["areas_for_improvement"]
            )
        )

        connection.commit()

        return True, "Answer evaluated successfully.", evaluation

    except Exception as error:
        connection.rollback()
        return False, str(error), None

    finally:
        cursor.close()
        connection.close()