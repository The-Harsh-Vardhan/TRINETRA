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
(TRUNCATED FOR README - SEE FILE STRUCTURE ABOVE)

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