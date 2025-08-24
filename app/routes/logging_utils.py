import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "localhost")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def log_interaction(prompt: str, answer: str, success: bool = True, error_message: str = None):
    connection = mysql.connector.connect(
        host=DATABASE_URL,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )

    try:
        if connection.is_connected():
            cursor = connection.cursor()
            sql = """
                INSERT INTO logs (user_prompt, jarvis_response, success, error_message)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (prompt, answer, success, error_message))
            connection.commit()

    except Error as e:
        print(f"MySQL Error: {e}")

    finally:
        if connection and connection.is_connected():
            if cursor:
                cursor.close()
            connection.close()