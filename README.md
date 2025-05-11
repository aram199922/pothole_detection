# Automated Pothole Detection for Road Monitoring

[![Watch the demo](https://img.youtube.com/vi/_RKtE7-C0b4/0.jpg)](https://www.youtube.com/watch?v=_RKtE7-C0b4)

## Table of Contents
- [Introduction - Aim of The Project](#introduction---aim-of-the-project)
- [Data Collection and Preprocessing](#data-collection-and-preprocessing)
- [Training and Testing](#training-and-testing)
- [Raspberry Pi Deployment](#raspberry-pi-deployment)

## Introduction - Aim of The Project
This project proposes an automated pothole detection system leveraging deep learning-based object detection models: YOLOv8 and YOLOv11, trained on a custom-annotated dataset. To ensure high inferencing speed and portability, the models are optimized for deployment on edge devices: Raspberry Pi 4 and 5. The system is designed for real-time inference from live dashcam video streams, enabling on go detection and localization of road potholes. Detected potholes are geotagged using a GPS module, providing precise location data for maintenance planning. This lightweight, low-latency solution demonstrates the potential of integrating modern computer vision in real life applications.

As with any well-formulated detection problem, the project will start with gathering and preprocessing data with a wide variety of images. Then, it will move on to training and testing the model, and for this specific project, finish with deployment on the edge device and testing the model on a live video stream in that environment.

Read the whole README, where you can find tutorials and all the explanations about the project.
Start with the YOLO model easy introductory **How It Works** explanation video: <br>
https://www.youtube.com/watch?v=ag3DLKsl2vk&list=PLJ7aTi3ZNpXBdEvv3VlRk46Ei6cxeT_Il&index=15 <br>
For more Information visit the **official** website: <br>
https://www.ultralytics.com/yolo

**Before** starting the project in any of the environments run the following commands to create virtual environment: <br>
**In bash terminal**: <br>
python -m venv venv_name <br>
source venv_name/bin/activate (In linux) <br>
source venv_name/Scripts/activate (In Windows) <br>
pip install -r requirements.txt (or all the packages that will be needed) <br>
**In powershell**: <br>
python -m venv venv_name <br>
.\venv_name\bin\activate (In Linux) <br>
.\venv_name\Scripts\activate (In Windows) <br>
**If you get a "running scripts is disabled" error in PowerShell, you may need to run:** <br>
**Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass** <br>
pip install -r requirements.txt

## Data Collection and Preprocessing
For YOLO models specific labeling is needed, where each label of the image should be in seperate **.txt** file: <br>
**class_id x_center y_center width height**
1. class_id — integer representing the object class (starts from 0).
2. x_center — x-coordinate of the bounding box center (normalized).
3. y_center — y-coordinate of the bounding box center (normalized).
4. width — width of the bounding box (normalized).
5. height — height of the bounding box (normalized).

There were three main open source datasets used in this project (find in the **data** folder), here are the links for accessing and downloading those datasets:
1. https://datasetninja.com/road-pothole-images
2. https://www.kaggle.com/datasets/tallwinkingstan/road-traversing-knowledge-rtk-dataset
3. https://figshare.com/articles/figure/Potholes_dataset_with_YOLO_annotations/21214400/3?file=37622126

---

1. For the first dataset from datasetsninja.com, we will need to proceed with Kaggle and access the shared Google Drive. There will be four main subfolders, where one will need to choose based on the specific task and memory. They are all similar and have many common images. For this specific project, Dataset 1 (Simplex) was used. The folder contains Train and Test sets with their proper annotations (however, in COCO format used for the COCO dataset). As the annotation labels are all given in one file and we have a different labeling format other than the YOLO format, some preprocessing will be needed along with data splitting (train, test, validation). All this processes can be found in **scripts/data_annotation_converter.ipynb**.
2. For the second dataset (RTK dataset), only the subfolder AsphaltBad was used, as the project aims to make detections for asphalted roads. In this dataset, we don't have any proper bounding box annotations; hence, we will need to annotate it manually. For easy manual annotations refer to this tutorial which uses **cvat.ai** annotation tool: <br>
https://youtu.be/m9fH9OWn8YM?si=4NiwVybZUtrcjJOS&t=304
3. For the third dataset (Figshare), the whole folder was downloaded. It contains subfolders of images from different times of day and weather conditions. This is very useful, as a wide variety gives the opportunity to train a well-generalized model. Here, just refoldering and splitting into train and validation is needed. For second and third datasets processes use **scripts/data_converter.ipynb**.

**All the processed data will be in yolo_data folder**

**Only samples from each dataset are in the folders!!!**

## Training and Testing
Training of the model can be done both in the Google Colab environment and on a local machine if a CUDA-enabled high-performance GPU is available.

Notebooks for both cases are available in the GitHub repository with their respective **.yaml** files. Adjust the parameters and hyperparameters for your specific need (epochs, augmentations, epochs, imgsz, etc.). Find the codes in:
**scripts/training_colab.ipynb** and **scripts/training_local.ipynb**.

YOLO version 8 and 11 models have been trained, because these variants are well optimized for different platforms. Models were trained for 640x640 and 736x736 pixel-sized images. From numerous models, three of the versions are in the **results** folder (with their NCNN-converted versions).

For testing the inference on video or image, refer to **scripts/predict_image.py** and **scripts/predict_video.py**.
Examples of inferenced images and videos can be found in **test_pothole_videos** and **test_pothole_images** folders. (or watch the video in YouTube) <br>
[![Watch the demo](https://img.youtube.com/vi/nSzvAnHtJfE/0.jpg)](https://www.youtube.com/watch?v=nSzvAnHtJfE) <br>
The model sometimes fails to detect very large potholes, where essentially the entire road is a "pothole". Additionally, in cases where potholes are filled with water, the model occasionally struggles to identify them. These issues are primarily due to a lack of sufficient data. While there are some images of water-filled potholes, more data is needed to improve detection in these scenarios. The same applies to very large potholes, where more examples are required to train the model effectively.

## Raspberry Pi Deployment
For deploying the model on Raspberry Pi, refer to the tutorial and it's article: <br> 
https://www.youtube.com/watch?v=XKIm_R_rIeQ&list=PLJ7aTi3ZNpXBdEvv3VlRk46Ei6cxeT_Il&index=17 <br>
https://core-electronics.com.au/guides/raspberry-pi/getting-started-with-yolo-object-and-animal-recognition-on-the-raspberry-pi/ <br>
Very important to make sure to install ultralytics with the following command: <br>
pip install ultralytics[export]

The model can be deployed on Raspberry Pi 4 or 5 with an up-to-date OS installed, although the Pi 5 is preferred for better inferencing speed (FPS). Before moving on, our model should be converted to NCNN format (quantization) for lighter workload on Raspberry. For this refer to **scripts/ncnn_conversion.py**.

Module UBlox NEO-M8N GPS was used, instructions can be found in the following tutorial: <br>
https://www.instructables.com/Interfacing-GPS-Module-With-Raspberry-Pi/

**All the Raspberry scripts should be run in Raspberry environment**

**scripts/raspberry/gps_probe.py** file is helpful for monitoring the signals coming from the GPS module.

**scripts/raspberry/live_detection_test.py** will be helpful for inferencing live videostream and saving it. (Webcamera plugged in USB port of Raspberry will be needed)

**scripts/raspberry/pothole_detector.py** is the main file which will start the live stream detection application. It will show FPS (frames inferenced in a second), gps information (longitude and latitude) on the output video file. It also logs the gps coordinates whenever a pothole is detected.

Showcase of the application (in car setup and the video of real life detection) can be watched in: <br>
Setup: https://www.youtube.com/watch?v=nONVP-yJtdk <br>
Showcase: https://www.youtube.com/watch?v=_RKtE7-C0b4






