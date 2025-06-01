import threading
import queue
from datetime import datetime
import cv2
import json
import os
import sys
import argparse

# Import all modules
import sys
import os

# Add the parent directory to Python path to fix imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trinetra-system.1. Entrance Count Module.people_counter import PeopleCounter
from trinetra-system.2. Face Recognition and Identification Module.face_recognition_main import FaceRecognitionSystem
from trinetra-system.3. Customer Journey Tracker Module.multi_camera_tracker import MultiCameraTracker
from trinetra-system.4. Billing Counter Matcher Module.billing_face_matcher import BillingCounterMatcher
from trinetra-system.5. Object and Attire Description Module.attire_description import AttireDescriptor
from trinetra-system.6. Behavioral Insights Module.behavior_analytics import BehaviorAnalytics
from trinetra-system.7. Vehicle Monitering Module.vehicle_recognition import VehicleRecognition
from trinetra-system.8. Emotion Detection Module.emotion_recognition import EmotionDetector

class TRINETRASystem:
    def __init__(self):
        # Initialize all modules
        self.people_counter = PeopleCounter()
        self.face_recognition = FaceRecognitionSystem()
        self.customer_tracker = MultiCameraTracker()
        self.billing_matcher = BillingCounterMatcher()
        self.attire_descriptor = AttireDescriptor()
        self.behavior_analytics = BehaviorAnalytics()
        self.vehicle_recognition = VehicleRecognition()
        self.emotion_detector = EmotionDetector()
        
        # Shared data queues
        self.customer_queue = queue.Queue()  # For sharing customer data between modules
        self.event_queue = queue.Queue()  # For system events
        
        # System state
        self.running = False
        self.cameras = {}
        
    def add_camera(self, camera_id, source, camera_type):
        """Add a camera to the system"""
        self.cameras[camera_id] = {
            'source': source,
            'type': camera_type,
            'capture': cv2.VideoCapture(source)
        }
        
        if camera_type == 'entrance':
            self.customer_tracker.add_camera(camera_id, source)

    def process_entrance_camera(self, frame, camera_id):
        """Process entrance camera feed"""
        # Count people
        processed_frame = self.people_counter.process_frame(frame)
        
        # Recognize faces
        face_results = self.face_recognition.process_frame(frame)
        
        # Track customer journey
        self.customer_tracker.process_frame(camera_id, frame)
        
        return processed_frame

    def process_store_camera(self, frame, camera_id):
        """Process in-store camera feed"""
        # Track customer journey
        self.customer_tracker.process_frame(camera_id, frame)
        
        # Analyze attire
        frame, attire_desc = self.attire_descriptor.process_frame(frame)
        
        # Detect emotions
        frame, emotions = self.emotion_detector.process_frame(frame)
        
        # Update behavioral analytics
        for customer_id, emotion_data in emotions.items():
            self.behavior_analytics.add_emotion_data(customer_id, {
                'timestamp': datetime.now(),
                'emotion': emotion_data
            })
            
        return frame

    def process_billing_camera(self, frame, bill_frame):
        """Process billing counter camera feed"""
        matches = self.billing_matcher.process_billing_counter(frame, bill_frame)
        
        for match in matches:
            customer_id = match.get('customer_id')
            if customer_id:
                self.behavior_analytics.add_transaction(customer_id, match['bill_info'])
                
        return frame

    def process_parking_camera(self, frame):
        """Process parking area camera feed"""
        frame, vehicles = self.vehicle_recognition.process_frame(frame)
        return frame

    def camera_thread(self, camera_id):
        """Thread function for processing each camera feed"""
        camera_info = self.cameras[camera_id]
        
        while self.running:
            ret, frame = camera_info['capture'].read()
            if not ret:
                continue
                
            # Process frame based on camera type
            if camera_info['type'] == 'entrance':
                processed_frame = self.process_entrance_camera(frame, camera_id)
            elif camera_info['type'] == 'store':
                processed_frame = self.process_store_camera(frame, camera_id)
            elif camera_info['type'] == 'billing':
                # For billing, we need both customer face and bill image
                # This is a simplified version - you'll need to modify based on your setup
                processed_frame = self.process_billing_camera(frame, frame)
            elif camera_info['type'] == 'parking':
                processed_frame = self.process_parking_camera(frame)
            
            # Display processed frame
            cv2.imshow(f'Camera {camera_id}', processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

    def start(self):
        """Start the TRINETRA system"""
        self.running = True
        
        # Create threads for each camera
        threads = []
        for camera_id in self.cameras:
            thread = threading.Thread(
                target=self.camera_thread,
                args=(camera_id,)
            )
            threads.append(thread)
            thread.start()
            
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        # Cleanup
        for camera_info in self.cameras.values():
            camera_info['capture'].release()
        cv2.destroyAllWindows()
        
        # Save all data
        self.save_system_state()

    def save_system_state(self):
        """Save the state of all modules"""
        self.face_recognition.save_database()
        self.behavior_analytics.save_data()
        self.vehicle_recognition.save_vehicle_data()
        self.emotion_detector.save_emotions_data()

    def load_system_state(self):
        """Load the previous state of all modules"""
        self.face_recognition.load_database()
        self.behavior_analytics.load_data()
        self.vehicle_recognition.load_vehicle_data()
        self.emotion_detector.load_emotions_data()

    def test_camera(self, source):
        """Test if a camera source is accessible"""
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            return False
        ret, frame = cap.read()
        cap.release()
        return ret and frame is not None

    def list_available_cameras(self):
        """List all available camera devices"""
        available_cameras = []
        for i in range(10):  # Check first 10 indexes
            if self.test_camera(i):
                available_cameras.append(i)
        return available_cameras

    def configure_cameras(self, config_file=None):
        """Configure cameras from a config file or use defaults"""
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            # Default configuration
            config = {
                'cameras': [
                    {'id': 0, 'source': 0, 'type': 'entrance'},  # Default webcam
                    # Add more default cameras here
                ]
            }

        # Test and add configured cameras
        for camera in config['cameras']:
            if self.test_camera(camera['source']):
                self.add_camera(camera['id'], camera['source'], camera['type'])
                print(f"Successfully added {camera['type']} camera (ID: {camera['id']})")
            else:
                print(f"Failed to add camera {camera['id']} (source: {camera['source']})")

    @staticmethod
    def create_camera_config(output_file='camera_config.json'):
        """Create a camera configuration file"""
        config = {
            'cameras': [
                {
                    'id': 0,
                    'source': 0,  # Default webcam
                    'type': 'entrance'
                },
                {
                    'id': 1,
                    'source': "rtsp://username:password@ip_address:port/stream",
                    'type': 'store'
                },
                {
                    'id': 2,
                    'source': "rtsp://username:password@ip_address:port/stream",
                    'type': 'billing'
                },
                {
                    'id': 3,
                    'source': "rtsp://username:password@ip_address:port/stream",
                    'type': 'parking'
                }
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Created camera configuration template at {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TRINETRA Surveillance System')
    parser.add_argument('--config', type=str, help='Path to camera configuration file')
    parser.add_argument('--create-config', action='store_true', help='Create a camera configuration template')
    parser.add_argument('--list-cameras', action='store_true', help='List available camera devices')
    parser.add_argument('--test', action='store_true', help='Run in test mode with sample videos')
    args = parser.parse_args()

    system = TRINETRASystem()

    if args.create_config:
        system.create_camera_config()
        sys.exit(0)

    if args.list_cameras:
        available_cameras = system.list_available_cameras()
        print("Available camera devices:")
        for camera_id in available_cameras:
            print(f"Camera ID: {camera_id}")
        sys.exit(0)

    if args.test:
        # Use sample videos for testing
        sample_videos = {
            'entrance': 'sample_videos/entrance.mp4',
            'store': 'sample_videos/store.mp4',
            'billing': 'sample_videos/billing.mp4',
            'parking': 'sample_videos/parking.mp4'
        }
        
        # Create sample_videos directory if it doesn't exist
        os.makedirs('sample_videos', exist_ok=True)
        
        # Add available test videos
        for camera_type, video_path in sample_videos.items():
            if os.path.exists(video_path):
                system.add_camera(len(system.cameras), video_path, camera_type)
            else:
                print(f"Sample video for {camera_type} not found at {video_path}")
    else:
        # Configure cameras from config file or use defaults
        system.configure_cameras(args.config)

    if not system.cameras:
        print("No cameras configured. Please check your camera configuration or run with --test flag")
        sys.exit(1)

    # Load previous state
    system.load_system_state()
    
    # Start the system
    print("Starting TRINETRA system...")
    print("Press 'q' in any camera window to exit")
    system.start()
