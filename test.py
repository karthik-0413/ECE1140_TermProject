import sys
from PyQt6.QtWidgets import QApplication
import track_model_ui

app = track_model_ui.QtWidgets.QApplication([])

ui = track_model_ui.track_ui()
ui.setupUi()

ui.uploadButton.clicked.connect(ui.test_upload_button)

ui.show()



sys.exit(app.exec())

