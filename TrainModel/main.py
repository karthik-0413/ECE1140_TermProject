# main.py

import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget
)
from PyQt6.QtCore import Qt

from train_model import TrainModelPage
from testbench import TestBenchPage
from murphy import MurphyPage
from train_data import TrainData
from train_controller_communicate import TrainControllerCommunicate
from track_model_communicate import TrackModelCommunicate
from CTC_communicate import CTCTrain


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Train Control Application")
        self.setGeometry(100, 100, 1200, 800)  # Adjusted window size

        # Create communication instances
        self.tc_communicate = TrainControllerCommunicate()
        self.tm_communicate = TrackModelCommunicate()
        self.ctc_communicate = CTCTrain()

        # Create TrainData instance
        self.train_data = TrainData(self.tc_communicate, self.tm_communicate, self.ctc_communicate)

        # Start periodic train state updates
        self.train_data.start_train_updates()

        # Central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top navigation layout
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(0)

        # Navigation buttons
        self.train_model_btn = QPushButton("Train Model")
        self.murphy_btn = QPushButton("Murphy")
        self.test_bench_btn = QPushButton("Test Bench")  # Moved to third position

        # Set fixed size and style for navigation buttons
        for btn in [self.train_model_btn, self.murphy_btn, self.test_bench_btn]:
            btn.setFixedSize(150, 50)
            btn.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: lightgray;
                    color: black;
                    border: 1px solid #ccc;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d3d3d3;
                }
            """)

        # Connect buttons to methods
        self.train_model_btn.clicked.connect(self.show_train_model)
        self.test_bench_btn.clicked.connect(self.show_test_bench)
        self.murphy_btn.clicked.connect(self.show_murphy)

        # Add navigation buttons to layout in new order
        nav_layout.addWidget(self.train_model_btn)
        nav_layout.addWidget(self.murphy_btn)
        nav_layout.addWidget(self.test_bench_btn)

        # Add navigation layout to main layout
        nav_container = QWidget()
        nav_container.setLayout(nav_layout)
        nav_container.setFixedHeight(50)
        main_layout.addWidget(nav_container, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()

        # Pages
        self.train_model_page = TrainModelPage(self.train_data, self.tc_communicate, self.tm_communicate)
        self.test_bench_page = TestBenchPage(self.train_data, self.tc_communicate, self.tm_communicate)
        self.murphy_page = MurphyPage(self.train_data, self.tc_communicate, self.tm_communicate)

        # Add pages to stacked widget in the new order
        self.stacked_widget.addWidget(self.train_model_page)  # Index 0
        self.stacked_widget.addWidget(self.murphy_page)       # Index 1
        self.stacked_widget.addWidget(self.test_bench_page)   # Index 2

        # Initially show Train Model page
        self.stacked_widget.setCurrentWidget(self.train_model_page)

        # Add stacked widget to main layout
        main_layout.addWidget(self.stacked_widget)

        # Set central widget
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect data_changed signal
        self.train_data.data_changed.connect(self.update_train_id_list)

        # Simulate initial train dispatch
        self.ctc_communicate.dispatch_train_signal.emit(self.train_data.train_count)

    def show_train_model(self):
        """Show the Train Model page."""
        self.train_model_page.update_display()
        self.stacked_widget.setCurrentWidget(self.train_model_page)

    def show_test_bench(self):
        """Show the Test Bench page."""
        self.test_bench_page.update_display()
        self.stacked_widget.setCurrentWidget(self.test_bench_page)

    def show_murphy(self):
        """Show the Murphy page."""
        self.murphy_page.update_display()
        self.stacked_widget.setCurrentWidget(self.murphy_page)

    def update_train_id_list(self):
        """Update the train ID list in the UI when train count changes."""
        train_ids = [str(i + 1) for i in range(self.train_data.train_count)]
        self.train_model_page.update_train_id_list(train_ids)
        self.test_bench_page.update_train_id_list(train_ids)
        self.murphy_page.update_train_id_list(train_ids)


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
