import cv2
import numpy as np
from ultralytics import YOLO

# Initialize YOLOv8 model
model = YOLO("yolov8n.pt")  # You can use yolov8s.pt for better accuracy

# Initialize video feed
cap = cv2.VideoCapture("input.mp4")  # Replace with 0 for webcam

# Line position for entry/exit
line_position = 300
enter_count, exit_count = 0, 0

# Simple centroid-based tracking
trackers = {}
next_id = 0

def get_centroid(x1, y1, x2, y2):
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def direction_check(old_y, new_y):
    if old_y < line_position and new_y >= line_position:
        return "in"
    elif old_y > line_position and new_y <= line_position:
        return "out"
    return None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    detections = []

    for box in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = box
        if int(cls) == 0:  # Class 0 is person
            cx, cy = get_centroid(x1, y1, x2, y2)
            detections.append(((x1, y1, x2, y2), (cx, cy)))

    # Update trackers
    updated = {}
    for (box, centroid) in detections:
        cx, cy = centroid
        matched = False
        for id_, data in trackers.items():
            prev_cx, prev_cy = data["centroid"]
            if abs(cx - prev_cx) < 50 and abs(cy - prev_cy) < 50:
                direction = direction_check(prev_cy, cy)
                if direction == "in":
                    enter_count += 1
                elif direction == "out":
                    exit_count += 1
                updated[id_] = {"centroid": (cx, cy), "box": box}
                matched = True
                break
        if not matched:
            updated[next_id] = {"centroid": (cx, cy), "box": box}
            next_id += 1
    trackers = updated

    # Draw line
    cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (255, 0, 0), 2)
    cv2.putText(frame, f"IN: {enter_count} | OUT: {exit_count}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Draw boxes
    for id_, data in trackers.items():
        x1, y1, x2, y2 = map(int, data["box"])
        cx, cy = data["centroid"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {id_}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("TRINETRA - People Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()