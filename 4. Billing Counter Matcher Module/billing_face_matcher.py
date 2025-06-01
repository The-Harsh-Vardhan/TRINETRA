import cv2
import face_recognition
import pickle
from datetime import datetime

# Simulate previously tracked customers (in real system, import from tracker)
with open("faces.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

# Simulate billing system (later link to real POS)
def simulate_order_data(name):
    return {
        "items": ["Coffee", "Pastry"],
        "total_value": 260,
        "staff": "Ritika",
        "billing_time": str(datetime.now())
    }

cap = cv2.VideoCapture(0)  # Replace with billing counter feed

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
            billing_info = simulate_order_data(name)

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} - ₹{billing_info['total_value']}",
                        (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            print(f"[MATCH] {name} billed ₹{billing_info['total_value']} by {billing_info['staff']}")
            # Optionally save to DB here

        else:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, "Unknown Customer", (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("TRINETRA - Billing Matcher", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()