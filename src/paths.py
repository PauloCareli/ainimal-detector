import os


CLASSES_FILE_PATH = 'src/classes.csv'

VIDEOS_DIR = os.path.join('.', 'videos')
LABELED_VIDEOS_DIR = os.path.join('.', 'videos', 'labeled')
IMAGES_DIR = os.path.join('.', 'images')
LABELED_IMAGES_DIR = os.path.join('.', 'images', 'labeled')

# MODEL_PATH = os.path.join('.', 'runs', 'detect',
#                           'train35', 'weights', 'last.pt')
# MODEL_PATH = "runs/detect/train47/weights/best.pt"
# MODEL_PATH = "runs/detect/train56/weights/best.pt"  # big model with wildlife cam
MODEL_PATH = "runs/detect/train57/weights/best.pt"  # small model with wildlife cam
