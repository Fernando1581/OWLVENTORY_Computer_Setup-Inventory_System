import os
from PyQt6 import QtWidgets, QtGui
from views.ui_Signup import Ui_MainWindow as UiSignup
from models.employee import EmployeeModel

class SignupController:
    def __init__(self):
        self.view = QtWidgets.QMainWindow()
        self.ui = UiSignup()
        self.ui.setupUi(self.view)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_folder = os.path.join(base_dir, "Images")

        if hasattr(self.ui, 'Background'):
            self.ui.Background.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (3).png")))
        if hasattr(self.ui, 'WhiteLogo'):
            self.ui.WhiteLogo.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (4).png")))
        if hasattr(self.ui, 'pic'):
            self.ui.pic.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "logointro.png")))

        self.ui.loginButton.clicked.connect(self.open_login)
        self.ui.signUpButton.clicked.connect(self.register_employee)

    def open_login(self):
        from controllers.login_controller import LoginController
        self.login_controller = LoginController()
        self.login_controller.view.show()
        self.view.close()

    def register_employee(self):
        fn = self.ui.FNInput.text()
        mn = self.ui.MNInput.text()
        ln = self.ui.userRegInput_3.text()
        password = self.ui.passRegInput.text()

        if not fn or not ln or not password:
            QtWidgets.QMessageBox.warning(self.view, "Error", "Please fill in required fields")
            return

        try:
            employee_id = EmployeeModel.register(fn, mn, ln, password)
            QtWidgets.QMessageBox.information(
                self.view,
                "Success",
                f"Account registered successfully!\nYour Employee ID is: {employee_id}"
            )
            self.open_login()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, "Error", f"Database error: {e}")