# train_controller_communicate.py

from PyQt6.QtCore import pyqtSignal, QObject

class TrainControllerCommunicate(QObject):

    # Train Controller -> Train Model
    power_command_signal = pyqtSignal(float)
    service_brake_command_signal = pyqtSignal(bool)
    emergency_brake_command_signal = pyqtSignal(bool)
    desired_temperature_signal = pyqtSignal(float)
    exterior_lights_signal = pyqtSignal(bool)  # 1 = On, 0 = Off
    interior_lights_signal = pyqtSignal(bool)  # 1 = On, 0 = Off
    left_door_signal = pyqtSignal(bool)        # 1 = Open, 0 = Closed
    right_door_signal = pyqtSignal(bool)       # 1 = Open, 0 = Closed
    announcement_signal = pyqtSignal(str)
    grade_signal = pyqtSignal(float)

    # Train Model -> Train Controller
    current_velocity_signal = pyqtSignal(float)
    commanded_speed_signal = pyqtSignal(int)
    commanded_authority_signal = pyqtSignal(int)
    engine_failure_signal = pyqtSignal(bool)
    brake_failure_signal = pyqtSignal(bool)
    signal_failure_signal = pyqtSignal(bool)
    passenger_brake_command_signal = pyqtSignal(bool)
    actual_temperature_signal = pyqtSignal(float)
    polarity_signal = pyqtSignal(bool)  # If flipped, then train has moved onto next block - NEW
    dispatch_train_signal = pyqtSignal(int)  # 1 = Dispatch, 0 = Do not dispatch
