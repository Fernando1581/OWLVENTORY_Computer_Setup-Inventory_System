import hashlib
from models.employee import EmployeeModel
from models.admin import AdminModel
from views.login_view import LoginView

class LoginController:
    def __init__(self):
        self.view = LoginView()
        self.view.bind_login_action(self.login_user)

    def show(self):
        self.view.show_view()

    def login_user(self):
        user_id, password = self.view.get_credentials()

        if not user_id or not password:
            self.view.show_error("Please fill in both fields")
            return

        # Hash password
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        # 1. Try Employee
        emp = EmployeeModel.login(user_id, hashed_pw)
        if emp:
            # emp structure: (id, Fn, Mn, Ln, password)
            emp_name = f"{emp[1]} {emp[3]}"
            from controllers.employee_controller import EmployeeController
            self.next_ctrl = EmployeeController(emp_id=emp[0], emp_name=emp_name)
            self.next_ctrl.show()
            self.view.close_view()
            return

        # 2. Try Admin (Plain text check as per original code)
        admin = AdminModel.login(user_id, password)
        if admin:
            # admin structure: (adminID, Fn)
            admin_name = admin[1]
            from controllers.admin_controller import AdminController
            self.next_ctrl = AdminController(admin_id=admin[0], admin_name=admin_name)
            self.next_ctrl.show()
            self.view.close_view()
            return

        self.view.show_error("Invalid ID or password")