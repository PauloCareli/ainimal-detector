import csv
import os
import datetime
from typing import List, Dict, Any, Optional


class DetectionCSVLogger:
    """
    CSV logger for YOLO detection results.
    Handles logging detection data for both images and videos with comprehensive metadata.
    """

    def __init__(self, output_directory: str, model_name: str = "Unknown"):
        """
        Initialize the CSV logger.

        Args:
            output_directory (str): Directory where CSV file will be saved
            model_name (str): Name of the AI model used for detection
        """
        self.output_directory = output_directory
        self.model_name = model_name

        # Generate filenames for both detection and summary files
        self.csv_filename = self._generate_csv_filename("detections")
        self.csv_path = output_directory.replace(
            "\\", "/") + "/" + self.csv_filename

        self.summary_filename = self._generate_csv_filename("summary")
        self.summary_path = output_directory.replace(
            "\\", "/") + "/" + self.summary_filename

        self.headers = [
            'detection_id',
            'session_id',
            'timestamp',
            'file_name',
            'file_path',
            'file_type',
            'frame_number',
            'frame_timestamp',
            'detection_class',
            'confidence',
            'bbox_x_center',
            'bbox_y_center',
            'bbox_width',
            'bbox_height',
            'bbox_x_min',
            'bbox_y_min',
            'bbox_x_max',
            'bbox_y_max',
            'image_width',
            'image_height',
            'model_name',
            'model_version',
            'detection_threshold',
            'processing_time_ms',
            'additional_metadata'
        ]
        self.session_id = self._generate_session_id()
        self.detection_counter = 0
        self._ensure_directory_exists()
        self._initialize_csv()
        self._initialize_summary_csv()

    def _generate_csv_filename(self, file_type: str = "detections") -> str:
        """Generate a unique CSV filename with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_model_name = "".join(
            c for c in self.model_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_model_name = safe_model_name.replace(' ', '_')
        return f"{file_type}_{safe_model_name}_{timestamp}.csv"

    def _generate_session_id(self) -> str:
        """Generate a unique session ID for this prediction run."""
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

    def _ensure_directory_exists(self):
        """Ensure the output directory exists."""
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory, exist_ok=True)

    def _initialize_csv(self):
        """Initialize the CSV file with headers."""
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.headers)
            print(f"Detection CSV logger initialized: {self.csv_path}")
        except Exception as e:
            print(f"Error initializing detection CSV file: {e}")

    def _initialize_summary_csv(self):
        """Initialize the summary CSV file with headers."""
        summary_headers = [
            'session_id',
            'start_time',
            'end_time',
            'model_name',
            'model_version',
            'total_files_processed',
            'successful_files',
            'failed_files',
            'total_detections',
            'total_processing_time_ms',
            'input_folder',
            'media_output_path',
            'report_output_path',
            'detection_threshold',
            'settings_used'
        ]
        try:
            with open(self.summary_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(summary_headers)
            print(f"Summary CSV logger initialized: {self.summary_path}")
        except Exception as e:
            print(f"Error initializing summary CSV file: {e}")

    def log_detections(self,
                       file_path: str,
                       detections: List[Dict[str, Any]],
                       frame_number: Optional[int] = None,
                       frame_timestamp: Optional[float] = None,
                       image_dimensions: Optional[tuple] = None,
                       processing_time_ms: Optional[float] = None,
                       model_version: str = "1.0",
                       detection_threshold: float = 0.5,
                       additional_metadata: str = ""):
        """
        Log detection results to CSV.

        Args:
            file_path (str): Path to the processed file
            detections (List[Dict]): List of detection results
            frame_number (int, optional): Frame number for video files
            frame_timestamp (float, optional): Timestamp within video
            image_dimensions (tuple, optional): (width, height) of the image/frame
            processing_time_ms (float, optional): Processing time in milliseconds
            model_version (str): Version of the model used
            detection_threshold (float): Detection confidence threshold used
            additional_metadata (str): Any additional metadata
        """
        try:
            current_timestamp = datetime.datetime.now().isoformat()
            file_name = os.path.basename(file_path)
            file_type = self._get_file_type(file_path)
            img_width, img_height = image_dimensions if image_dimensions else (
                0, 0)

            rows_to_write = []

            # If no detections, log one row indicating no detections
            if not detections:
                self.detection_counter += 1
                row = [
                    self.detection_counter,
                    self.session_id,
                    current_timestamp,
                    file_name,
                    file_path,
                    file_type,
                    frame_number if frame_number is not None else "",
                    frame_timestamp if frame_timestamp is not None else "",
                    "NO_DETECTION",
                    0.0,
                    "", "", "", "",  # bbox coordinates
                    "", "", "", "",  # bbox coordinates
                    img_width,
                    img_height,
                    self.model_name,
                    model_version,
                    detection_threshold,
                    processing_time_ms if processing_time_ms is not None else "",
                    additional_metadata
                ]
                rows_to_write.append(row)
            else:
                # Log each detection
                for detection in detections:
                    self.detection_counter += 1

                    # Extract detection data
                    class_name = detection.get('class', 'Unknown')
                    confidence = detection.get('confidence', 0.0)
                    bbox = detection.get('bbox', {})

                    # Handle different bbox formats
                    if isinstance(bbox, dict):
                        x_center = bbox.get('x_center', 0)
                        y_center = bbox.get('y_center', 0)
                        width = bbox.get('width', 0)
                        height = bbox.get('height', 0)
                    elif isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                        # Assume format: [x_min, y_min, x_max, y_max] or [x_center, y_center, width, height]
                        if 'x_min' in str(detection).lower() or len(bbox) == 4:
                            x_min, y_min, x_max, y_max = bbox[:4]
                            x_center = (x_min + x_max) / 2
                            y_center = (y_min + y_max) / 2
                            width = x_max - x_min
                            height = y_max - y_min
                        else:
                            x_center, y_center, width, height = bbox[:4]
                    else:
                        x_center = y_center = width = height = 0

                    # Calculate bounding box coordinates
                    x_min = x_center - width / 2
                    y_min = y_center - height / 2
                    x_max = x_center + width / 2
                    y_max = y_center + height / 2

                    row = [
                        self.detection_counter,
                        self.session_id,
                        current_timestamp,
                        file_name,
                        file_path,
                        file_type,
                        frame_number if frame_number is not None else "",
                        frame_timestamp if frame_timestamp is not None else "",
                        class_name,
                        round(confidence, 4),
                        round(x_center, 2),
                        round(y_center, 2),
                        round(width, 2),
                        round(height, 2),
                        round(x_min, 2),
                        round(y_min, 2),
                        round(x_max, 2),
                        round(y_max, 2),
                        img_width,
                        img_height,
                        self.model_name,
                        model_version,
                        detection_threshold,
                        processing_time_ms if processing_time_ms is not None else "",
                        additional_metadata
                    ]
                    rows_to_write.append(row)

            # Write all rows to CSV
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for row in rows_to_write:
                    writer.writerow(row)

        except Exception as e:
            print(f"Error logging detections to CSV: {e}")

    def _get_file_type(self, file_path: str) -> str:
        """Determine if file is image or video based on extension."""
        video_extensions = {'.mp4', '.avi', '.mov',
                            '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        image_extensions = {'.jpg', '.jpeg', '.png',
                            '.bmp', '.tiff', '.tif', '.webp'}

        ext = os.path.splitext(file_path)[1].lower()

        if ext in video_extensions:
            return "video"
        elif ext in image_extensions:
            return "image"
        else:
            return "unknown"

    def log_session_summary(self,
                            total_files_processed: int,
                            total_detections: int,
                            total_processing_time_ms: float,
                            start_time: str,
                            end_time: str,
                            settings_used: Dict[str, Any] = None):
        """
        Log a summary of the detection session to separate summary CSV.

        Args:
            total_files_processed (int): Number of files processed
            total_detections (int): Total number of detections made
            total_processing_time_ms (float): Total processing time
            start_time (str): Session start time
            end_time (str): Session end time
            settings_used (dict, optional): Settings used for this session
        """
        try:
            # Extract specific settings for structured logging
            input_folder = settings_used.get(
                'input_folder', '') if settings_used else ''
            media_output_path = settings_used.get(
                'media_output_path', '') if settings_used else ''
            report_output_path = settings_used.get(
                'report_output_path', '') if settings_used else ''
            detection_threshold = settings_used.get(
                'model_threshold', '') if settings_used else ''
            successful_files = settings_used.get(
                'successful_files', '') if settings_used else ''
            failed_files = settings_used.get(
                'failed_files', '') if settings_used else ''

            summary_row = [
                self.session_id,
                start_time,
                end_time,
                self.model_name,
                "1.0",  # model_version - could be extracted from model if available
                total_files_processed,
                successful_files,
                failed_files,
                total_detections,
                round(total_processing_time_ms, 2),
                input_folder,
                media_output_path,
                report_output_path,
                detection_threshold,
                str(settings_used) if settings_used else 'Default'
            ]

            with open(self.summary_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(summary_row)

            print(f"Session summary logged to: {self.summary_path}")

        except Exception as e:
            print(f"Error logging session summary: {e}")

    def get_csv_path(self) -> str:
        """Get the full path to the detection CSV file."""
        return self.csv_path

    def get_summary_path(self) -> str:
        """Get the full path to the summary CSV file."""
        return self.summary_path

    def get_csv_paths(self) -> Dict[str, str]:
        """Get both CSV file paths."""
        return {
            'detections': self.csv_path,
            'summary': self.summary_path
        }

    def get_detection_count(self) -> int:
        """Get the current detection counter."""
        return self.detection_counter
