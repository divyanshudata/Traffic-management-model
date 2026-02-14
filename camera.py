import cv2
from ultralytics import YOLO
import cvzone
import math
import os

# --- CONFIGURATION ---
# Use "traffic_video.mp4" or 0 for Webcam
VIDEO_SOURCE = "traffic_video.mp4" 

model = YOLO('yolov8n.pt')
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

cap = cv2.VideoCapture(VIDEO_SOURCE)

print("🎥 Camera Active. Writing data to sensor_data.txt...")

while True:
    success, img = cap.read()
    if not success:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop video
        continue

    results = model(img, stream=True, verbose=False)
    current_density = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            if currentClass in ["car", "truck", "bus", "motorbike"]:
                current_density += 1
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))

    # --- THE GOD MODE LINK ---
    # Write the car count to a file so the Simulation can read it
    with open("sensor_data.txt", "w") as f:
        f.write(str(current_density))

    # Display on screen
    color = (0, 255, 0)
    if current_density > 5: color = (0, 0, 255)
    cvzone.putTextRect(img, f'Real-Time Density: {current_density}', (50, 50), 
                       scale=3, thickness=3, colorT=(255, 255, 255), colorR=color)

    cv2.imshow("SIH - Camera Input", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()