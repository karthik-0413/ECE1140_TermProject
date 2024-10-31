import sys
import time
from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition, pyqtSlot, Qt, QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QSlider, QHBoxLayout

class TimerThread(QThread):
    second_passed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.active = False
        self.is_paused = False
        self.seconds_elapsed = 0
        self.speed_multiplier = 1.0
        self.lock = QMutex()
        self.pause_signal = QWaitCondition()

    def run(self):
        while self.active:
            self.lock.lock()
            if self.is_paused:
                self.pause_signal.wait(self.lock)
            self.lock.unlock()

            adjusted_speed = self.speed_multiplier * 10

            # Sleeping based on the adjusted simulation speed
            time.sleep(1.0 / adjusted_speed)
            self.seconds_elapsed += 1
            print(self.seconds_elapsed)
            self.second_passed.emit(self.seconds_elapsed)

    def start_clock(self):
        self.active = True
        self.is_paused = False
        self.start()

    def halt_clock(self):
        self.lock.lock()
        self.is_paused = True
        self.lock.unlock()

    def continue_clock(self):
        self.lock.lock()
        self.is_paused = False
        self.pause_signal.wakeAll()
        self.lock.unlock()

    def modify_speed(self, multiplier: float):
        self.speed_multiplier = multiplier
        print(f"Speed multiplier set to {multiplier}")

    def terminate_clock(self):
        self.active = False
        self.quit()
        self.wait()


class TimerUI(QWidget):
    def __init__(self, timer: TimerThread):
        super().__init__()
        self.timer = timer
        self.speed_multiplier = 1.0
        self.start_time = time.time()
        
        # Timer to update display based on speed multiplier
        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self.update_elapsed_time)
        
        # Start the display timer to refresh every second (real time)
        self.display_timer.start(1000)
        
        self.seconds_elapsed = 0
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        self.setStyleSheet("background-color: #eeeeee;")

        # Timer display label
        self.time_display = QLabel("00:00:00")
        self.time_display.setFixedWidth(170)
        self.time_display.setStyleSheet("""
            font-size: 30px;
            color: #222222;
            font-weight: bold;
            background-color: #ffffff;
            border-radius: 8px;
            padding: 8px;
            border: 1px solid #aaaaaa;
        """)
        layout.addWidget(self.time_display)

        # Speed slider configuration
        slider_layout = QHBoxLayout()

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(20)
        self.speed_slider.setValue(1)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.valueChanged.connect(self.update_speed)

        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #aaa;
                height: 6px;
                background: #dddddd;
                margin: 1px 0;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                border: 1px solid #777777;
                width: 16px;
                margin: -2px 0;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #66bb6a;
            }
            QSlider::tick:horizontal {
                background: #bbbbbb;
            }
        """)

        self.speed_display = QLabel("1.0x")
        self.speed_display.setStyleSheet("""
            font-size: 14px;
            color: #66bb6a;
            font-weight: bold;
        """)
        
        slider_layout.addWidget(self.speed_slider)
        slider_layout.addWidget(self.speed_display)

        layout.addLayout(slider_layout)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

    @pyqtSlot()
    def update_elapsed_time(self):
        # Increase elapsed time based on speed multiplier
        self.seconds_elapsed += self.speed_multiplier
        hrs = int(self.seconds_elapsed // 3600)
        mins = int((self.seconds_elapsed % 3600) // 60)
        secs = int(self.seconds_elapsed % 60)

        # Update the display label with the formatted time
        self.time_display.setText(f"{hrs:02}:{mins:02}:{secs:02}")

    @pyqtSlot(int)
    def update_speed(self, multiplier: int):
        # Update speed multiplier and display text
        self.speed_multiplier = multiplier
        self.speed_display.setText(f"{multiplier:.1f}x")
        print(f"Speed multiplier set to {multiplier}")
        self.timer.modify_speed(multiplier)
        
        # Adjust display update interval based on speed multiplier
        if multiplier > 0:
            self.display_timer.start(int(1000 / multiplier))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock_thread = TimerThread()
    ui = TimerUI(clock_thread)
    clock_thread.start_clock()
    ui.show()
    sys.exit(app.exec())
