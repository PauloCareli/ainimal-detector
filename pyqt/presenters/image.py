from PyQt5.QtGui import QPixmap, QImage
import os
import cv2


class ImagePresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_folder_selected(self, folder_path):
        self.model.image_model.folder_path = folder_path
        folder_contents = self.load_folder_contents(folder_path)
        self.view.image_view.load_folder_contents(folder_contents)

    def load_folder_contents(self, folder_path):
        self.view.image_view.progress_bar.setVisible(True)

        folder_contents = []

        # Get all files (with optional recursion)
        all_files = []
        if self.model.settings_model.recursive_folder_search:
            # Recursive search through all subdirectories
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Store both the full path and relative path for display
                    relative_path = os.path.relpath(file_path, folder_path)
                    all_files.append((file_path, relative_path))
        else:
            # Only scan the immediate folder
            directories = os.listdir(folder_path)
            for file_name in directories:
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):  # Only include files, not directories
                    all_files.append((file_path, file_name))

        for file_index, (file_path, display_name) in enumerate(all_files):
            if len(all_files) > 1:  # Avoid division by zero
                self.view.image_view.update_progress_bar(
                    file_index/(len(all_files)-1))

            # Check if the file is an image or video
            if display_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                pixmap = QPixmap(file_path)
            elif display_name.lower().endswith(('.mp4', '.avi', '.mkv')):
                pixmap = self.get_video_frame(file_path)
            else:
                continue  # Skip non-supported file types

            folder_contents.append(
                {"pixmap": pixmap, "name": display_name, "path": file_path})

        return folder_contents

    def get_video_frame(self, file_path):
        # Get the first frame of the video as a QPixmap
        cap = cv2.VideoCapture(file_path)
        ret, frame = cap.read()
        cap.release()

        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height,
                             bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image.rgbSwapped())
            return pixmap
