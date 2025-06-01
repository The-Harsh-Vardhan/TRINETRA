import cv2
import numpy as np
from paddleocr import PaddleOCR
import datetime
from collections import defaultdict
import json
import torch
from ultralytics import YOLO

class VehicleRecognition:
    def __init__(self):
        # Initialize YOLO model for vehicle detection
        self.vehicle_detector = YOLO('yolov8n.pt')
        
        # Initialize PaddleOCR for license plate recognition
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
        # Store vehicle data
        self.vehicle_data = defaultdict(list)
        
        # Vehicle classes from COCO dataset
        self.vehicle_classes = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}

    def detect_vehicles(self, frame):
        """Detect vehicles in frame using YOLOv8"""
        results = self.vehicle_detector(frame)[0]
        vehicles = []
        
        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            if int(cls) in self.vehicle_classes:
                vehicles.append({
                    'bbox': box.tolist(),
                    'type': self.vehicle_classes[int(cls)]
                })
                
        return vehicles

    def extract_license_plate(self, frame, vehicle_bbox):
        """Extract and recognize license plate from vehicle region"""
        x1, y1, x2, y2 = map(int, vehicle_bbox)
        vehicle_region = frame[y1:y2, x1:x2]
        
        # Use OCR to detect text in vehicle region
        result = self.ocr.ocr(vehicle_region, cls=True)
        
        # Filter and process potential license plates
        license_plate = None
        max_confidence = 0
        
        for line in result:
            text = line[1][0]
            confidence = line[1][1]
            
            # Basic license plate validation (customize based on your region's format)
            if len(text) >= 5 and any(c.isdigit() for c in text):
                if confidence > max_confidence:
                    license_plate = text
                    max_confidence = confidence
                    
        return license_plate, max_confidence

    def track_vehicle(self, license_plate, vehicle_type, timestamp):
        """Track vehicle entry/exit"""
        self.vehicle_data[license_plate].append({
            'timestamp': timestamp,
            'vehicle_type': vehicle_type
        })

    def get_vehicle_history(self, license_plate):
        """Get history of a specific vehicle"""
        return self.vehicle_data.get(license_plate, [])

    def save_vehicle_data(self, filename='vehicle_data.json'):
        """Save vehicle data to file"""
        # Convert datetime objects to strings
        data_to_save = {}
        for plate, visits in self.vehicle_data.items():
            data_to_save[plate] = [
                {
                    'timestamp': v['timestamp'].isoformat(),
                    'vehicle_type': v['vehicle_type']
                }
                for v in visits
            ]
            
        with open(filename, 'w') as f:
            json.dump(data_to_save, f)

    def load_vehicle_data(self, filename='vehicle_data.json'):
        """Load vehicle data from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            # Convert strings back to datetime
            for plate, visits in data.items():
                self.vehicle_data[plate] = [
                    {
                        'timestamp': datetime.datetime.fromisoformat(v['timestamp']),
                        'vehicle_type': v['vehicle_type']
                    }
                    for v in visits
                ]
                
        except FileNotFoundError:
            print(f"No existing data file found at {filename}")

    def process_frame(self, frame):
        """Process a frame and return detected vehicles with license plates"""
        # Detect vehicles
        vehicles = self.detect_vehicles(frame)
        detected_data = []
        
        for vehicle in vehicles:
            # Extract license plate
            license_plate, confidence = self.extract_license_plate(frame, vehicle['bbox'])
            
            if license_plate and confidence > 0.5:  # Minimum confidence threshold
                # Track vehicle
                self.track_vehicle(
                    license_plate,
                    vehicle['type'],
                    datetime.datetime.now()
                )
                
                detected_data.append({
                    'license_plate': license_plate,
                    'vehicle_type': vehicle['type'],
                    'confidence': confidence,
                    'bbox': vehicle['bbox']
                })
                
                # Draw bounding box and info
                x1, y1, x2, y2 = map(int, vehicle['bbox'])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{vehicle['type']}: {license_plate}",
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
        return frame, detected_data

    def run(self, source=0):
        """Run vehicle recognition system"""
        cap = cv2.VideoCapture(source)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frame, detected_vehicles = self.process_frame(frame)
            
            # Display frame
            cv2.imshow('Vehicle Recognition', processed_frame)
            
            # Print detections
            for vehicle in detected_vehicles:
                print(f"\nDetected {vehicle['vehicle_type']}")
                print(f"License Plate: {vehicle['license_plate']}")
                print(f"Confidence: {vehicle['confidence']:.2f}")
                
                # Get vehicle history
                history = self.get_vehicle_history(vehicle['license_plate'])
                if len(history) > 1:
                    print(f"Previous visits: {len(history)-1}")
                    
                print("-" * 50)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        # Save data before exit
        self.save_vehicle_data()

if __name__ == "__main__":
    recognizer = VehicleRecognition()
    # Load previous data if exists
    recognizer.load_vehicle_data()
    # Run recognition system
    recognizer.run()