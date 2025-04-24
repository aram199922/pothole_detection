# Automated Pothole Detection for Road Monitoring

## Table of Contents
- [Introduction - Aim of The Project](#introduction)
- [Data Collection and Preprocessing](#data-preprocessing)
- [Training and Testing](#training)
- [Raspberry Pi Deployment](#raspberry-pi])

## Introduction - Aim of The Project
This project proposes an automated pothole detection system leveraging deep learning-based object detection models: YOLOv8 and YOLOv11, trained on a custom-annotated dataset. To ensure high inferencing speed and portability, the models are optimized for deployment on edge devices: Raspberry Pi 4 and 5. The system is designed for real-time inference from live dashcam video streams, enabling on go detection and localization of road potholes. Detected potholes are geotagged using a GPS module, providing precise location data for maintenance planning. This lightweight, low-latency solution demonstrates the potential of integrating modern computer vision in real life applications.

As any other well formulated detection problem the project will start from gathering and preprocessing data with wide variety of images. Then, move on to training and testing the model and for this specific project finishing with deployment on the edge device and testing the model on live video stream in that environment.

Read the whole README, where you can find tutorials and all the explanations about the project.
Start with the YOLO model easy introductory **How It Works** explanation video:
https://www.youtube.com/watch?v=ag3DLKsl2vk&list=PLJ7aTi3ZNpXBdEvv3VlRk46Ei6cxeT_Il&index=15
For more Information visit the **official** website:
https://www.ultralytics.com/yolo

**Before** starting the project in any of the environments run the following commands to create virtual environment:
In bash terminal:
python -m venv venv_name
source venv_name/bin/activate
pip install -r requirements.txt (or all the packages that will be needed)

## Data Collection and Preprocessing
For YOLO models specific labeling is needed, where each label of the image should be in seperate **.txt** file: <br>
**class_id x_center y_center width height**
1. class_id — integer representing the object class (starts from 0).
2. x_center — x-coordinate of the bounding box center (normalized).
3. y_center — y-coordinate of the bounding box center (normalized).
4. width — width of the bounding box (normalized).
5. height — height of the bounding box (normalized).

There were three main open source datasets used in this project, here are the links for accessing and downloading those datasets:
1. https://datasetninja.com/road-pothole-images
2. https://www.kaggle.com/datasets/tallwinkingstan/road-traversing-knowledge-rtk-dataset
3. https://figshare.com/articles/figure/Potholes_dataset_with_YOLO_annotations/21214400/3?file=37622126

1. For the first dataset from datasetsninja.com we will need to proceed with kaggle and access the shared google drive. There will be 4 main subfolders, where one will need to choose for specific task and memory. They are all similar and have many common images, for this specific project Dataset 1 (Simplex) was used. Folder contains Train and Test sets with it's proper annotations (however in COCO format used for COCO dataset). As the annotation labels are all given in one file and we have different labeling format other then YOLO format, some preprocessing will be needed alng with data splitting (train, test, validation). All this processed can be found in **data_annotation_converter.ipynb**.
2. For the second dataset (RTK dataset), only the subfolder AsphaltBad was used as the project aims to make detections for asphalted roads. Here, in this dataset we don't have any proper bounding box annotations, hence we will need to annotate it manually. For easy manual annotations refer to this tutorial which uses **cvat.ai** annotation tool: <br>
https://youtu.be/m9fH9OWn8YM?si=4NiwVybZUtrcjJOS&t=304
3. For the third dataset (figshare), the whole folder was downloaded. It contains subfolders of images of different day time and weather conditions. This is very useful as wide variety gives the opportunity to train a well generelized model. Here just refoldering and splitting into train validation. For second and third datasets processes use **data_converter.ipynb**.

**Sample images and labels from each of this datasets will be available in the repository for showcasing purposes.**

## Training and Testing
Training of the model can be done both in Google Colab environment and on local machine if CUDA enabled high performance GPU is available.

Notebooks for both cases are available in the google repository with their respective **.yaml** files. Adjust the parameters and hyperparameters for your specific need (epochs, augmentations, epochs, imgsz, etc.). Find the codes in:
**training_colab.ipynb** and **training_local.ipynb**.

During the project many models have been trained, including YOLO version 8 and YOLO version 11 (specifically these versions are well optimized for different platforms). Models were trained for 640x640 and 736x736 pixel sized images. One of the model versions will be available in the repository (with its ncnn converted version).

For predicting video or image refer to **predict_image.py** and **predict_video.py**.
Examples of inferenced images and videos can be found in **pothole_videos** and **pothole_images** folders. (or watch the video in YouTube)
https://www.youtube.com/watch?v=nSzvAnHtJfE

...

## Raspberry Pi Deployment
For deploying the model on Raspberry Pi, refer to the tutorial and it's article:
https://www.youtube.com/watch?v=XKIm_R_rIeQ&list=PLJ7aTi3ZNpXBdEvv3VlRk46Ei6cxeT_Il&index=17
https://core-electronics.com.au/guides/raspberry-pi/getting-started-with-yolo-object-and-animal-recognition-on-the-raspberry-pi/

Model can be deployed on any Raspberry Pi which has up to date OS installed, although Pi 5 is prefered for better inferencing speed (FPS).

...
