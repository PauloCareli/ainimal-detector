import os
from object_detector import ObjectDetector

from predict_image import label_all_images
from predict_video import label_all_videos
from utils.csv_logger import DetectionCSVLogger


class PredictPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_folder_selected(self, folder_path):
        self.model.image_model.folder_path = folder_path
        # Delegate to image presenter for folder loading
        if hasattr(self.view, 'presenter') and hasattr(self.view.presenter, 'image_presenter'):
            folder_contents = self.view.presenter.image_presenter.load_folder_contents(
                folder_path)
            self.view.image_view.load_folder_contents(folder_contents)

    def predict(self, folder_path, model, progress_callback=None):
        """
        Run prediction on folder with optional CSV logging for both images and videos
        """
        detector = ObjectDetector(model_path=model.path)
        detector.set_threshold(self.model.settings_model.threshold)

        # Initialize CSV logger
        csv_output_path = getattr(
            self.model.settings_model, 'report_output_path', 'pyqt/reports')
        csv_logger = DetectionCSVLogger(
            output_directory=csv_output_path,
            model_name=model.name
        )

        # Define supported extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif',
                            '.bmp', '.JPG', '.tiff', '.webp')
        video_extensions = ('.mp4', '.avi', '.mkv', '.mov',
                            '.wmv', '.flv', '.webm', '.m4v', '.MP4')

        # Check what files are in the folder (with optional recursion)
        image_files = []
        video_files = []

        if self.model.settings_model.recursive_folder_search:
            # Recursive search through all subdirectories
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.relpath(
                        os.path.join(root, file), folder_path)
                    if file.lower().endswith(image_extensions):
                        image_files.append(file_path)
                    elif file.lower().endswith(video_extensions):
                        video_files.append(file_path)
        else:
            # Only scan the immediate folder
            all_files = os.listdir(folder_path)
            image_files = [
                f for f in all_files if f.lower().endswith(image_extensions)]
            video_files = [
                f for f in all_files if f.lower().endswith(video_extensions)]

        search_mode = "recursively" if self.model.settings_model.recursive_folder_search else "in current folder"
        print(
            f"Found {len(image_files)} images and {len(video_files)} videos to process {search_mode}")

        # Calculate total files
        total_files = len(image_files) + len(video_files)
        completed_files = 0

        combined_results = {
            'total_files': 0,
            'successful_files': 0,
            'failed_files': 0,
            'total_detections': 0,
            'total_processing_time_ms': 0,
            'csv_paths': None,
            'image_results': None,
            'video_results': None
        }

        # Process images if any exist
        if image_files:
            if progress_callback:
                search_info = " (recursive)" if self.model.settings_model.recursive_folder_search else ""
                progress_callback(
                    0, f"Starting image processing ({len(image_files)} of {total_files} files{search_info})...")

            # Create a custom progress callback for images that tracks overall progress
            def image_progress_wrapper(file_index, message):
                # file_index is 0-based index within images
                files_completed_so_far = completed_files + file_index + 1
                overall_progress = (files_completed_so_far / total_files) * 100
                file_num = file_index + 1
                progress_callback(
                    overall_progress, f"Image {file_num}/{len(image_files)} (File {files_completed_so_far}/{total_files}): {message}")

            image_results = label_all_images(
                folder_path=folder_path,
                folder_path_output=self.model.settings_model.media_output_path,
                detector=detector,
                csv_logger=csv_logger,
                progress_callback=image_progress_wrapper if progress_callback else None,
                file_list=image_files
            )
            combined_results['image_results'] = image_results
            combined_results['total_files'] += image_results['total_files']
            combined_results['successful_files'] += image_results['successful_files']
            combined_results['failed_files'] += image_results['failed_files']
            combined_results['total_detections'] += image_results['total_detections']
            combined_results['total_processing_time_ms'] += image_results['total_processing_time_ms']
            completed_files += len(image_files)

        # Process videos if any exist
        if video_files:
            if progress_callback:
                overall_progress = (completed_files / total_files) * 100
                search_info = " (recursive)" if self.model.settings_model.recursive_folder_search else ""
                progress_callback(overall_progress,
                                  f"Starting video processing ({len(video_files)} of {total_files} files{search_info})...")

            # Create a custom progress callback for videos that tracks overall progress
            def video_progress_wrapper(file_index, message):
                # file_index is 0-based index within videos
                files_completed_so_far = completed_files + file_index + 1
                overall_progress = (files_completed_so_far / total_files) * 100
                file_num = file_index + 1
                progress_callback(
                    overall_progress, f"Video {file_num}/{len(video_files)} (File {files_completed_so_far}/{total_files}): {message}")

            video_results = label_all_videos(
                folder_path=folder_path,
                folder_path_output=self.model.settings_model.media_output_path,
                detector=detector,
                csv_logger=csv_logger,
                progress_callback=video_progress_wrapper if progress_callback else None,
                file_list=video_files
            )
            combined_results['video_results'] = video_results
            combined_results['total_files'] += video_results['total_files']
            combined_results['successful_files'] += video_results['successful_files']
            combined_results['failed_files'] += video_results['failed_files']
            combined_results['total_detections'] += video_results['total_detections']
            combined_results['total_processing_time_ms'] += video_results['total_processing_time_ms']

        # Get CSV paths from the logger
        combined_results['csv_paths'] = csv_logger.get_csv_paths(
        ) if csv_logger else None

        # Final progress update
        if progress_callback:
            progress_callback(
                100, f"Processing complete! {total_files} files processed.")

        return {
            'output_path': self.model.settings_model.media_output_path,
            'csv_paths': combined_results['csv_paths'],
            'summary': combined_results
        }
