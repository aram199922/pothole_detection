import cv2
from ultralytics import YOLO
import serial
import pynmea2
import time

# Load YOLO model
model = YOLO("best_ncnn_model")

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output_inferenced.avi', fourcc, 10, (640, 480))

# Initialize GPS serial connection
gps_serial = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

# Open GPS log file
gps_log = open('pothole_gps_log.txt', 'a')

def get_gps_coordinates():
    line = gps_serial.readline().decode('ascii', errors='replace').strip()
    if line.startswith('$GPGGA') or line.startswith('$GNGGA'):
        try:
            msg = pynmea2.parse(line)
            if msg.latitude and msg.longitude:
                return msg.latitude, msg.longitude
        except pynmea2.ParseError:
            pass
    return None, None

last_latitude = 0.0
last_longitude = 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform inference
    results = model(frame, verbose=False)

    # Annotate frame
    annotated_frame = results[0].plot()

    # Calculate FPS
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time
    cv2.putText(annotated_frame, f'FPS: {fps:.2f}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Retrieve GPS coordinates
    latitude, longitude = get_gps_coordinates()
    if latitude is not None and longitude is not None:
        last_latitude = latitude
        last_longitude = longitude
    
    #latitude, longitude = get_gps_coordinates()
    #gps_text = f'Lat: {latitude:.6f}, Lon: {longitude:.6f}'
    gps_text = f'Lat: {last_latitude:.6f}, Lon: {last_longitude:.6f}'
    cv2.putText(annotated_frame, gps_text, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Check for pothole detection
    pothole_detected = False
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        if class_name.lower() == 'pothole':
            pothole_detected = True
            break

    # If pothole detected, log GPS coordinates
    if pothole_detected:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        gps_log.write(f'{timestamp}, {last_latitude}, {last_longitude}\n')
        #gps_log.write(f'{timestamp}, {latitude}, {longitude}\n')
        gps_log.flush()

    # Display and save frame
    cv2.imshow('YOLO Live Detection', annotated_frame)
    out.write(annotated_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
out.release()
gps_log.close()
cv2.destroyAllWindows()

