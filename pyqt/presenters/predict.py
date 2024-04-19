from PyQt5.QtGui import QPixmap, QImage
import os
import cv2

from predict_image import label_all_images


class PredictPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_folder_selected(self, folder_path):
        self.model.image_model.folder_path = folder_path
        folder_contents = self.load_folder_contents(folder_path)
        self.view.image_view.load_folder_contents(folder_contents)

    def predict(self, folder_path, model):
        print(folder_path)
        print(model)
        label_all_images(folder_path)
        pass

    # def find_content(self, folder_path):
        #     self.view.image_view.progress_bar.setVisible(True)

        #     folder_contents = []
        #     directories = os.listdir(folder_path)
        #     for file_index, file_name in enumerate(directories):
        #         self.view.image_view.update_progress_bar(
        #             file_index/(len(directories)-1))

        #         file_path = os.path.join(folder_path, file_name)

        #         # Check if the file is an image or video
        #         if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        #             pixmap = QPixmap(file_path)
        #         elif file_name.lower().endswith(('.mp4', '.avi', '.mkv')):
        #             pixmap = self.get_video_frame(file_path)
        #         else:
        #             continue  # Skip non-supported file types

        #         folder_contents.append(
        #             {"pixmap": pixmap, "name": file_name, "path": file_path})

        #     return folder_contents

        # def load_folder_contents(self, folder_path):
        #     self.view.image_view.progress_bar.setVisible(True)

        #     folder_contents = []
        #     directories = os.listdir(folder_path)
        #     for file_index, file_name in enumerate(directories):
        #         self.view.image_view.update_progress_bar(
        #             file_index/(len(directories)-1))

        #         file_path = os.path.join(folder_path, file_name)

        #         # Check if the file is an image or video
        #         if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        #             pixmap = QPixmap(file_path)
        #         elif file_name.lower().endswith(('.mp4', '.avi', '.mkv')):
        #             pixmap = self.get_video_frame(file_path)
        #         else:
        #             continue  # Skip non-supported file types

        #         folder_contents.append(
        #             {"pixmap": pixmap, "name": file_name, "path": file_path})

        #     return folder_contents

        # def get_video_frame(self, file_path):
        #     # Get the first frame of the video as a QPixmap
        #     cap = cv2.VideoCapture(file_path)
        #     ret, frame = cap.read()
        #     cap.release()

        #     if ret:
        #         height, width, channel = frame.shape
        #         bytes_per_line = 3 * width
        #         q_image = QImage(frame.data, width, height,
        #                          bytes_per_line, QImage.Format_RGB888)
        #         pixmap = QPixmap.fromImage(q_image.rgbSwapped())
        #         return pixmap
