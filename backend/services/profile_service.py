from backend.database.connection import get_db_connection


def create_or_update_profile(user_id, phone, education, target_role):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        check_query = """
            SELECT id
            FROM profiles
            WHERE user_id = %s
        """

        cursor.execute(check_query, (user_id,))
        profile = cursor.fetchone()

        if profile:
            update_query = """
                UPDATE profiles
                SET phone = %s,
                    education = %s,
                    target_role = %s
                WHERE user_id = %s
            """

            cursor.execute(
                update_query,
                (phone, education, target_role, user_id)
            )

            connection.commit()

            return True, "Profile updated successfully."

        insert_query = """
            INSERT INTO profiles (
                user_id,
                phone,
                education,
                target_role
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (user_id, phone, education, target_role)
        )

        connection.commit()

        return True, "Profile created successfully."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()


def get_profile(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT id, user_id, phone, education, target_role, created_at
            FROM profiles
            WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))
        profile = cursor.fetchone()

        return profile

    except Exception:
        return None

    finally:
        cursor.close()
        connection.close()