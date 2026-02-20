import os
from PyQt6 import QtWidgets, QtGui
from views.ui_login import Ui_MainWindow

class LoginView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_images()

    def setup_images(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_folder = os.path.join(base_dir, "Images")
        try:
            self.ui.Background.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (3).png")))
            self.ui.WhiteLogo.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (4).png")))
            self.ui.pic.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "logointro.png")))
        except Exception:
            pass

    # --- Interaction Methods for Controller ---
    def bind_login_action(self, callback):
        self.ui.loginButton.clicked.connect(callback)

    def get_credentials(self):
        return self.ui.userInput.text(), self.ui.passInput.text()

    def show_error(self, message):
        QtWidgets.QMessageBox.warning(self, "Login Error", message)

    def close_view(self):
        self.close()

    def show_view(self):
        self.show()