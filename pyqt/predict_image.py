import os
import cv2

from paths import IMAGES_DIR, LABELED_IMAGES_DIR
from object_detector import ObjectDetector


def label_image(name: str, detector: ObjectDetector = ObjectDetector()) -> None:
    image_path = os.path.join(IMAGES_DIR, name)
    image_path_out = os.path.join(LABELED_IMAGES_DIR, name)

    # Ensure the output directory exists
    os.makedirs(LABELED_IMAGES_DIR, exist_ok=True)

    img = cv2.imread(image_path)

    if img is None:
        print("Error reading image file.")
        exit()

    img = cv2.resize(img, (640, 640))  # Resize image to model input size

    results = detector.detect(img)
    img = detector.process_results(img, results)

    cv2.imwrite(image_path_out, img)
    cv2.destroyAllWindows()

    return 'Image saved on ' + image_path_out


def label_multiple_images(names: list[str]) -> None:
    detector = ObjectDetector()
    for name in names:
        label_image(name=name, detector=detector)


def label_all_images(path: str = IMAGES_DIR) -> None:
    detector = ObjectDetector()
    image_names = [f for f in os.listdir(path) if f.lower().endswith(
        ('.png', '.jpg', '.jpeg', '.gif', ".JPG"))]
    for name in image_names:
        label_image(name, detector=detector)


if __name__ == "__main__":
    # label_image(name='jaguar3.jpg')
    label_all_images()
