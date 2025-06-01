import os
import face_recognition
import pickle

KNOWN_FACES_DIR = "known_faces"
ENCODING_FILE = "faces.pkl"

known_encodings = []
known_names = []

# Ensure the known_faces directory exists
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# Capture a new face image
def save_new_face(image_path, name):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if encodings:
        known_encodings.append(encodings[0])
        known_names.append(name)

        # Save the new face to the known_faces directory
        new_face_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
        face_recognition.save_image_file(new_face_path, image)

        # Save updated encodings and names to the pickle file
        with open(ENCODING_FILE, "wb") as f:
            pickle.dump((known_encodings, known_names), f)

        print(f"[INFO] Saved new face for {name}.")
    else:
        print("[ERROR] No face found in the image.")

# Example usage
# save_new_face("path_to_image.jpg", "John_Doe")