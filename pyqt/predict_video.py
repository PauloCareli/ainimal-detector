import os
import time
from typing import Any, Dict, Optional

import cv2

from object_detector import ObjectDetector
from utils.csv_logger import DetectionCSVLogger


def label_video(name: str,
                folder_path: str,
                folder_path_output: str,
                detector: ObjectDetector = ObjectDetector(),
                csv_logger: Optional[DetectionCSVLogger] = None,
                progress_callback=None) -> Dict[str, Any]:
    """
    Process a single video and optionally log detections to CSV.

    Returns:
        Dict with processing results including detection data for CSV logging
    """
    video_path = folder_path.replace("\\", "/") + "/" + name
    video_path_out = folder_path_output.replace("\\", "/") + "/" + name

    # Ensure the output directory exists
    os.makedirs(folder_path_output, exist_ok=True)

    start_time = time.time()
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error reading video file: {video_path}")
        return {
            'success': False,
            'message': f'Error reading video file: {video_path}',
            'detections': [],
            'processing_time_ms': 0
        }

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path_out, fourcc, fps, (width, height))

    total_detections = 0
    frame_number = 0

    ret, frame = cap.read()

    while ret:
        frame_timestamp = frame_number / fps if fps > 0 else 0

        # Resize frame for detection (YOLO input size)
        original_frame = frame.copy()
        detection_frame = cv2.resize(frame, (640, 640))

        # Detect objects
        results = detector.detect(detection_frame)

        # Extract detection data for CSV logging
        frame_detections = []
        if results.boxes is not None and len(results.boxes) > 0:
            for box_data in results.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = box_data

                # Convert to original video coordinates
                x1_orig = (x1 / 640) * width
                y1_orig = (y1 / 640) * height
                x2_orig = (x2 / 640) * width
                y2_orig = (y2 / 640) * height

                # Calculate center and dimensions
                x_center = (x1_orig + x2_orig) / 2
                y_center = (y1_orig + y2_orig) / 2
                bbox_width = x2_orig - x1_orig
                bbox_height = y2_orig - y1_orig

                detection = {
                    'class': detector.model.names[int(class_id)],
                    'confidence': confidence,
                    'bbox': {
                        'x_center': x_center,
                        'y_center': y_center,
                        'width': bbox_width,
                        'height': bbox_height
                    }
                }
                frame_detections.append(detection)

        total_detections += len(frame_detections)

        # Log to CSV if logger is provided
        if csv_logger:
            csv_logger.log_detections(
                file_path=video_path,
                detections=frame_detections,
                frame_number=frame_number,
                frame_timestamp=frame_timestamp,
                image_dimensions=(width, height),
                processing_time_ms=0,  # Will be calculated per frame if needed
                model_version=getattr(detector.model, 'version', '1.0'),
                detection_threshold=detector.threshold
            )

        # We need to manually draw the bounding boxes on the original frame
        # because the detection results are from the 640x640 resized frame
        processed_frame = original_frame.copy()

        if results.boxes is not None and len(results.boxes) > 0:
            for box_data in results.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = box_data

                # Convert coordinates from 640x640 detection frame to original frame
                x1_orig = int((x1 / 640) * width)
                y1_orig = int((y1 / 640) * height)
                x2_orig = int((x2 / 640) * width)
                y2_orig = int((y2 / 640) * height)

                # Draw bounding box
                cv2.rectangle(processed_frame, (x1_orig, y1_orig),
                              (x2_orig, y2_orig), (0, 255, 0), 4)

                # Draw class label
                class_name = detector.model.names[int(class_id)].upper()
                cv2.putText(
                    processed_frame,
                    class_name,
                    (x1_orig, y1_orig - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.3,
                    (0, 255, 0),
                    3,
                    cv2.LINE_AA
                )

        out.write(processed_frame)

        # Update progress if callback provided
        if progress_callback:
            progress = (frame_number / frame_count) * 100
            progress_callback(
                progress, f"Processing frame {frame_number}/{frame_count}...")

        frame_number += 1
        ret, frame = cap.read()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    processing_time_ms = (time.time() - start_time) * 1000

    return {
        'success': True,
        'message': f'Video saved on {video_path_out}',
        'detections': total_detections,
        'processing_time_ms': processing_time_ms,
        'output_path': video_path_out,
        'frame_count': frame_count,
        'fps': fps
    }


def label_multiple_videos(names: list[str],
                          folder_path: str,
                          folder_path_output: str,
                          detector: ObjectDetector = ObjectDetector(),
                          csv_logger: Optional[DetectionCSVLogger] = None) -> None:
    for name in names:
        label_video(name=name,
                    folder_path=folder_path,
                    folder_path_output=folder_path_output,
                    detector=detector,
                    csv_logger=csv_logger)


def label_all_videos(folder_path: str,
                     folder_path_output: str,
                     detector: ObjectDetector = ObjectDetector(),
                     csv_logger: Optional[DetectionCSVLogger] = None,
                     progress_callback=None) -> Dict[str, Any]:
    """
    Process all videos in a folder and optionally log detections to CSV.

    Returns:
        Dict with summary of processing results
    """
    start_session_time = time.time()
    session_start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Extended video formats support
    video_names = [f for f in os.listdir(folder_path) if f.lower().endswith(
        ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.MP4'))]

    print(f'Found {len(video_names)} videos to process')

    total_detections = 0
    total_processing_time = 0
    total_frames = 0
    successful_files = 0
    failed_files = 0

    for index, name in enumerate(video_names):
        try:
            # Update progress if callback provided
            if progress_callback:
                progress = (index / len(video_names)) * 100
                progress_callback(progress, f"Processing video {name}...")

            result = label_video(
                name,
                folder_path=folder_path,
                folder_path_output=folder_path_output,
                detector=detector,
                csv_logger=csv_logger,
                progress_callback=progress_callback
            )

            if result['success']:
                successful_files += 1
                total_detections += result['detections']
                total_processing_time += result['processing_time_ms']
                total_frames += result.get('frame_count', 0)
            else:
                failed_files += 1
                print(f"Failed to process {name}: {result['message']}")

        except (cv2.error, IOError, ValueError) as e:
            failed_files += 1
            print(f"Error processing {name}: {e}")

    # Final progress update
    if progress_callback:
        progress_callback(100, "Video processing complete!")

    session_end_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    total_session_time = (time.time() - start_session_time) * 1000

    # Log session summary to CSV
    if csv_logger:
        csv_logger.log_session_summary(
            total_files_processed=len(video_names),
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
                'failed_files': failed_files,
                'total_frames_processed': total_frames
            }
        )

    return {
        'total_files': len(video_names),
        'successful_files': successful_files,
        'failed_files': failed_files,
        'total_detections': total_detections,
        'total_frames': total_frames,
        'total_processing_time_ms': total_session_time,
        'csv_paths': csv_logger.get_csv_paths() if csv_logger else None
    }
