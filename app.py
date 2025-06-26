from flask import Flask, request, jsonify
import base64
import numpy as np
import face_recognition
import cv2
from datetime import datetime
from db_config import get_connection

app = Flask(__name__)

# To create base64 string to face encoding for future comparisons
def get_face_encoding(base64_str):
    try:
        image_data = base64.b64decode(base64_str)
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        face_encodings = face_recognition.face_encodings(img)
        return face_encodings[0] if face_encodings else None
    except Exception as e:
        print("Error decoding image:", e)
        return None

#To match with the saved encodings in our db
def get_existing_encodings(cursor):
    cursor.execute("SELECT name, face_encoding FROM entry")
    rows = cursor.fetchall()
    existing = []
    for name, encoding_blob in rows:
        encoding = np.frombuffer(encoding_blob, dtype=np.float64)
        existing.append((name, encoding))
    return existing

# API endpoint
@app.route('/submit-face', methods=['POST'])
def submit_face():
    data = request.json

    name = data.get('name')
    gender = data.get('gender')
    age = data.get('age')
    image_base64 = data.get('image')

    if not all([name, gender, age, image_base64]):
        return jsonify({'error': 'Missing required fields'}), 400

    encoding = get_face_encoding(image_base64)
    if encoding is None:
        return jsonify({'error': 'No face detected'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get existing face encodings
        existing_data = get_existing_encodings(cursor)

        for existing_name, stored_encoding in existing_data:
            match = face_recognition.compare_faces([stored_encoding], encoding, tolerance=0.6)
            if match[0]:
                # Log duplicate entry when same image is identified
                cursor.execute(
                    "INSERT INTO logs (event_type, name, timestamp) VALUES (%s, %s, %s)",
                    ('duplicate entry', existing_name, datetime.now())
                )
                conn.commit()
                return jsonify({'message': 'Duplicate entry found', 'name': existing_name}), 200

        # Insert new entry when new face is recognized
        cursor.execute(
            "INSERT INTO entry (name, gender, age, image_base64, face_encoding) VALUES (%s, %s, %s, %s, %s)",
            (name, gender, age, image_base64, encoding.tobytes())
        )
        conn.commit()
        return jsonify({'message': 'New entry added'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
