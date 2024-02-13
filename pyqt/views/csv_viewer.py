from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QFileDialog, QWidget
from PyQt5.QtCore import Qt
import pandas as pd


class CSVView(QWidget):
    def __init__(self, view_instance):
        super().__init__()
        self.view_instance = view_instance
        self.window = view_instance.window

        # Set up the main window

        # Create a table widget and a layout for the central widget
        self.central_widget = QTableWidget(self)
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.central_widget)

        # Create "Open CSV" button and connect it to the load_csv method
        self.open_button = QPushButton("Open CSV", self)
        self.open_button.clicked.connect(self.load_csv)
        self.open_button.setFixedHeight(40)

        # Create "Close CSV" button and connect it to the close_csv method
        self.close_button = QPushButton("Close CSV", self)
        self.close_button.clicked.connect(self.close_csv)
        self.close_button.setFixedHeight(40)

        # Add buttons to the layout
        self.central_layout.addWidget(self.open_button)
        self.central_layout.addWidget(self.close_button)

        # Create a container widget to hold the layout
        # central_container = QWidget()
        # central_container.setLayout(self.central_layout)
        self.setLayout(self.central_layout)
        # self.setCentralWidget(central_container)

    def load_csv(self):
        # Open a file dialog to get the CSV file path
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        # Check if a file is selected
        if file_name:
            # Load the CSV data into the table using Pandas
            self.load_data(file_name)

    def close_csv(self):
        # Remove all rows and columns to close the CSV file
        self.central_widget.setRowCount(0)
        self.central_widget.setColumnCount(0)

    def load_data(self, file_name):
        self.close_csv()
        # Read CSV data using Pandas
        try:
            df = pd.read_csv(file_name)
        except pd.errors.EmptyDataError:
            print(file_name, " is empty")
            return

        # Set the number of rows and columns in the table
        self.central_widget.setRowCount(df.shape[0])
        self.central_widget.setColumnCount(df.shape[1])

        # Populate the table with data
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                self.central_widget.setItem(row, col, item)

        # Set accessibility properties
        self.central_widget.setFocusPolicy(Qt.StrongFocus)
        self.central_widget.setAccessibleName("CSV Data Table")
        self.central_widget.setAccessibleDescription(
            "Table displaying CSV data")

        self.open_button.setAccessibleName("Open CSV Button")
        self.open_button.setAccessibleDescription("Button to open a CSV file")

        self.close_button.setAccessibleName("Close CSV Button")
        self.close_button.setAccessibleDescription(
            "Button to close a CSV file")
