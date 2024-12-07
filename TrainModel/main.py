import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import Qt

# Import custom modules
from TrainModel.train_data import TrainData
from TrainModel.murphy import MurphyPage
from TrainModel.train_model import TrainModelPage
from TrainModel.base_page import BasePage

# Communication classes
# from TrainModel.train_controller_communicate import TrainControllerCommunicate
from Resources.TrainTrainControllerComm import TrainTrainController
from TrainModel.track_model_communicate import TrackModelCommunicate
from Resources.CTCTrain import CTCTrain
from TrainModel.CTC_communicate import CTC_Train_Model_Communicate

class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self, ctc_train_communicate: CTCTrain, tc_communicate: TrainTrainController, tm_communicate: TrackModelCommunicate):
        super().__init__()

        self.setWindowTitle("Train Control Application")
        self.setGeometry(100, 100, 1200, 800)  # Adjusted window size

        # Create communication instances
        self.tc_communicate = tc_communicate
        self.tm_communicate = tm_communicate
        self.ctc_communicate = ctc_train_communicate

        # Create TrainData instance
        self.train_data = TrainData(self.tc_communicate, self.tm_communicate, self.ctc_communicate)
        # # print("TrainData instance created")

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create pages
        self.murphy_page = MurphyPage(self.train_data, self.tc_communicate, self.tm_communicate)
        self.train_model_page = TrainModelPage(self.train_data, self.tc_communicate, self.tm_communicate)

        # Add pages as tabs
        self.tabs.addTab(self.murphy_page, "Murphy")
        self.tabs.addTab(self.train_model_page, "Train Model")

        # Update Train ID lists in all pages
        self.update_train_id_lists()

        # Connect data changed signal to update Train IDs when train count changes
        self.train_data.data_changed.connect(self.update_train_id_lists)
        
        

    def update_train_id_lists(self):
        """Update Train ID combo boxes in all pages when train count changes."""
        train_ids = [str(i + 1) for i in range(self.train_data.train_count)]
        self.murphy_page.update_train_id_list(train_ids)
        self.train_model_page.update_train_id_list(train_ids)

def main():
    app = QApplication(sys.argv)
    ctc_communicate = CTCTrain()
    tc_communicate = TrainTrainController()
    window = MainWindow(ctc_communicate, tc_communicate)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()