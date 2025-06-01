import torch
import clip
from PIL import Image
import cv2
import numpy as np
from transformers import pipeline
from ultralytics import YOLO

class AttireDescriptor:
    def __init__(self):
        # Load YOLO model for person detection
        self.yolo_model = YOLO("yolov8n.pt")
        
        # Load CLIP model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        # Load image captioning model
        self.caption_generator = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        
        # Predefined clothing and accessory categories
        self.categories = [
            "t-shirt", "shirt", "pants", "jeans", "dress", "skirt", "jacket",
            "coat", "sweater", "hat", "cap", "sunglasses", "bag", "backpack",
            "suit", "tie", "formal wear", "casual wear", "sports wear",
            "red clothing", "blue clothing", "green clothing", "black clothing",
            "white clothing", "yellow clothing", "pink clothing"
        ]
        
        # Encode categories
        self.category_features = self.model.encode_text(
            clip.tokenize(self.categories).to(self.device)
        )

    def generate_description(self, image):
        """Generate a natural language description of the person's attire"""
        # Convert image for captioning
        if isinstance(image, np.ndarray):
            # Convert OpenCV BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
        else:
            pil_image = image
            
        # Generate caption
        captions = self.caption_generator(pil_image)
        general_description = captions[0]['generated_text']
        
        # Prepare image for CLIP
        image_input = self.preprocess(pil_image).unsqueeze(0).to(self.device)
        
        # Get image features
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            
        # Calculate similarities with categories
        similarities = (100.0 * image_features @ self.category_features.T).softmax(dim=-1)
        
        # Get top matches
        values, indices = similarities[0].topk(5)
        
        # Build detailed description
        detected_items = [
            f"{self.categories[idx]} ({values[i].item():.1f}%)"
            for i, idx in enumerate(indices)
        ]
        
        return {
            'general_description': general_description,
            'detected_items': detected_items,
            'confidence_scores': values.tolist()
        }

    def detect_person(self, frame):
        """Detect person in frame using YOLOv8"""
        results = self.yolo_model(frame)[0]
        
        person_boxes = []
        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            if cls == 0:  # person class
                person_boxes.append(box.tolist())
                
        return person_boxes

    def process_frame(self, frame):
        """Process a frame and return descriptions for each detected person"""
        person_boxes = self.detect_person(frame)
        descriptions = []
        
        for box in person_boxes:
            x1, y1, x2, y2 = map(int, box)
            person_img = frame[y1:y2, x1:x2]
            
            # Get description
            description = self.generate_description(person_img)
            descriptions.append({
                'bbox': box,
                'description': description
            })
            
            # Draw bounding box and description
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, description['general_description'][:50],
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
        return frame, descriptions

    def run(self, source=0):
        """Run real-time attire description"""
        cap = cv2.VideoCapture(source)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frame, descriptions = self.process_frame(frame)
            
            # Display frame
            cv2.imshow('Attire Description', processed_frame)
            
            # Print descriptions
            for desc in descriptions:
                print("\nPerson Description:")
                print(f"General: {desc['description']['general_description']}")
                print("Detected Items:")
                for item in desc['description']['detected_items']:
                    print(f"- {item}")
                print("-" * 50)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    descriptor = AttireDescriptor()
    descriptor.run()