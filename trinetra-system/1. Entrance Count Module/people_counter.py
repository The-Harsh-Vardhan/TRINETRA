import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import supervision as sv
import json

class PeopleCounter:
    def __init__(self, video_source=None):
        # Initialize YOLO model
        self.model = YOLO('yolov8n.pt')
        self.tracker = sv.ByteTrack()
        self.entrance_line = None
        self.people_in = 0
        self.people_out = 0
        self.tracked_ids = defaultdict(lambda: {"last_y": None, "counted": False})
        
        # Video source handling
        self.video_source = video_source if video_source else self.get_default_video()
        self.cap = None
        self.should_loop = self.get_loop_config()

    def get_default_video(self):
        try:
            with open('camera_config.json', 'r') as f:
                config = json.load(f)
                for camera in config['cameras']:
                    if camera['type'] == 'entrance':
                        return camera['source']
                return config.get('default_fallback', 0)
        except Exception as e:
            print(f"Error loading camera config: {e}")
            return 0

    def get_loop_config(self):
        try:
            with open('camera_config.json', 'r') as f:
                config = json.load(f)
                return config.get('video_loop', True)
        except:
            return True

    def start_video(self):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video source: {self.video_source}")

    def read_frame(self):
        if self.cap is None:
            self.start_video()
        
        ret, frame = self.cap.read()
        if not ret and self.should_loop:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        
        return ret, frame if ret else None

    def set_entrance_line(self, frame):
        height, width = frame.shape[:2]
        # Set entrance line at 60% of frame height
        self.entrance_line = int(height * 0.6)

    def process_frame(self, frame):
        if self.entrance_line is None:
            self.set_entrance_line(frame)

        # Detect people using YOLO
        results = self.model(frame)[0]
        detections = sv.Detections.from_yolov8(results)
        
        # Filter for person class (class_id = 0 in COCO dataset)
        mask = np.array([class_id == 0 for class_id in detections.class_id], dtype=bool)
        detections = detections[mask]

        # Track detections
        detections = self.tracker.update(detections=detections, frame=frame)

        # Count people crossing the line
        for detection_id, bbox in zip(detections.tracker_id, detections.xyxy):
            if detection_id is not None:
                current_y = (bbox[1] + bbox[3]) / 2  # Center y-coordinate
                last_y = self.tracked_ids[detection_id]["last_y"]
                
                if last_y is not None and not self.tracked_ids[detection_id]["counted"]:
                    # Check if person crossed the line
                    if last_y < self.entrance_line and current_y >= self.entrance_line:
                        self.people_in += 1
                        self.tracked_ids[detection_id]["counted"] = True
                    elif last_y > self.entrance_line and current_y <= self.entrance_line:
                        self.people_out += 1
                        self.tracked_ids[detection_id]["counted"] = True

                self.tracked_ids[detection_id]["last_y"] = current_y

        # Draw entrance line
        cv2.line(frame, (0, self.entrance_line), (frame.shape[1], self.entrance_line), (0, 255, 0), 2)

        # Draw counts
        cv2.putText(frame, f"In: {self.people_in}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Out: {self.people_out}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Draw bounding boxes
        for bbox in detections.xyxy:
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        return frame

    def cleanup(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

    def run(self):
        try:
            self.start_video()
            
            while True:
                ret, frame = self.read_frame()
                if not ret:
                    break

                # Process frame and get detections
                processed_frame = self.process_frame(frame)
                
                # Draw entrance line
                cv2.line(processed_frame, (0, self.entrance_line), 
                        (processed_frame.shape[1], self.entrance_line), 
                        (0, 255, 0), 2)
                
                # Display counts
                count_text = f"In: {self.people_in} Out: {self.people_out}"
                cv2.putText(processed_frame, count_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Show frame
                cv2.imshow('People Counter', processed_frame)
                
                # Break on 'q' press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
        finally:
            self.cleanup()

if __name__ == "__main__":
    # Create instance with default video source from config
    counter = PeopleCounter()
    counter.run()