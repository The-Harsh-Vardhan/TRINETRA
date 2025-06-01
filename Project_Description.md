# TRINETRA

## ⭐ Project Title

❖ **TRINETRA**

➤ **Targeted Retail Insights via NETworked Real-time Analytics**

**"Smart Surveillance and Customer Behavior Analytics System Using Multi-Camera
Computer Vision"**

## ⭐ Project Objectives

```
● Track customer footfall and movement inside a shop or cafe using CCTV feeds.
```
```
● Recognize repeat customers and personalize experiences through facial recognition.
```
```
● Extract behavioral and transactional insights such as waiting time, purchase habits,
and service quality.
```
```
● Monitor staff performance and recommend operational improvements.
```
```
● Associate external vehicle data with customer identity for extended profiling.
```
## System Architecture Overview

```
Camera Feeds → Central Server → Processing Modules:
```
- Entrance Count Module
- Face Recognition Module
- Object & Clothing Descriptor
- Billing Camera Analysis
- Vehicle Recognition Module
↓
Unified Customer Profile Database + Staff Performance Dashboard


## ⭐ Core Modules and Functions

**1. Entrance Count Module**

```
● Purpose : Count number of people entering and exiting.
```
```
● Tech : Background subtraction or YOLO/Detectron2 + tracking (Deep SORT or
ByteTrack).
```
**2. Face Recognition & Identification**

```
● Purpose : Match faces to existing database.
```
```
● Tech : FaceNet / Dlib / DeepFace for embedding; cosine similarity for matching.
```
**3. Customer Journey Tracker**

```
● Purpose : Track movements across different cameras.
```
```
● Tech : Multi-camera person re-identification using appearance and trajectory cues.
```
**4. Billing Counter Matcher**

```
● Purpose : Match customer with bill data using face detection and timestamp
correlation.
```
```
● Tech : OCR for bill details + face alignment.
```
**5. Object & Attire Description**

```
● Purpose : Describe what the customer is wearing or carrying.
```
```
● Tech : CLIP or BLIP models + object detection and captioning.
```
**6. Behavioral Insights Engine**


● **Features** :

```
○ Waiting time (arrival to bill time)
```
```
○ Repeat orders/favorite items
```
```
○ Companion identification
```
```
○ Staff member interaction
```
```
○ Avg. order value per visit
```
**7. Vehicle Monitoring Module**

● **Purpose** : Extract and match vehicle numbers to customers.

● **Tech** : License Plate Recognition (LPR) models like OpenALPR or PaddleOCR.

###### 📊 Output & Applications

```
For Management:
```
● Staff analytics and performance dashboard

● Heatmaps of customer flow and service time

● VIP or high-value customer alerts

```
For Staff:
```
● Notification of regular or VIP customers

● Behavioral tips based on previous history

● Smart recommendations on service approach


###### 🔐 Ethical Considerations

● **Privacy** : Ensure data encryption, consent notices, and opt-out options.

● **Bias Mitigation** : Use diverse datasets for training facial recognition and
re-identification models.

● **Compliance** : Align with GDPR or local data protection laws.

###### 🧾 Possible Tech Stack

```
Componen
t
```
```
Suggested Tools
```
```
Face
Recognition
```
```
DeepFace, Dlib, FaceNet
```
```
Object
Detection
```
```
YOLOv8, Detectron
```
```
Tracking Deep SORT, ByteTrack
```
```
OCR Tesseract, PaddleOCR
```
```
Captioning BLIP, CLIP, ImageBind
```
```
Backend Flask/FastAPI, PostgreSQL
```
```
Frontend
Dashboard
```
```
React.js + D3.js or Streamlit
```
```
Camera
Feed
```
```
RTSP ingestion via OpenCV or
FFmpeg
```

## ⭐ Research Papers

➤Here are some research papers closely aligned with your project on customer tracking
and behavioral analytics in retail using computer vision:

###### 📚 Relevant Research Papers

```
No
.
```
```
Title Summary
```
```
1 Advanced Customer Behavior
Tracking and Heatmap Analysis
with YOLOv5 and DeepSORT
(Mohamed et al., 2024)
```
```
Uses YOLOv5 and DeepSORT to
analyze customer movement,
generate heatmaps, and optimize
product placement in real-time.
```
```
2 System and Method for Retail
Customer Tracking in Surveillance
Camera Network (Burke, 2016,
Patent)
```
```
Describes a multi-camera retail
tracking system matching faces at
POS to earlier footage for behavior
and interaction analysis.
```
```
3 Towards In-Store Multi-Person
Tracking Using Head Detection
and Track Heatmaps (Musaev et al.,
2020)
```
```
Uses head detection and heatmaps
for accurate multi-person tracking in
store environments, addressing
occlusions and trajectory mapping.
```
```
4 Video-CRM: Understanding
Customer Behaviors in Stores
(Haritaoglu et al., 2013)
```
```
One of the earliest systems for group
detection at checkout and product
interaction tracking using stereo
cameras.
```
```
5 Deep Learning-Based Approach to
Detect Customer Age, Gender, and
Expression in Surveillance Video
(Ijjina et al., 2020)
```
```
Proposes WideResNet and Xception
for demographic and emotion
detection in low-quality retail CCTV
footage.
```
These papers can guide both your implementation strategy and technical choices for
modules like face tracking, multi-camera identity re-matching, behavioral analytics, and
demographic tagging.


## ⭐ WORKFLOW

➤Here's a **comprehensive end-to-end workflow** for your **TRINETRA** system — from the
**moment a customer arrives** at the shop until they **exit** — detailing every **camera’s role** ,
every **analytic recorded** , and how the system interacts in real time.

### 🧠 TRINETRA Smart Surveillance Workflow

###### 🏪 Scenario:

A customer visits a retail store equipped with **multi-camera AI-powered computer vision
system**.


### 🟢 1. Customer Arrival (Outside the Shop)

###### 🎥 Camera 1: Outdoor Entry Camera

**Function:** Detects approaching individuals and vehicles.

```
● License Plate Recognition (LPR):
```
```
○ Detects and OCRs vehicle number using OpenALPR or PaddleOCR.
```
```
○ Matches to existing customer database.
```
```
○ Links vehicle ID to customer profile.
```
### 🚶 2. Entry Detection

###### 🎥 Camera 2: Overhead Entrance Camera (Inside)

**Function:** Detects when people enter or exit.

```
● People Detection (YOLOv8) + Tracking (ByteTrack or Deep SORT)
```
```
○ Draws virtual line across entrance to classify entry vs exit.
```
```
○ Increments footfall count.
```
```
○ Triggers the Face Capture Event on entry.
```
### 🧑 3. Customer Identification

###### 🎥 Camera 3: Face Recognition Camera at Entry

**Function:** Captures face and runs recognition.


```
● Face Detection + Embedding Comparison (DeepFace or face_recognition)
```
```
○ If recognized :
```
```
■ Fetches Customer ID from database.
```
```
■ Adds timestamped visit log.
```
```
○ If unrecognized :
```
```
■ Classifies as new customer.
```
```
■ Stores face encoding and snapshot.
```
```
■ Flags for registration at billing counter.
```
### 🕵 4. In-Shop Tracking

###### 🎥 Camera 4: Top-View or Corridor Cameras

**Function:** Re-identifies and follows customer through store.

```
● Person Re-ID based on face, clothing (color histograms), or deep embeddings.
```
```
● Logs:
```
```
○ Dwell time at different zones
```
```
○ Movement path (heatmap)
```
```
○ Waiting time (e.g. in queue)
```
### 🤖 5. Object & Appearance Analysis


###### 🧠 Triggered on Any Camera Where Full Body Visible

**Function:** Describes what the customer is **wearing or carrying**.

```
● Object Detection + Image Captioning (YOLOv8 + CLIP/BLIP)
```
```
● Output:
```
```
○ “Red t-shirt, black jeans, carrying backpack”
```
```
○ Saved as text description in customer profile.
```
### 🧾 6. Billing & Final Face Confirmation

###### 🎥 Camera 5: Billing Counter Camera

**Function:** Captures face + context at checkout.

```
● Face Verification :
```
```
○ Cross-matches with entry face → confirms identity.
```
```
● Fetch Bill Details (manual input or POS system OCR)
```
```
○ Total order value
```
```
○ Items bought
```
```
○ Staff name serving them
```
```
● Logs:
```
```
○ Visit duration = Exit time - Entry time
```
```
○ Average order value
```

```
○ Most frequent purchases (over time)
```
### 🟣 7. Exit Detection

###### 🎥 Camera 2 (Reused): Exit Line Crossing

**Function:** Detects when person leaves.

```
● Tracking ID used to mark exit time.
```
```
● Updates visit record with:
```
```
○ Total time spent
```
```
○ Zone-specific time
```
```
○ Queue duration
```
```
○ Served by staff X
```
### 📊 8. Real-Time Data Logging & Dashboard Update

```
● Database Updated:
```
```
○ Customer_Profile
```
```
○ Visit_History
```
```
○ Vehicle_Tracking
```
```
○ Staff_Interaction
```
```
● Dashboard Triggers:
```

```
○ Regular customer alert
```
```
○ High-value customer → Assign experienced staff
```
```
○ VIP alerts for staff awareness
```
### 🛡 9. Privacy & Security Checks

```
● Unknown faces are blurred or anonymized.
```
```
● All embeddings are encrypted.
```
```
● Data is retained under consent-driven retention policies.
```
###### 📉 Sample Timeline

```
Time Action Module
```
```
10:02 Vehicle detected LPR
```
```
10:03 Face captured at
entrance
```
```
Face Recognition
```
```
10:04 Customer enters store Person Counting
```
```
10:06–10:
5
```
```
Browsing inside Re-ID + Tracking
```
```
10:16 At billing Face match + POS link
```
```
10:18 Exits shop Exit tracking
```