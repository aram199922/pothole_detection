# Automated Pothole Detection for Road Monitoring

## Table of Contents
- [Introduction - Aim of The Project](#introduction)
- [Data Collection and Preprocessing](#data-preprocessing)
- [Training and Testing](#training)
- [Raspberry Pi Deployment](#raspberry-pi])

## Introduction - Aim of The Project
This project proposes an automated pothole detection system leveraging deep learning-based object detection models: YOLOv8 and YOLOv11, trained on a custom-annotated dataset. To ensure high inferencing speed and portability, the models are optimized for deployment on edge devices: Raspberry Pi 4 and 5. The system is designed for real-time inference from live dashcam video streams, enabling on go detection and localization of road potholes. Detected potholes are geotagged using a GPS module, providing precise location data for maintenance planning. This lightweight, low-latency solution demonstrates the potential of integrating modern computer vision in real life applications.

As any other well formulated detection problem the project will start from gathering and preprocessing data with wide variety of images. Then, move on to training and testing the model and for this specific project finishing with deployment on the edge device and testing the model on live video stream in that environment.

## Data Collection and Preprocessing
For YOLO models specific labeling is needed, where each label of the image should be in seperate .txt file:
<class_id> <x_center> <y_center> <width> <height>
1. class_id — integer representing the object class (starts from 0).
2. x_center — x-coordinate of the bounding box center (normalized).
3. y_center — y-coordinate of the bounding box center (normalized).
4. width — width of the bounding box (normalized).
5. height — height of the bounding box (normalized).

There were three main open source datasets used in this project, here are the links for accessing and downloading those datasets:
1. https://datasetninja.com/road-pothole-images
2. https://www.kaggle.com/datasets/tallwinkingstan/road-traversing-knowledge-rtk-dataset
3. https://figshare.com/articles/figure/Potholes_dataset_with_YOLO_annotations/21214400/3?file=37622126

1. For the first dataset from datasetsninja.com we will need to proceed with kaggle and access the shared google drive. There will be 4 main subfolders, where one will need to choose for specific task and memory. They are all similar and have many common images, for this specific project Dataset 1 (Simplex) was used. Folder contains Train and Test sets with it's proper annotations (however in COCO format used for COCO dataset). As the annotation labels are all given in one file and we have different labeling format other then YOLO format, some preprocessing will be needed alng with data splitting (train, test, validation). All this processed can be find in **data_annotation_converter.ipynb**
2. For the second dataset (RTK dataset), only the subfolder AsphaltBad was used as the project aims to make detections for asphalted roads. Here, in this dataset we don't have any proper bounding box annotations, hence we will need to annotate it manually. For easy manual annotations refer to this tutorial which uses **cvat.ai** annotation tool:
https://youtu.be/m9fH9OWn8YM?si=4NiwVybZUtrcjJOS&t=304
3. For the third dataset (figshare), the whole folder was downloaded. It contains subfolders of images of different day time and weather conditions. This is very useful as wide variety gives the opportunity to train a well generelized model. 


## Training and Testing
More info here...

## Raspberry Pi Deployment
Cool stuff...