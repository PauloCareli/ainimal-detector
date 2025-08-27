import os
import cv2
import time
from typing import Dict, Any, Optional, List

from object_detector import ObjectDetector
from utils.csv_logger import DetectionCSVLogger


def label_image(name: str,
                folder_path,
                folder_path_output="/output",
                detector: ObjectDetector = ObjectDetector(),
                csv_logger: Optional[DetectionCSVLogger] = None
                ) -> Dict[str, Any]:
    """
    Process a single image and optionally log detections to CSV.

    Returns:
        Dict with processing results including detection data for CSV logging
    """
    image_path = folder_path.replace("\\", "/") + "/" + name
    image_path_out = folder_path_output.replace("\\", "/") + "/" + name

    # Ensure the output directory exists (including subdirectories)
    output_dir = os.path.dirname(image_path_out)
    os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error reading image file: {image_path}")
        return {
            'success': False,
            'message': f'Error reading image file: {image_path}',
            'detections': [],
            'processing_time_ms': 0
        }

    original_img = img.copy()
    original_height, original_width = img.shape[:2]
    img = cv2.resize(img, (640, 640))  # Resize image to model input size

    # Detect objects
    results = detector.detect(img)

    # Extract detection data for CSV logging
    # Note: YOLO already filtered by threshold in detector.detect()
    detections = []
    if results.boxes is not None and len(results.boxes) > 0:
        for box_data in results.boxes.data.tolist():
            x1, y1, x2, y2, confidence, class_id = box_data

            # Convert to original image coordinates
            x1_orig = (x1 / 640) * original_width
            y1_orig = (y1 / 640) * original_height
            x2_orig = (x2 / 640) * original_width
            y2_orig = (y2 / 640) * original_height

            # Calculate center and dimensions
            x_center = (x1_orig + x2_orig) / 2
            y_center = (y1_orig + y2_orig) / 2
            width = x2_orig - x1_orig
            height = y2_orig - y1_orig

            detection = {
                'class': detector.model.names[int(class_id)],
                'confidence': confidence,
                'bbox': {
                    'x_center': x_center,
                    'y_center': y_center,
                    'width': width,
                    'height': height
                }
            }
            detections.append(detection)

    # Process and draw results
    img = detector.process_results(img, results)

    # Save processed image
    cv2.imwrite(image_path_out, img)

    processing_time_ms = (time.time() - start_time) * 1000

    # Log to CSV if logger is provided
    if csv_logger:
        csv_logger.log_detections(
            file_path=image_path,
            detections=detections,
            image_dimensions=(original_width, original_height),
            processing_time_ms=processing_time_ms,
            model_version=getattr(detector.model, 'version', '1.0'),
            detection_threshold=detector.threshold
        )

    cv2.destroyAllWindows()

    return {
        'success': True,
        'message': f'Image saved on {image_path_out}',
        'detections': detections,
        'processing_time_ms': processing_time_ms,
        'output_path': image_path_out
    }


def label_multiple_images(names: list[str],
                          folder_path,
                          folder_path_output="/output",
                          detector: ObjectDetector = ObjectDetector()) -> None:
    for name in names:
        label_image(name=name, detector=detector, folder_path=folder_path,
                    folder_path_output=folder_path_output)


def label_all_images(folder_path: str,
                     folder_path_output: str = "/output",
                     detector: ObjectDetector = ObjectDetector(),
                     csv_logger: Optional[DetectionCSVLogger] = None,
                     progress_callback=None,
                     file_list: Optional[List[str]] = None
                     ) -> Dict[str, Any]:
    """
    Process all images in a folder and optionally log detections to CSV.

    Returns:
        Dict with summary of processing results
    """
    start_session_time = time.time()
    session_start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Use provided file list or scan folder
    if file_list is not None:
        image_names = file_list
        print(f'Processing {len(image_names)} images from provided list')
    else:
        image_names = [f for f in os.listdir(folder_path) if f.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.gif', ".JPG"))]
        print(f'Found {len(image_names)} images to process')

    total_detections = 0
    total_processing_time = 0
    successful_files = 0
    failed_files = 0

    for index, name in enumerate(image_names):
        try:
            # Update progress if callback provided
            if progress_callback:
                # Pass the file index and filename to the callback
                progress_callback(index, name)

            result = label_image(
                name,
                detector=detector,
                folder_path=folder_path,
                folder_path_output=folder_path_output,
                csv_logger=csv_logger
            )

            if result['success']:
                successful_files += 1
                total_detections += len(result['detections'])
                total_processing_time += result['processing_time_ms']
            else:
                failed_files += 1
                print(f"Failed to process {name}: {result['message']}")

        except Exception as e:
            failed_files += 1
            print(f"Error processing {name}: {e}")

    session_end_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    total_session_time = (time.time() - start_session_time) * 1000

    # Log session summary to CSV
    if csv_logger:
        csv_logger.log_session_summary(
            total_files_processed=len(image_names),
            total_detections=total_detections,
            total_processing_time_ms=total_session_time,
            start_time=session_start_timestamp,
            end_time=session_end_timestamp,
            settings_used={
                'input_folder': folder_path,
                'media_output_path': folder_path_output,
                'report_output_path': csv_logger.output_directory if csv_logger else '',
                'model_threshold': detector.threshold,
                'successful_files': successful_files,
                'failed_files': failed_files
            }
        )

    return {
        'total_files': len(image_names),
        'successful_files': successful_files,
        'failed_files': failed_files,
        'total_detections': total_detections,
        'total_processing_time_ms': total_session_time,
        'csv_paths': csv_logger.get_csv_paths() if csv_logger else None
    }
