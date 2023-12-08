from ultralytics import YOLO
import ultralytics
import torch
import torchvision
# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
# print(torchvision.__version__) # this will tell if it's cpu or gpu
# ultralytics.checks()
# Use the model
if __name__ == '__main__':
    results = model.train(data="src/config.yaml",
                          epochs=100)  # train the model
