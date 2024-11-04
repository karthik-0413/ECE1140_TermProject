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
from CTC_communicate import CTCCommunicate  # Renamed file

class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Train Control Application")
        self.setGeometry(100, 100, 1200, 800)  # Adjusted window size

        # Create communication instances
        self.tc_communicate = TrainControllerCommunicate()
        self.tm_communicate = TrackModelCommunicate()
        self.ctc_communicate = CTCCommunicate()  # Updated class name

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

        # Connect CTC to update train counts (simulate receiving train counts)
        # For testing, let's simulate the CTC sending train counts
        self.simulate_ctc_train_counts()

    def simulate_ctc_train_counts(self):
        """Simulate CTC sending train counts at intervals."""
        from PyQt6.QtCore import QTimer

        self.train_counts = [1, 2, 3, 2, 1, 0]  # Example train counts
        self.ctc_timer = QTimer()
        self.ctc_timer.timeout.connect(self.send_next_train_count)
        self.ctc_timer.start(5000)  # Every 5 seconds

    def send_next_train_count(self):
        if self.train_counts:
            next_count = self.train_counts.pop(0)
            self.ctc_communicate.update_current_train_count(next_count)
        else:
            self.ctc_timer.stop()

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

    def update_train_id_lists(self):
        """Update Train ID combo boxes in all pages when train count changes."""
        train_ids = [str(i + 1) for i in range(self.train_data.train_count)]
        self.testbench_page.update_train_id_list(train_ids)
        self.murphy_page.update_train_id_list(train_ids)
        self.train_model_page.update_train_id_list(train_ids)
        self.test_bench_page.update_train_id_list(train_ids)
        self.murphy_page.update_train_id_list(train_ids)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
