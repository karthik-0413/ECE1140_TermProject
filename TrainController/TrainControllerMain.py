# main.py
import sys
from PyQt6.QtWidgets import QApplication
from TrainControllerUI import TrainControllerUI
from TrainControllerEngineer import TrainEngineerUI
from TrainControllerTestBench import TrainControllerTestBenchUI
from TrainControllerCommunicateSignals import Communicate

def main():
    # Create a single QApplication instance
    app = QApplication(sys.argv)
    
    # Create instances of each UI window
    communicator = Communicate()
    ui1 = TrainControllerUI(communicator)
    # ui2 = TrainEngineerUI(communicator)
    ui3 = TrainControllerTestBenchUI(communicator)

    # Show each window
    ui1.show()
    # ui2.show()
    ui3.show()

    # Execute the single event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()