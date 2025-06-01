import os
import face_recognition
import pickle

KNOWN_FACES_DIR = "known_faces"
ENCODING_FILE = "faces.pkl"

known_encodings = []
known_names = []

# Loop through all images in known_faces/
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(filename)[0])

# Save to pickle file
with open(ENCODING_FILE, "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print(f"[INFO] Encoded {len(known_names)} faces.")