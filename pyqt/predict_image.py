import os
import cv2

from object_detector import ObjectDetector


def label_image(name: str,
                folder_path,
                folder_path_output="/output",
                detector: ObjectDetector = ObjectDetector()
                ) -> None:
    image_path = os.path.join(folder_path, name)
    image_path_out = os.path.join(folder_path_output, name)

    # Ensure the output directory exists
    os.makedirs(folder_path_output, exist_ok=True)

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


def label_multiple_images(names: list[str],
                          folder_path,
                          folder_path_output="/output",
                          detector: ObjectDetector = ObjectDetector()) -> None:
    for name in names:
        label_image(name=name, detector=detector, folder_path=folder_path,
                    folder_path_output=folder_path_output)


def label_all_images(folder_path: str,
                     folder_path_output: str = "/output",
                     detector: ObjectDetector = ObjectDetector()
                     ) -> None:

    image_names = [f for f in os.listdir(folder_path) if f.lower().endswith(
        ('.png', '.jpg', '.jpeg', '.gif', ".JPG"))]
    print('foundimages')
    for name in image_names:
        label_image(name, detector=detector,  folder_path=folder_path,
                    folder_path_output=folder_path_output)


if __name__ == "__main__":
    # label_image(name='jaguar3.jpg')
    label_all_images()
