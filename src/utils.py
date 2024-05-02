import random
import shutil
import os
from paths import CLASSES_FILE_PATH


def get_classes():
    with open(CLASSES_FILE_PATH, 'r') as f:
        classes = f.read().strip().split('\n')

    return classes


def get_classes_from_model(model):

    return model.names


def get_class_dict(by_name=False):
    if by_name:
        return {cls: idx for idx, cls in enumerate(get_classes())}

    return {idx: cls for idx, cls in enumerate(get_classes())}


def find_last_folder(folder_path):
    # Get a list of subdirectories in the specified folder
    subfolders = [f for f in os.listdir(
        folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    if not subfolders:
        print("No subfolders found.")
        return None

    # Extract numeric parts from each subfolder name and find the maximum
    max_number = 0
    last_folder = None

    for subfolder in subfolders:
        try:
            folder_number = int(subfolder.split("train")[-1])
            if folder_number > max_number:
                max_number = folder_number
                last_folder = subfolder
        except ValueError:
            pass  # Skip folders without a numeric part

    return last_folder


def split_and_move_data(main_folder_path, output_folder_path, split_ratio=0.2):
    # Define paths
    train_folder_path = os.path.join(main_folder_path, "train")
    images_folder_path = os.path.join(train_folder_path, "images")
    labels_folder_path = os.path.join(train_folder_path, "labels")

    output_train_folder_path = os.path.join(output_folder_path, "train")
    output_val_folder_path = os.path.join(output_folder_path, "val")

    output_images_train_path = os.path.join(output_train_folder_path, "images")
    output_labels_train_path = os.path.join(output_train_folder_path, "labels")

    output_images_val_path = os.path.join(output_val_folder_path, "images")
    output_labels_val_path = os.path.join(output_val_folder_path, "labels")

    # Create output folders
    os.makedirs(output_images_train_path, exist_ok=True)
    os.makedirs(output_labels_train_path, exist_ok=True)
    os.makedirs(output_images_val_path, exist_ok=True)
    os.makedirs(output_labels_val_path, exist_ok=True)

    # List all image files
    image_files = [f for f in os.listdir(
        images_folder_path) if f.endswith(".jpg")]

    # Shuffle the list of image files
    random.shuffle(image_files)

    # Calculate the number of files to move for validation
    num_val_files = int(split_ratio * len(image_files))

    # Move files to validation folder
    for img_file in image_files[:num_val_files]:
        img_path = os.path.join(images_folder_path, img_file)
        label_path = os.path.join(
            labels_folder_path, img_file.replace(".jpg", ".txt"))

        shutil.move(img_path, output_images_val_path)
        shutil.move(label_path, output_labels_val_path)

    # Move remaining files to training folder
    for img_file in image_files[num_val_files:]:
        img_path = os.path.join(images_folder_path, img_file)
        label_path = os.path.join(
            labels_folder_path, img_file.replace(".jpg", ".txt"))

        shutil.move(img_path, output_images_train_path)
        shutil.move(label_path, output_labels_train_path)


if __name__ == '__main__':
    # Example usage
    main_folder_path = 'datasets/OIDv4/OID/lu'
    output_folder_path = 'datasets/OIDv4/OID/lu/val'

    split_and_move_data(main_folder_path, output_folder_path)
