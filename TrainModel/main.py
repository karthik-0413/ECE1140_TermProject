# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import Qt

# Import custom modules
from train_data import TrainData
from testbench import TestBenchPage
from murphy import MurphyPage
from train_model import TrainModelPage
from base_page import BasePage

# Communication classes
from train_controller_communicate import TrainControllerCommunicate
from track_model_communicate import TrackModelCommunicate
from CTC_communicate import CTCTrain


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Train Control Application")
        self.setGeometry(100, 100, 1200, 800)  # Adjusted window size

        # Create communication instances
        self.tc_communicate = TrainControllerCommunicate()
        self.tm_communicate = TrackModelCommunicate()
        self.ctc_communicate = CTCTrain()

        # Create TrainData instance
        self.train_data = TrainData(self.tc_communicate, self.tm_communicate, self.ctc_communicate)

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create pages
        self.testbench_page = TestBenchPage(self.train_data, self.train_id_changed)
        self.murphy_page = MurphyPage(self.train_data, self.tc_communicate, self.tm_communicate)
        self.train_model_page = TrainModelPage(self.train_data, self.tc_communicate, self.tm_communicate)

        # Add pages as tabs
        self.tabs.addTab(self.testbench_page, "Test Bench")
        self.tabs.addTab(self.murphy_page, "Murphy")
        self.tabs.addTab(self.train_model_page, "Train Model")

        # Update Train ID lists in all pages
        self.update_train_id_lists()

        # Connect data changed signal to update Train IDs when train count changes
        self.train_data.data_changed.connect(self.update_train_id_lists)

        # Emit initial train count (0 trains)
        self.ctc_communicate.current_train_count_signal.emit(0)

    def update_train_id_lists(self):
        """Update Train ID combo boxes in all pages when train count changes."""
        train_ids = [str(i + 1) for i in range(self.train_data.train_count)]
        self.testbench_page.update_train_id_list(train_ids)
        self.murphy_page.update_train_id_list(train_ids)
        self.train_model_page.update_train_id_list(train_ids)

    def train_id_changed(self, new_train_id):
        """Handle Train ID change (if needed)."""
        pass  # Implement if necessary


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
