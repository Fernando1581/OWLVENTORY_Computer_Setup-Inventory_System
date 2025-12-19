import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from controllers.login_controller import LoginController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "Images")
    QDir.addSearchPath("img", image_path)
    controller = LoginController()
    controller.view.show()
    sys.exit(app.exec())
