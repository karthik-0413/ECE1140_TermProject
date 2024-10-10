import sys
from PyQt6.QtWidgets import QApplication
from communicationSignals import Communicate
from frontend import CTC_Controller
from block_page import BP
from simulation_page import Simulate
from test_bench import TB

def main():
    # Create a single QApplication instance
    app = QApplication(sys.argv)
    
    # Create instances of each UI window
    communicator = Communicate()  # Replace with your actual communicator class
    ui1 = CTC_Controller(communicator)
    ui2 = BP(communicator)
    ui3 = Simulate(communicator)
    ui4 = TB(communicator)

    # Show each window
    ui1.show()
    ui2.show()
    ui3.show()
    ui4.show()

    # Execute the single event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()