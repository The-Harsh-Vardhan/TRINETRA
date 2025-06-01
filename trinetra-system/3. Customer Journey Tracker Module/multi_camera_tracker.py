import os
import cv2
import face_recognition
import pickle
import numpy as np
from collections import defaultdict
import time
from ultralytics import YOLO
import supervision as sv
from deepface import DeepFace

# Load encoded face data
with open("../2. Face Recognition and Identification Module/faces.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

class MultiCameraTracker:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.tracker = sv.ByteTrack()
        self.camera_streams = {}  # Dictionary to store camera streams
        self.customer_tracks = defaultdict(list)  # Store customer trajectories
        self.face_embeddings = {}  # Store face embeddings for re-identification
        
    def add_camera(self, camera_id, source):
        """Add a new camera stream to the system"""
        self.camera_streams[camera_id] = {
            'source': source,
            'capture': cv2.VideoCapture(source),
            'active_tracks': {}
        }

    def get_face_embedding(self, frame, bbox):
        """Extract face embedding from detected person"""
        try:
            x1, y1, x2, y2 = map(int, bbox)
            face_img = frame[y1:y2, x1:x2]
            embedding = DeepFace.represent(face_img, model_name="Facenet")[0]["embedding"]
            return embedding
        except:
            return None

    def match_person_across_cameras(self, embedding1, embedding2, threshold=0.6):
        """Match person across different cameras using face embeddings"""
        if embedding1 is None or embedding2 is None:
            return False
        distance = np.linalg.norm(np.array(embedding1) - np.array(embedding2))
        return distance < threshold

    def update_customer_journey(self, camera_id, person_id, position, timestamp):
        """Update customer journey with new position"""
        self.customer_tracks[person_id].append({
            'camera_id': camera_id,
            'position': position,
            'timestamp': timestamp
        })

    def process_frame(self, camera_id, frame):
        """Process frame from a single camera"""
        # Detect people using YOLO
        results = self.model(frame)[0]
        detections = sv.Detections.from_yolov8(results)
        
        # Filter for person class (class_id = 0 in COCO dataset)
        mask = np.array([class_id == 0 for class_id in detections.class_id], dtype=bool)
        detections = detections[mask]

        # Track detections
        detections = self.tracker.update(detections=detections, frame=frame)

        # Process each detection
        for detection_id, bbox in zip(detections.tracker_id, detections.xyxy):
            if detection_id is not None:
                # Get face embedding for new tracks
                if detection_id not in self.face_embeddings:
                    embedding = self.get_face_embedding(frame, bbox)
                    if embedding is not None:
                        self.face_embeddings[detection_id] = embedding

                # Update position
                center = ((bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2)
                self.update_customer_journey(camera_id, detection_id, center, time.time())

                # Draw bounding box
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID: {detection_id}", (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def run(self):
        """Main loop to process all camera feeds"""
        while True:
            frames = {}
            
            # Read frames from all cameras
            for camera_id, camera_info in self.camera_streams.items():
                ret, frame = camera_info['capture'].read()
                if ret:
                    frames[camera_id] = frame
                else:
                    print(f"Failed to read from camera {camera_id}")
                    continue

            # Process each frame
            for camera_id, frame in frames.items():
                processed_frame = self.process_frame(camera_id, frame)
                cv2.imshow(f'Camera {camera_id}', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        for camera_info in self.camera_streams.values():
            camera_info['capture'].release()
        cv2.destroyAllWindows()

    def get_customer_journey(self, person_id):
        """Retrieve the complete journey of a specific customer"""
        return self.customer_tracks.get(person_id, [])

    def generate_heatmap(self, camera_id, frame_shape):
        """Generate heatmap of customer movements for a specific camera"""
        heatmap = np.zeros(frame_shape[:2], dtype=np.float32)
        
        for tracks in self.customer_tracks.values():
            for point in tracks:
                if point['camera_id'] == camera_id:
                    x, y = map(int, point['position'])
                    cv2.circle(heatmap, (x, y), 20, (1,), -1)

        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap = cv2.applyColorMap(heatmap.astype(np.uint8), cv2.COLORMAP_JET)
        return heatmap

if __name__ == "__main__":
    tracker = MultiCameraTracker()
    
    # Add camera streams (modify sources as needed)
    tracker.add_camera(0, 0)  # Webcam
    # tracker.add_camera(1, "rtsp://camera1_ip:port")  # IP camera
    # tracker.add_camera(2, "video_file.mp4")  # Video file
    
    tracker.run()