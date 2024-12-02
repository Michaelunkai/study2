import os
import cv2
import numpy as np
import torch

# Step 1: Download the YOLOv5 model
os.system('wget https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5s.pt')

# Step 2: Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Step 3: Open the video capture
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for faster processing
    img = cv2.resize(frame, (640, 640))

    # Convert frame to a format suitable for YOLOv5
    results = model(img)

    # Process the results
    labels, confidences, boxes = results.xyxyn[0][:, -1], results.xyxyn[0][:, 4], results.xyxyn[0][:, :-1]
    
    for i, (box, conf, label) in enumerate(zip(boxes, confidences, labels)):
        if conf > 0.3:  # Filter out weak detections
            x1, y1, x2, y2 = int(box[0] * frame.shape[1]), int(box[1] * frame.shape[0]), int(box[2] * frame.shape[1]), int(box[3] * frame.shape[0])
            color = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{model.names[int(label)]} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            print(f"{model.names[int(label)]}: {conf:.2f}")

    # Show the output frame
    cv2.im ow("Video Feed", frame)

    # If 'q' is pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
