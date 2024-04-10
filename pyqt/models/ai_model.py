class AIModel:
    def __init__(self, name=None, path="", description="", accuracy=0.0, threshold=0.6):
        """
        Initialize an AIModel object with specified attributes.

        Parameters:
        name (str): Name of the AI model.
        path (str): File path or location of the AI model.
        description (str): Description or details about the AI model.
        accuracy (float): Accuracy or performance metric of the AI model.
        """
        self.name = name
        self.path = path
        self.description = description
        self.accuracy = accuracy
        self.model = None
        self.is_trained = True
        self.threshold = threshold

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
