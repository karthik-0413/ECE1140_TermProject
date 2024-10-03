import sys
import os

cur_dir = os.path.dirname(__file__)
ui_dir = os.path.join(cur_dir, '../UI/')
sys.path.append(ui_dir)

import frontend
from  PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = frontend.App()
    ex.show()
    sys.exit(app.exec())
