import os
import cv2

from paths import LABELED_VIDEOS_DIR, VIDEOS_DIR
from object_detector import ObjectDetector


def label_video(name: str, detector: ObjectDetector = ObjectDetector()) -> None:
    video_path = os.path.join(VIDEOS_DIR, name)
    video_path_out = os.path.join(LABELED_VIDEOS_DIR,  name)

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    if not ret:
        print("Error reading video file.")
        exit()

    H, W, _ = frame.shape

    out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(
        *'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    detector = ObjectDetector()
    while ret:
        results = detector.detect(frame)
        frame = detector.process_results(frame, results)

        out.write(frame)
        ret, frame = cap.read()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return 'Video saved on ' + video_path_out


def label_multiple_videos(names: list[str]) -> None:
    detector = ObjectDetector()
    for name in names:
        label_video(name=name, detector=detector)


def label_all_videos(path: str = VIDEOS_DIR) -> None:
    detector = ObjectDetector()
    video_names = [f for f in os.listdir(path) if f.lower().endswith(
        ('.mp4', '.avi', '.mkv', '.mov', '.MP4'))]
    for name in video_names:
        label_video(name, detector=detector)


label_video(name='06070175.mp4')
# label_all_videos()
