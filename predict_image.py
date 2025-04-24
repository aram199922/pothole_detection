from ultralytics import YOLO
import cv2
import os

model_path = os.path.join('.', 'runs_300_736p', 'detect', 'train', 'weights', 'best.pt')
model = YOLO(model_path)


IMAGE_DIR = os.path.join('.', 'pothole_images','test_1.jpg')
print(IMAGE_DIR)


img = cv2.imread(IMAGE_DIR)

results = model(IMAGE_DIR, conf=0.1)

results[0].show()

image_path_out = os.path.join('.', 'pothole_images','test_1_out_300.jpg')
results[0].save(filename=image_path_out)

print("Detection complete! Check 'output.jpg'.")