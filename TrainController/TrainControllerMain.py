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
    communicator = Communicate()  # Replace with your actual communicator class
    ui1 = TrainControllerUI(communicator)
    ui2 = TrainEngineerUI(communicator)
    ui3 = TrainControllerTestBenchUI(communicator)

    # Show each window
    ui1.show()
    ui2.show()
    ui3.show()

    # Execute the single event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
# DONE:
# Position can be found from current velocity * timestep (Accumulate Over Time) - DONE
# Current Velocity should only change from Test Bench and Brakes!! - DONE
# When brakes are pressed, then you make power = 0 and activate service brake - DONE
# Find out why pressing the brakes makes the authority stops working - DONE
# Make Brake Buttons diveted in the UI whenever it is pressed and make power command to 0 - DONE
# In lab, find out Kp and Ki correct values - DONE
# If above commanded velocity, then power = 0 and service brake is activated until current velocity is below commanded velocity - DONE
# Emergency is not automatic, it is manual (ALWAYS MANUAL) - DONE
# Fix commanded speed from Test Bench - DONE
# Make sure all unit conversion is good - DONE


# STILL NEED TO DO:

