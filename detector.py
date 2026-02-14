import cv2
from ultralytics import YOLO

# Load the official YOLOv8 model (Small version is faster)
model = YOLO('yolov8n.pt')

# Open video file (Use '0' for Webcam)
cap = cv2.VideoCapture("traffic.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame, stream=True)

    car_count = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Class 2 is 'Car' in COCO dataset
            cls = int(box.cls[0])
            if cls == 2: 
                car_count += 1
                # Draw box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display Count
    cv2.putText(frame, f"Cars: {car_count}", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("SIH Traffic AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()