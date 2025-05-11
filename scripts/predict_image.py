from ultralytics import YOLO
import cv2
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

image_path_out = os.path.join(script_dir, '..','test_pothole_images','Vid_Pd_sunset_00000103_out.jpg')
image_path = os.path.join(script_dir, '..','test_pothole_images','Vid_Pd_sunset_00000103.jpg')
model_path = os.path.join(script_dir, '..', 'results', 'yolov11_model_736p', 'weights', 'best.pt')

model = YOLO(model_path)

img = cv2.imread(image_path)

results = model(image_path, conf=0.1)

results[0].show()
results[0].save(filename=image_path_out)
print("Detection complete! Check 'output.jpg'.")