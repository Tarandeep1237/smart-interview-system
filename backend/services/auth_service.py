from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.connection import get_db_connection


def register_user(name, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        check_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(check_query, (email,))

        if cursor.fetchone():
            return False, "Email already registered."

        password_hash = generate_password_hash(password)

        insert_query = """
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (name, email, password_hash)
        )

        connection.commit()

        return True, "Registration successful."

    except Exception as error:
        connection.rollback()
        return False, str(error)

    finally:
        cursor.close()
        connection.close()


def login_user(email, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT id, name, email, password_hash, role
            FROM users
            WHERE email = %s
        """

        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if not user:
            return False, "Invalid email or password.", None

        if not check_password_hash(user["password_hash"], password):
            return False, "Invalid email or password.", None

        return True, "Login successful.", {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }

    except Exception as error:
        return False, str(error), None

    finally:
        cursor.close()
        connection.close()