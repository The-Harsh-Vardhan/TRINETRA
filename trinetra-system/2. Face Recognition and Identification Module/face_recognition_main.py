import cv2
import numpy as np
from deepface import DeepFace
import pickle
import os
from datetime import datetime

class FaceRecognitionSystem:
    def __init__(self, database_path='faces.pkl'):
        self.database_path = database_path
        self.known_faces = self.load_database()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def load_database(self):
        if os.path.exists(self.database_path):
            with open(self.database_path, 'rb') as f:
                return pickle.load(f)
        return {}

    def save_database(self):
        with open(self.database_path, 'wb') as f:
            pickle.dump(self.known_faces, f)

    def add_face(self, face_image, customer_id, metadata=None):
        try:
            embedding = DeepFace.represent(face_image, model_name="Facenet")[0]["embedding"]
            self.known_faces[customer_id] = {
                'embedding': embedding,
                'metadata': metadata or {},
                'last_seen': datetime.now(),
                'visit_count': 1
            }
            self.save_database()
            return True
        except Exception as e:
            print(f"Error adding face: {e}")
            return False

    def recognize_face(self, face_image, threshold=0.6):
        try:
            current_embedding = DeepFace.represent(face_image, model_name="Facenet")[0]["embedding"]
            
            best_match = None
            min_distance = float('inf')
            
            for customer_id, data in self.known_faces.items():
                distance = np.linalg.norm(np.array(current_embedding) - np.array(data['embedding']))
                if distance < threshold and distance < min_distance:
                    min_distance = distance
                    best_match = customer_id
            
            if best_match:
                # Update customer data
                self.known_faces[best_match]['last_seen'] = datetime.now()
                self.known_faces[best_match]['visit_count'] += 1
                self.save_database()
                return best_match, self.known_faces[best_match]
            
            return None, None

        except Exception as e:
            print(f"Error in face recognition: {e}")
            return None, None

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            customer_id, customer_data = self.recognize_face(face_img)
            
            # Draw rectangle around face
            color = (0, 255, 0) if customer_id else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Display customer info if recognized
            if customer_id:
                label = f"ID: {customer_id}"
                visits = f"Visits: {customer_data['visit_count']}"
                cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.putText(frame, visits, (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame

    def run(self, source=0):
        cap = cv2.VideoCapture(source)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frame = self.process_frame(frame)
            cv2.imshow('Face Recognition', processed_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('a'):
                # Add new face when 'a' is pressed
                customer_id = f"CUST_{len(self.known_faces)}"
                if self.add_face(frame, customer_id):
                    print(f"Added new customer with ID: {customer_id}")
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_system = FaceRecognitionSystem()
    face_system.run()