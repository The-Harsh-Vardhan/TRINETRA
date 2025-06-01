import cv2
import numpy as np
from deepface import DeepFace
import datetime
from collections import defaultdict
import json

class EmotionDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.emotions_data = defaultdict(list)
        
    def detect_emotion(self, face_image):
        """Detect emotion in face image using DeepFace"""
        try:
            result = DeepFace.analyze(
                face_image, 
                actions=['emotion'],
                enforce_detection=False
            )
            return result[0]['emotion']
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return None

    def track_customer_emotion(self, customer_id, emotion_data, timestamp=None):
        """Track customer's emotional state over time"""
        if timestamp is None:
            timestamp = datetime.datetime.now()
            
        self.emotions_data[customer_id].append({
            'timestamp': timestamp,
            'emotions': emotion_data
        })

    def get_customer_emotions(self, customer_id):
        """Get emotional history for a customer"""
        return self.emotions_data.get(customer_id, [])

    def analyze_emotional_trends(self, customer_id):
        """Analyze emotional trends for a customer"""
        emotions = self.get_customer_emotions(customer_id)
        if not emotions:
            return None
            
        # Aggregate emotions
        emotion_counts = defaultdict(int)
        total_readings = len(emotions)
        
        for reading in emotions:
            for emotion, score in reading['emotions'].items():
                emotion_counts[emotion] += score / total_readings
                
        # Get dominant emotion
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])
        
        # Calculate emotional stability
        emotion_variance = np.var([list(e['emotions'].values()) for e in emotions])
        
        return {
            'dominant_emotion': dominant_emotion[0],
            'emotion_distribution': dict(emotion_counts),
            'emotional_stability': 1 - min(emotion_variance, 1)  # 0 to 1 scale
        }

    def save_emotions_data(self, filename='emotions_data.json'):
        """Save emotions data to file"""
        data_to_save = {}
        for customer_id, emotions in self.emotions_data.items():
            data_to_save[customer_id] = [
                {
                    'timestamp': e['timestamp'].isoformat(),
                    'emotions': e['emotions']
                }
                for e in emotions
            ]
            
        with open(filename, 'w') as f:
            json.dump(data_to_save, f)

    def load_emotions_data(self, filename='emotions_data.json'):
        """Load emotions data from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            for customer_id, emotions in data.items():
                self.emotions_data[customer_id] = [
                    {
                        'timestamp': datetime.datetime.fromisoformat(e['timestamp']),
                        'emotions': e['emotions']
                    }
                    for e in emotions
                ]
                
        except FileNotFoundError:
            print(f"No existing data file found at {filename}")

    def process_frame(self, frame, customer_tracking_info=None):
        """
        Process a frame and detect emotions
        customer_tracking_info: dict mapping face locations to customer IDs
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        frame_emotions = {}
        
        for i, (x, y, w, h) in enumerate(faces):
            face_img = frame[y:y+h, x:x+w]
            emotions = self.detect_emotion(face_img)
            
            if emotions:
                # Get customer ID if tracking info is provided
                customer_id = None
                if customer_tracking_info:
                    # Find closest tracked face
                    face_center = (x + w/2, y + h/2)
                    min_dist = float('inf')
                    for tracked_face, tracked_id in customer_tracking_info.items():
                        tx, ty, tw, th = tracked_face
                        tracked_center = (tx + tw/2, ty + th/2)
                        dist = np.sqrt((face_center[0] - tracked_center[0])**2 +
                                     (face_center[1] - tracked_center[1])**2)
                        if dist < min_dist:
                            min_dist = dist
                            customer_id = tracked_id
                
                if not customer_id:
                    customer_id = f"UNKNOWN_{i}"
                
                # Track emotions
                self.track_customer_emotion(customer_id, emotions)
                frame_emotions[customer_id] = emotions
                
                # Draw rectangle and emotions
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Get dominant emotion
                dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
                cv2.putText(frame, f"{customer_id}: {dominant_emotion}",
                           (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
        return frame, frame_emotions

    def run(self, source=0):
        """Run emotion detection system"""
        cap = cv2.VideoCapture(source)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frame, emotions = self.process_frame(frame)
            
            # Display frame
            cv2.imshow('Emotion Detection', processed_frame)
            
            # Print emotions
            for customer_id, emotion_data in emotions.items():
                print(f"\nCustomer: {customer_id}")
                for emotion, score in emotion_data.items():
                    print(f"{emotion}: {score:.2f}")
                print("-" * 50)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        # Save data before exit
        self.save_emotions_data()

if __name__ == "__main__":
    detector = EmotionDetector()
    # Load previous data if exists
    detector.load_emotions_data()
    # Run detection system
    detector.run()