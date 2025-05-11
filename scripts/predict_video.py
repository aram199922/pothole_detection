import os
from ultralytics import YOLO
import cv2

script_dir = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(script_dir, '..', 'results', 'yolov11_model_736p', 'weights', 'best.pt')
video_path = os.path.join(script_dir, '..', 'test_pothole_videos', 'dashcam_video_2_in.mp4')
video_path_out = os.path.join(script_dir, '..', 'test_pothole_videos', 'dashcam_video_2_out.mp4')

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model = YOLO(model_path)

threshold = 0.3

while ret:

    results = model(frame)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            label = f"{results.names[int(class_id)].upper()} {score:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()