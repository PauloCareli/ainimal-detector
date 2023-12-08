from paths import CLASSES_FILE_PATH


def get_classes():
    with open(CLASSES_FILE_PATH, 'r') as f:
        classes = f.read().strip().split('\n')

    return classes


def get_class_dict(by_name=False):
    if by_name:
        return {cls: idx for idx, cls in enumerate(get_classes())}

    return {idx: cls for idx, cls in enumerate(get_classes())}
