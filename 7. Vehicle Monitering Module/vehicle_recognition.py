import cv2
from ultralytics import YOLO
import easyocr
from datetime import datetime

# Load models
yolo_model = YOLO("yolov8n.pt")  # General YOLOv8 model for car detection
ocr_reader = easyocr.Reader(['en'])

# Placeholder: link vehicle plate to known person later
vehicle_log = {}

cap = cv2.VideoCapture("vehicle_entry.mp4")  # Replace with live feed or 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = yolo_model(frame)[0]
    vehicles = [box for box in results.boxes.data.tolist()
                if int(box[5]) in [2, 3, 5, 7]]  # 2: car, 3: motorbike, etc.

    for box in vehicles:
        x1, y1, x2, y2, conf, cls = map(int, box[:6])
        vehicle_crop = frame[y1:y2, x1:x2]
        gray = cv2.cvtColor(vehicle_crop, cv2.COLOR_BGR2GRAY)

        # OCR to read plate
        result = ocr_reader.readtext(gray)
        plate_number = "Unknown"

        for (_, text, prob) in result:
            if len(text) >= 5 and prob > 0.5:
                plate_number = text
                break

        # Draw on frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
        cv2.putText(frame, f"Plate: {plate_number}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        if plate_number != "Unknown" and plate_number not in vehicle_log:
            vehicle_log[plate_number] = {
                "detected_time": str(datetime.now()),
                "camera": "Outdoor Entry",
                "frame_coords": (x1, y1, x2, y2)
            }
            print(f"[INFO] Vehicle {plate_number} logged at entry.")

    cv2.imshow("TRINETRA - Vehicle Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()