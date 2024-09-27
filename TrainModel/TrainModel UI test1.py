import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy, QSpacerItem, QGridLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class BasePage(QWidget):
    def __init__(self, title):
        super().__init__()

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to allow header to span full width
        main_layout.setSpacing(0)  # Remove spacing between header and content

        # Header
        header = QLabel(title)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont('Arial', 32, QFont.Weight.Bold))  # Large, bold font
        header.setStyleSheet("""
            background-color: lightblue;
            padding: 10px 0;  /* Reduced Top and Bottom padding */
        """)
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(header)

        # Content area
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        main_layout.addLayout(self.content_layout)

        self.setLayout(main_layout)

class MurphyPage(BasePage):
    def __init__(self, train_data):
        super().__init__("Murphy")
        self.train_data = train_data

        # Vertical layout with top spacer, failure sections, bottom spacer
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(0, 0, 0, 0)
        main_content_layout.setSpacing(0)

        # Top spacer to push failure sections to center
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_content_layout.addSpacerItem(top_spacer)

        # Container for failure sections
        failures_container = QWidget()
        failures_layout = QVBoxLayout()
        failures_layout.setContentsMargins(100, 0, 100, 0)  # Left and right padding
        failures_layout.setSpacing(30)  # Space between failure sections

        # Define failure types with ":" appended
        failure_types = ["Signal Pickup Failure:", "Train Engine Failure:", "Brake Failure:"]

        for failure in failure_types:
            failure_layout = QHBoxLayout()
            failure_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for consistency
            failure_layout.setSpacing(20)  # Space between label and button

            label = QLabel(failure)
            label.setFont(QFont('Arial', 18))  # Increased font size
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            button = QPushButton("Inactive")
            button.setCheckable(True)
            button.setFont(QFont('Arial', 14))  # Increased font size
            button.setFixedSize(140, 50)  # Increased button size
            button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:checked {
                    background-color: #8B0000;  /* Bloody red */
                }
            """)
            button.clicked.connect(lambda checked, btn=button: self.toggle_button(btn))

            failure_layout.addWidget(label)
            failure_layout.addWidget(button)

            failures_layout.addLayout(failure_layout)

        failures_container.setLayout(failures_layout)
        main_content_layout.addWidget(failures_container)

        # Bottom spacer to push failure sections to center
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_content_layout.addSpacerItem(bottom_spacer)

        # Add main content layout to content_layout
        self.content_layout.addLayout(main_content_layout)

    def toggle_button(self, button):
        if button.isChecked():
            button.setText("Active")
            # Set bloody red color
            button.setStyleSheet("""
                QPushButton {
                    background-color: #8B0000;
                    color: white;
                    border-radius: 5px;
                }
            """)
        else:
            button.setText("Inactive")
            button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    color: white;
                    border-radius: 5px;
                }
            """)

class TrainModelPage(BasePage):
    def __init__(self, train_data):
        super().__init__("Train Model")
        self.train_data = train_data  # Store the train data

        # Dictionaries to store value labels
        self.value_labels_form1 = {}  # To store value labels for form1
        self.value_labels_form2 = {}  # To store value labels for form2

        # Main content layout
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(50, 50, 50, 50)
        main_content_layout.setSpacing(30)

        # First form
        form1_widget = QWidget()
        form1_layout = QGridLayout()
        form1_layout.setSpacing(10)

        # Data items for form1
        data_items_form1 = [
            ("Cabin Temperature", "cabin_temperature", "°F"),
            ("Maximum Capacity", "maximum_capacity", "passengers"),
            ("Passenger Count", "passenger_count", ""),
            ("Crew Count", "crew_count", ""),
            ("Maximum Speed", "maximum_speed", "mph"),
            ("Current Speed", "current_speed", "mph"),
            ("Total Car Weight", "total_car_weight", "t"),
        ]

        # Create labels for form1
        for i, (label_text, var_name, unit) in enumerate(data_items_form1):
            label = QLabel(label_text)
            label.setFont(QFont('Arial', 16))
            value = getattr(self.train_data, var_name)
            value_text = f"{value} {unit}".strip()
            value_label = QLabel(value_text)
            value_label.setFont(QFont('Arial', 16))
            form1_layout.addWidget(label, i, 0)
            form1_layout.addWidget(value_label, i, 1)
            self.value_labels_form1[var_name] = value_label  # Store the value label

        form1_widget.setLayout(form1_layout)

        # Second form
        form2_widget = QWidget()
        form2_layout = QGridLayout()
        form2_layout.setSpacing(10)

        # Data items for form2
        data_items_form2 = [
            ("Train Length", "train_length", "m"),
            ("Train Height", "train_height", "m"),
            ("Train Width", "train_width", "m"),
            ("Number of Cars", "number_of_cars", ""),
            ("Single Car Tare Weight", "single_car_tare_weight", "t"),
        ]

        # Create labels for form2
        for i, (label_text, var_name, unit) in enumerate(data_items_form2):
            label = QLabel(label_text)
            label.setFont(QFont('Arial', 16))
            value = getattr(self.train_data, var_name)
            value_text = f"{value} {unit}".strip()
            value_label = QLabel(value_text)
            value_label.setFont(QFont('Arial', 16))
            form2_layout.addWidget(label, i, 0)
            form2_layout.addWidget(value_label, i, 1)
            self.value_labels_form2[var_name] = value_label  # Store the value label

        form2_widget.setLayout(form2_layout)

        # Add forms to main content layout
        main_content_layout.addWidget(form1_widget)
        # Add some spacing
        main_content_layout.addSpacing(30)
        main_content_layout.addWidget(form2_widget)

        # Add main content layout to the page
        self.content_layout.addLayout(main_content_layout)

class TestBenchPage(BasePage):
    def __init__(self, train_data):
        super().__init__("Test Bench")
        self.train_data = train_data
        # Currently blank as per instructions

class TrainData:
    def __init__(self):
        # Variables for the data values
        self.cabin_temperature = 78  # degrees Fahrenheit
        self.maximum_capacity = 222  # passengers
        self.passenger_count = 100
        self.crew_count = 2
        self.maximum_speed = 50  # mph
        self.current_speed = 40  # mph
        self.total_car_weight = 226.8  # tons

        self.train_length = 32.2  # meters
        self.train_height = 3.42  # meters
        self.train_width = 2.65  # meters
        self.number_of_cars = 4  # variable
        self.single_car_tare_weight = 40.9  # tons

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Application Example")
        self.setGeometry(100, 100, 900, 700)  # Set a reasonable window size

        # Create TrainData instance
        self.train_data = TrainData()

        # Central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to allow full-width header
        main_layout.setSpacing(0)  # Remove spacing between navigation and content

        # Top navigation layout
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(0)  # Remove spacing between buttons

        # Navigation buttons
        self.train_model_btn = QPushButton("Train Model")
        self.test_bench_btn = QPushButton("Test Bench")
        self.murphy_btn = QPushButton("Murphy")

        # Set fixed size and style for navigation buttons
        for btn in [self.train_model_btn, self.test_bench_btn, self.murphy_btn]:
            btn.setFixedSize(150, 50)  # Fixed button size for consistency
            btn.setFont(QFont('Arial', 12, QFont.Weight.Bold))  # Increased font size and bold
            btn.setStyleSheet("""
                QPushButton {
                    background-color: lightgray;
                    color: black;
                    border: 1px solid #ccc;
                }
                QPushButton:hover {
                    background-color: #d3d3d3;
                }
            """)

        # Connect buttons to methods
        self.train_model_btn.clicked.connect(self.show_train_model)
        self.test_bench_btn.clicked.connect(self.show_test_bench)
        self.murphy_btn.clicked.connect(self.show_murphy)

        # Add navigation buttons to layout without spacing
        nav_layout.addWidget(self.train_model_btn)
        nav_layout.addWidget(self.test_bench_btn)
        nav_layout.addWidget(self.murphy_btn)

        # Add navigation layout to main layout
        nav_container = QWidget()
        nav_container.setLayout(nav_layout)
        nav_container.setFixedHeight(50)  # Fixed height for navigation
        main_layout.addWidget(nav_container, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()

        # Pages
        self.train_model_page = TrainModelPage(self.train_data)
        self.test_bench_page = TestBenchPage(self.train_data)
        self.murphy_page = MurphyPage(self.train_data)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.train_model_page)
        self.stacked_widget.addWidget(self.test_bench_page)
        self.stacked_widget.addWidget(self.murphy_page)

        # Initially show Murphy page
        self.stacked_widget.setCurrentWidget(self.murphy_page)

        # Add stacked widget to main layout
        main_layout.addWidget(self.stacked_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_train_model(self):
        self.stacked_widget.setCurrentWidget(self.train_model_page)

    def show_test_bench(self):
        self.stacked_widget.setCurrentWidget(self.test_bench_page)

    def show_murphy(self):
        self.stacked_widget.setCurrentWidget(self.murphy_page)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
