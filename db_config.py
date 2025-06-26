import mysql.connector

def get_connection():
    """Establishes a connection with MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="pass",  # Enter your password
            database="face_recognition_db",
            charset="utf8mb4"  
        )
        #print("Checking if TABLE is being executed...")
        return conn
    except mysql.connector.Error as e:
        print(f"[Error] Database Connection Failed: {e}")
        return None
