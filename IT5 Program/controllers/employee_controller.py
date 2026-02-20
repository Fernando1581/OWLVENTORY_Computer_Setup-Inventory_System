from models.computer import ComputerModel
from models.employee import EmployeeModel
from views.employee_view import EmployeeView
from controllers.dialog_controller import RequestController


class EmployeeController:
    def __init__(self, emp_id, emp_name):
        self.emp_id = emp_id
        self.view = EmployeeView(emp_id)

        self.check_assigned_pc()
        self.view.bind_actions(self.logout, self.open_report_form, self.show_notifications)

    def show(self):
        self.view.show_view()

    def show_notifications(self):
        msgs = EmployeeModel.get_all_notifications(self.emp_id)
        self.view.show_notification_dialog(msgs)
        EmployeeModel.mark_read(self.emp_id)

    def open_report_form(self):
        pc_data = ComputerModel.get_pc_by_employee(self.emp_id)
        if not pc_data:
            self.view.show_alert("Error", "No assigned PC.", True)
            return

        pc_no = pc_data[0]
        dialog = RequestController(self.emp_id, pc_no)
        dialog.run()

    def check_assigned_pc(self):
        try:
            pc = ComputerModel.get_pc_by_employee(self.emp_id)
            if pc:
                self.view.set_pc_label(f"PC #{pc[0]}")
            else:
                pc_num = ComputerModel.assign_pc(self.emp_id)
                self.view.set_pc_label(f"PC #{pc_num}" if pc_num else "No PC Available")
        except Exception as e:
            self.view.show_alert("Error", str(e), True)

    def logout(self):
        if self.view.ask_confirm("Logout", "Log out?"):
            from controllers.login_controller import LoginController
            self.lc = LoginController()
            self.lc.show()
            self.view.close_view()