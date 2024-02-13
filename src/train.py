from ultralytics import YOLO
import ultralytics
import torch
import torchvision
import sys

from utils import find_last_folder
MODEL = "yolov8n.yaml"
# MODEL = "yolov8x.yaml"  # Better accuracy, but takes longer to train and run
# MODEL = "last.pt"
TRAINED_MODELS_PATH = "./runs/detect/"
# Load a model
# print(torchvision.__version__) # this will tell if it's cpu or gpu
# ultralytics.checks()
# Use the model


def new_training():
    # model = YOLO("yolov8n.yaml")  # build a new model from scratch
    model = YOLO(MODEL)  # build a new model from scratch
    results = model.train(data="src/config.yaml",
                          patience=40,
                          epochs=100,
                          )  # train the model


def train_pretrained():
    last_folder = find_last_folder(TRAINED_MODELS_PATH)
    if last_folder:
        print(f"The last folder is: {last_folder}")
        model = YOLO(TRAINED_MODELS_PATH + last_folder + "/weights/best.pt")
        results = model.train(data="src/config.yaml",
                              patience=50,
                              epochs=100,
                              )  # train the model
        print(results)
    else:
        print("No valid folders found.")


def resume_training():
    # Find the last folder
    last_folder = find_last_folder(TRAINED_MODELS_PATH)
    if last_folder:
        print(f"The last folder is: {last_folder}")
        model = YOLO(TRAINED_MODELS_PATH + last_folder + "/weights/last.pt")
        model.train(resume=True)
    else:
        print("No valid folders found.")


if __name__ == '__main__':

    if "--resume" in sys.argv:
        resume_training()
        exit()

    if "--pretrained" in sys.argv:
        train_pretrained()
        exit()

    new_training()

# Resume train
