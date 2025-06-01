import cv2
from ultralytics import YOLO
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load YOLO model for person detection
model = YOLO("yolov8n.pt")

# Load BLIP model for captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

cap = cv2.VideoCapture("input.mp4")  # Replace with live feed

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    people = [box for box in results.boxes.data.tolist() if int(box[5]) == 0]

    for box in people:
        x1, y1, x2, y2, conf, cls = map(int, box[:6])
        person_crop = frame[y1:y2, x1:x2]

        if person_crop.shape[0] == 0 or person_crop.shape[1] == 0:
            continue

        # Convert crop to PIL Image for BLIP
        image_pil = Image.fromarray(cv2.cvtColor(person_crop, cv2.COLOR_BGR2RGB))

        inputs = processor(images=image_pil, return_tensors="pt")
        with torch.no_grad():
            out = blip_model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)

        # Draw description on frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 128, 0), 2)
        cv2.putText(frame, caption, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 128, 0), 2)

        print(f"[INFO] Description: {caption}")

    cv2.imshow("TRINETRA - Attire Description", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()