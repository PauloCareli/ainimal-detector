import cv2

from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, result=None, model_path='yolov8n.pt'):
        if result:
            self.result = result
            self.x1, self.y1, self.x2, self.y2, self.score, self.class_id = result
        self.threshold = 0.5
        # self.model = YOLO("yolov8n.pt")  # pre trained by yolo
        self.model = YOLO(model_path)
        # self.class_dict = self.model.names

    def set_model(self, model):
        self.model = model

    def set_result(self, result):
        self.result = result
        self.x1, self.y1, self.x2, self.y2, self.score, self.class_id = result

    def set_image(self, image):
        self.image = image

    def set_threshold(self, threshold):
        self.threshold = threshold

    # def set_class_dict(self, class_dict):
    #     self.class_dict = class_dict

    def detect(self, image):
        # Run YOLO detection with our confidence threshold
        results = self.model(image, conf=self.threshold)[0]
        return results

    def process_results(self, image, results):
        self.set_image(image)
        for result in results.boxes.data.tolist():
            self.set_result(result)
            self.draw_bounding_box()
        return self.image

    def draw_bounding_box(self, image=None):
        if image:
            self.set_image(image)
        self.draw_rectangle()
        self.draw_text()

    def draw_rectangle(self):
        cv2.rectangle(self.image, (int(self.x1), int(self.y1)),
                      (int(self.x2), int(self.y2)), (0, 255, 0), 4)

    def draw_text(self):
        cv2.putText(
            self.image,
            self.model.names[int(self.class_id)].upper(),
            (int(self.x1), int(self.y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (0, 255, 0),
            3,
            cv2.LINE_AA
        )
