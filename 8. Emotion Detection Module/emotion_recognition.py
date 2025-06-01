import cv2
from deepface import DeepFace
from datetime import datetime

# Store logs
emotion_log = []

cap = cv2.VideoCapture(0)  # Replace with camera or video file

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = analysis[0]['dominant_emotion']
        score = analysis[0]['emotion'][dominant_emotion]

        # Annotate frame
        cv2.putText(frame, f"Emotion: {dominant_emotion} ({score:.1f}%)", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # Log only new entries
        if not emotion_log or emotion_log[-1]['emotion'] != dominant_emotion:
            emotion_log.append({
                "timestamp": str(datetime.now()),
                "emotion": dominant_emotion,
                "confidence": round(score, 2)
            })
            print(f"[LOG] {dominant_emotion} ({score:.1f}%) at {emotion_log[-1]['timestamp']}")

    except Exception as e:
        print(f"[ERROR] {e}")
        cv2.putText(frame, "Face not detected", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("TRINETRA - Emotion Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()