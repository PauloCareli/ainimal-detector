class AIModel:
    def __init__(self, name=None, path="", description="", accuracy=0.0, threshold=0.6,
                 model_type=None, version=None, training_date=None, map_50=None,
                 training_images=None, classes=None, input_size=None,
                 supported_formats=None, optimal_conditions=None,
                 training_dataset=None, performance_notes=None):
        """
        Initialize an AIModel object with specified attributes.

        Parameters:
        name (str): Name of the AI model.
        path (str): File path or location of the AI model.
        description (str): Description or details about the AI model.
        accuracy (float): Accuracy or performance metric of the AI model.
        threshold (float): Detection threshold of the AI model.
        model_type (str): Type of the model (e.g., YOLOv8 Custom).
        version (str): Version of the model.
        training_date (str): Date when the model was trained.
        map_50 (float): Mean Average Precision at IoU=0.5.
        training_images (int): Number of training images used.
        classes (list): List of detectable classes.
        input_size (str): Input image size (e.g., "640x640").
        supported_formats (list): List of supported file formats.
        optimal_conditions (str): Optimal usage conditions.
        training_dataset (str): Description of training dataset.
        performance_notes (str): Additional performance notes.
        """
        self.name = name
        self.path = path
        self.description = description
        self.accuracy = accuracy
        self.model = None
        self.is_trained = True
        self.threshold = threshold
        self.model_type = model_type
        self.version = version
        self.training_date = training_date
        self.map_50 = map_50
        self.training_images = training_images
        self.classes = classes or []
        self.input_size = input_size
        self.supported_formats = supported_formats or []
        self.optimal_conditions = optimal_conditions
        self.training_dataset = training_dataset
        self.performance_notes = performance_notes

    def set_name(self, name):
        """Set the name of the AI model."""
        self.name = name

    def set_path(self, path):
        """Set the file path or location of the AI model."""
        self.path = path

    def set_description(self, description):
        """Set the description or details about the AI model."""
        self.description = description

    def set_accuracy(self, accuracy):
        """Set the accuracy or performance metric of the AI model."""
        self.accuracy = accuracy

    def set_threshold(self, threshold):
        """Set the threshold or performance metric of the AI model."""
        self.threshold = threshold
