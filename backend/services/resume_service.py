from backend.database.connection import get_db_connection
from backend.services.resume_parser import extract_resume_text


def save_resume(user_id, file_name, file_path):

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        extracted_text = extract_resume_text(file_path)

        query = """
            INSERT INTO resumes (
                user_id,
                file_name,
                file_path,
                extracted_text
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                user_id,
                file_name,
                file_path,
                extracted_text
            )
        )

        connection.commit()

        return True, "Resume uploaded and processed successfully."

    except Exception as error:

        connection.rollback()

        return False, str(error)

    finally:

        cursor.close()
        connection.close()