import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import QTimer, QElapsedTimer
from test2 import calculate_speed

class TrainControllerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.elapsed_timer = QElapsedTimer()

    def initUI(self):
        self.setWindowTitle('Train Controller')

        # Speed Display
        self.speed_label = QLabel('Speed (mph):')
        self.speed_display = QLabel('40')
        self.brake_button = QPushButton('Apply Brake')
        self.brake_button.pressed.connect(self.start_braking)
        self.brake_button.released.connect(self.stop_braking)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.speed_label)
        layout.addWidget(self.speed_display)
        layout.addWidget(self.brake_button)
        self.setLayout(layout)

        # Initial conditions
        self.initial_speed = 40  # Initial speed in mph
        self.deceleration = -1 * 7.6  # Deceleration in m/s^2 (1 mph/s converted to m/s^2)
        self.current_speed = self.initial_speed  # Current speed in mph

    def start_braking(self):
        self.elapsed_timer.start()
        self.timer.start(100)  # Update every 100 ms

    def stop_braking(self):
        self.timer.stop()
        # Update initial speed to the current speed for the next braking session
        self.initial_speed = self.current_speed

    def update_speed(self):
        elapsed_time = self.elapsed_timer.elapsed() / 1000  # Convert ms to seconds
        new_speed = calculate_speed(self.initial_speed * 0.44704, self.deceleration, elapsed_time) / 0.44704  # Convert m/s to mph
        self.current_speed = new_speed
        self.speed_display.setText(f'{new_speed:.2f}')
        if new_speed <= 0:
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrainControllerUI()
    ex.show()
    sys.exit(app.exec())
