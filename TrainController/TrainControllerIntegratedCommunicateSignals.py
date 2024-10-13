from PyQt6.QtCore import pyqtSignal, QObject

class IntegratedCommunicate(QObject):
    
    # Engineer Signals
    engineer_kp_signal = pyqtSignal(float)
    engineer_ki_signal = pyqtSignal(float)
    
    # Outputs to the Train Model
    power_command_signal = pyqtSignal(float)
    service_brake_command_signal = pyqtSignal(bool)
    emergency_brake_command_signal = pyqtSignal(bool)
    desired_temperature_signal = pyqtSignal(float)
    exterior_lights_signal = pyqtSignal(bool)
    interior_lights_signal = pyqtSignal(bool)
    left_door_signal = pyqtSignal(bool) # 1 = Open, 0 = Closed
    right_door_signal = pyqtSignal(bool)    # 1 = Open, 0 = Closed
    announcement_signal = pyqtSignal(str)
    station_name_signal = pyqtSignal(str)
    
    # Inputs from the Train Model
    current_velocity_signal = pyqtSignal(float)
    commanded_speed_signal = pyqtSignal(float)
    commanded_authority_signal = pyqtSignal(float)
    engine_failure_signal = pyqtSignal(bool)
    brake_failure_signal = pyqtSignal(bool)
    signal_failure_signal = pyqtSignal(bool)
    passenger_brake_command_signal = pyqtSignal(bool)
    actual_temperature_signal = pyqtSignal(float)   # NEW
    blocks_between_stations_signal = pyqtSignal(list)   # NEW
    enable_switch_status_signal = pyqtSignal(bool)   # NEW -> 1 = check for next switch status, 0 = ignore next switch status
    switch_status_signal = pyqtSignal(bool)   # NEW -> 1 = switch is right/down, 0 = switch is left/up