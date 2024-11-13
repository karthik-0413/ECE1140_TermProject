import sys
import time
from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition, Qt, QMutexLocker
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QSlider, QVBoxLayout

class StopwatchEngine(QThread):
    time_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.running = False
        self.on_hold = False
        self.elapsed_seconds = 0
        self.speed_factor = 1.0
        self.mutex = QMutex()
        self.pause_condition = QWaitCondition()

    def initiate(self):
        self.running = True
        self.on_hold = False
        self.start()

    def suspend(self):
        with QMutexLocker(self.mutex):
            self.on_hold = True

    def resume(self):
        with QMutexLocker(self.mutex):
            self.on_hold = False
            self.pause_condition.wakeAll()

    def set_speed(self, multiplier: float):
        self.speed_factor = multiplier

    def terminate(self):
        self.running = False
        self.quit()
        self.wait()
        
    def run(self):
        while self.running:
            with QMutexLocker(self.mutex):
                if self.on_hold:
                    self.pause_condition.wait(self.mutex)

            # Wait based on the modified speed factor
            time.sleep(1.0 / (self.speed_factor * 10))
            self.elapsed_seconds += 1
            # print(f"Elapsed time: {self.elapsed_seconds} seconds")
            self.time_updated.emit(self.elapsed_seconds)

class ClockDisplay(QWidget):
    def __init__(self, stopwatch: StopwatchEngine):
        super().__init__()
        self.stopwatch = stopwatch
        self.stopwatch.time_updated.connect(self.refresh_time)
        
        self.setWindowTitle("Clock Display")
        self.setStyleSheet("background-color: lightgray;")

        layout = QVBoxLayout()

        # Digital time display
        self.display_label = QLabel("00:00:00")
        layout.addWidget(self.display_label)

        # Speed control slider
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(0, 20)
        self.speed_slider.setValue(1)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.valueChanged.connect(self.adjust_speed)

        # Display for current speed
        self.speed_label = QLabel("1.0x")
        self.speed_label.setStyleSheet("color: black;")
        
        # Arrange slider and speed label
        slider_container = QVBoxLayout()
        slider_container.addWidget(self.speed_slider)
        slider_container.addWidget(self.speed_label)

        layout.addLayout(slider_container)
        self.setLayout(layout)

    def refresh_time(self, seconds_elapsed):
        hours = seconds_elapsed // 3600
        minutes = (seconds_elapsed % 3600) // 60
        seconds = seconds_elapsed % 60

        # Format time for display
        self.display_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.display_label.setStyleSheet("color: black;")

    def adjust_speed(self, multiplier: int):
        if multiplier == 0:
            self.stopwatch.suspend()
            self.speed_label.setText("Paused")
        else:
            self.stopwatch.resume()
            self.stopwatch.set_speed(multiplier)
            self.speed_label.setText(f"{multiplier:.1f}x")

# Example usage
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     engine = StopwatchEngine()
#     interface = ClockDisplay(engine)
#     engine.initiate()
#     interface.show()
#     sys.exit(app.exec())
