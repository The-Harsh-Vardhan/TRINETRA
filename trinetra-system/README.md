# 🧠 TRINETRA

> **TRINETRA** — Targeted Retail Insights via NETworked Real-time Analytics — is a multi-camera smart surveillance system for retail shops and cafes, leveraging Computer Vision, AI, and Behavior Analytics to monitor and optimize customer experience and staff performance.

## 📌 Features
- ✅ Real-time people counting
- ✅ Face recognition & customer ID logging
- ✅ Multi-camera person tracking
- ✅ Billing counter face & order linkage
- ✅ Clothing and object description
- ✅ Emotion detection for mood logging
- ✅ Weapon and threat detection
- ✅ Vehicle license plate recognition
- ✅ Behavior analytics: time, queue, items

## 🗂️ Directory Structure
```
trinetra-system
├── 1. Entrance Count Module
│   └── people_counter.py
├── 2. Face Recognition and Identification Module
│   ├── face_recognition_main.py
│   ├── save_new_face.py
│   └── faces.pkl
├── 3. Customer Journey Tracker Module
│   └── multi_camera_tracker.py
├── 4. Billing Counter Matcher Module
│   └── billing_face_matcher.py
├── 5. Object and Attire Description Module
│   └── attire_description.py
├── 6. Behavioral Insights Module
│   └── behavior_analytics.py
├── 7. Vehicle Monitoring Module
│   └── vehicle_recognition.py
├── 8. Emotion Detection Module
│   └── emotion_recognition.py
├── Project_Description.md
├── Project_Proposal.txt
└── README.md
```

## 🛠️ Installation Guide

### 1. Set Up Python Environment
```bash
python -m venv trinetra-env
source trinetra-env/bin/activate  # or trinetra-env\Scripts\activate on Windows
```

### 2. Install Dependencies
```bash
pip install opencv-python ultralytics face_recognition deepface easyocr torch torchvision transformers numpy
```

### 3. Download YOLOv8 Weights
Place `yolov8n.pt` in your working directory.

### 4. Run Modules
Examples:
```bash
python "1. Entrance Count Module/people_counter.py"
python "2. Face Recognition and Identification Module/face_recognition_main.py"
```

## 🔐 Privacy & Ethics
- Facial data is stored securely
- Only known customers are tracked
- All activity is GDPR-aligned and anonymized when necessary

## 📄 License
MIT