from PyQt6.QtCore import pyqtSignal, QObject

class TrainTrainController(QObject):
    
    # Train Controller -> Train Model
    power_command_signal = pyqtSignal(list)    # float,watts
    service_brake_command_signal = pyqtSignal(list) # bool
    emergency_brake_command_signal = pyqtSignal(list)   # bool
    desired_temperature_signal = pyqtSignal(list)  # float
    exterior_lights_signal = pyqtSignal(list)  # 1 = On, 0 = Off
    interior_lights_signal = pyqtSignal(list)  # 1 = On, 0 = Off
    left_door_signal = pyqtSignal(list)        # 1 = Open, 0 = Closed
    right_door_signal = pyqtSignal(list)       # 1 = Open, 0 = Closed
    announcement_signal = pyqtSignal(list)   # string
    
    # Train Model -> Train Controller
    current_velocity_signal = pyqtSignal(list) # float  km/h
    commanded_speed_signal = pyqtSignal(list) # int     km/h
    commanded_authority_signal = pyqtSignal(list)    # int         blocks
    engine_failure_signal = pyqtSignal(list)    # bool
    brake_failure_signal = pyqtSignal(list) # bool
    signal_failure_signal = pyqtSignal(list)    # bool
    passenger_brake_command_signal = pyqtSignal(list)   # bool
    actual_temperature_signal = pyqtSignal(list)   # float
    polarity_signal = pyqtSignal(list)                 # bool
    train_count_signal = pyqtSignal(int)  # Total number of trains