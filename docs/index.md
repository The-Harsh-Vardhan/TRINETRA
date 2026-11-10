# TRINETRA

Targeted Retail Insights via NETworked Real-time Analytics: a research proof-of-concept exploring multi-camera computer vision for smart retail. It is not a production system.

Eight standalone Python modules cover entrance counting, face recognition, billing matching, scene description, behavioral logging, vehicle plate reading and emotion detection, built on OpenCV, YOLOv8, face_recognition, DeepFace, BLIP and EasyOCR.

- Source: [The-Harsh-Vardhan/TRINETRA](https://github.com/The-Harsh-Vardhan/TRINETRA)
- [Architecture](architecture.md)

## Run a module

```bash
git clone https://github.com/The-Harsh-Vardhan/TRINETRA.git
cd TRINETRA
python "1. Entrance Count Module/people_counter.py"
```

Dependencies are listed in the README; YOLOv8 weights (`yolov8n.pt`) are downloaded from Ultralytics. `people_counter.py` reads `input.mp4` from the working directory.
