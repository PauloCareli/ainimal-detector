import os
from tqdm import tqdm
from PIL import Image
import shutil

from utils import get_class_dict, get_classes


def convert_coordinates(width, height, x_min, y_min, x_max, y_max):
    x_center = (x_min + x_max) / 2 / width
    y_center = (y_min + y_max) / 2 / height
    box_width = (x_max - x_min) / width
    box_height = (y_max - y_min) / height

    return x_center, y_center, box_width, box_height


def convert_oid_to_yolo(input_path, output_path, images_path, output_img_path):
    class_dict = get_class_dict(by_name=True)
    print(class_dict)
    for root, dirs, files in os.walk(input_path):
        for file in tqdm(files):
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r') as f:
                    lines = f.readlines()
                print(lines)
                image_path = os.path.join(
                    images_path, file.replace('.txt', '.jpg'))
                shutil.copy(image_path, os.path.join(
                    output_img_path, file.replace('.txt', '.jpg')))
                image = Image.open(image_path)
                width, height = image.size

                output_lines = []

                for line in lines:
                    parts = line.strip().split()
                    class_name, x_min, y_min, x_max, y_max = parts

                    class_id = class_dict[class_name.lower()]
                    x_center, y_center, box_width, box_height = convert_coordinates(
                        width, height, float(x_min), float(
                            y_min), float(x_max), float(y_max)
                    )

                    yolo_line = f"{class_id} {x_center} {y_center} {box_width} {box_height}\n"
                    output_lines.append(yolo_line)

                with open(os.path.join(output_path, file), 'w') as f:
                    f.writelines(output_lines)


# Replace these paths with your actual paths
# input_path = 'datasets/OIDv4/OID/All images/type/all labels'

input_path = 'OID/Dataset/{type}/{class}/Label'
images_path = 'OID/Dataset/{type}/{class}/'
output_img_path = 'datasets/OIDv4/OID/Dataset/{type}/images/'
output_path = 'datasets/OIDv4/OID/Dataset/{type}/labels'

# images_path = 'datasets/OIDv4/OID/All images/Train/all images'
# output_path = 'datasets/OIDv4/OID/Dataset/train/labels'


types = ["train", "validation", "test"]
types = ["validation", "test"]
for current_class in get_classes():
    for current_type in types:
        print(current_type)
        print(current_class)
        convert_oid_to_yolo(input_path.replace("{type}", current_type).replace("{class}", current_class.capitalize()),
                            output_path.replace("{type}", current_type.lower()).replace(
                                "{class}", current_class.capitalize()),
                            images_path.replace("{type}", current_type).replace(
                                "{class}", current_class.capitalize()),
                            output_img_path.replace("{type}", current_type)
                            )
