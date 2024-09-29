# main_window.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from test2 import Communicate  # Import the signal module

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize the Communicate class
        self.communicate = Communicate()

        # Connect the custom signal to a slot
        self.communicate.button_clicked_signal.connect(self.on_button_clicked)

        self.initUI()

    def initUI(self):
        self.label = QLabel('Button not clicked yet', self)
        self.button = QPushButton('Click Me', self)

        # Connect the button click event to emit the custom signal
        self.button.clicked.connect(self.emit_signal)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.setWindowTitle('Custom Signal Example')
        self.show()

    def emit_signal(self):
        # Emit the custom signal with a message
        self.communicate.button_clicked_signal.emit("Button was clicked!")

    def on_button_clicked(self, message):
        # Slot to handle the custom signal with the message
        self.label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    sys.exit(app.exec())
