import cv2
from ultralytics import YOLO

# Load model
model = YOLO("runs_v11_640p/detect/train/weights/best_ncnn_model")

# Open the camera (0 = default camera)
cap = cv2.VideoCapture(0)

# Set camera resolution (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output_inferenced.avi', fourcc, 4, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inference
    results = model(frame, verbose=False)

    # Draw results on frame
    annotated_frame = results[0].plot()

    # Optional: calculate FPS if you want to log or debug
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time
    cv2.putText(annotated_frame, f'FPS: {fps:.2f}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Write the frame
    out.write(annotated_frame)

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()
