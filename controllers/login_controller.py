import os
from PyQt6 import QtWidgets, QtGui
from views.ui_login import Ui_MainWindow as UiLogin
from models.employee import EmployeeModel
from models.admin import AdminModel


class LoginController:
    def __init__(self):
        self.view = QtWidgets.QMainWindow()

        self.ui = UiLogin()
        self.ui.setupUi(self.view)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_folder = os.path.join(base_dir, "Images")

        self.ui.Background.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (3).png")))
        self.ui.WhiteLogo.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (4).png")))
        self.ui.pic.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "logointro.png")))

        self.ui.signUpButton.clicked.connect(self.open_signup)
        self.ui.signupButton2.clicked.connect(self.open_signup)
        self.ui.loginButton.clicked.connect(self.login_user)

    def open_signup(self):
        from controllers.signup_controller import SignupController
        self.signup_controller = SignupController()
        self.signup_controller.view.show()
        self.view.close()

    def login_user(self):
        user_id = self.ui.userInput.text()
        password = self.ui.passInput.text()

        if not user_id or not password:
            QtWidgets.QMessageBox.warning(self.view, "Error", "Please fill in both fields")
            return

        emp = EmployeeModel.login(user_id, password)
        if emp:
            emp_name = f"{emp[1]} {emp[3]}"
            from controllers.employee_controller import EmployeeController
            self.employee_controller = EmployeeController(emp_id=emp[0], emp_name=emp_name)
            self.employee_controller.view.show()
            self.view.close()
            return

        admin = AdminModel.login(user_id, password)
        if admin:
            try:
                admin_name = admin[1]
                from controllers.admin_controller import AdminController
                self.admin_controller = AdminController(admin_id=admin[0], admin_name=admin_name)
                self.admin_controller.view.show()
                self.view.close()
            except Exception as e:
                import traceback
                print(traceback.format_exc())  # Prints to terminal
                QtWidgets.QMessageBox.critical(self.view, "System Error", f"Could not load Admin Panel:\n{e}")
            return

        QtWidgets.QMessageBox.warning(self.view, "Error", "Invalid ID or password")