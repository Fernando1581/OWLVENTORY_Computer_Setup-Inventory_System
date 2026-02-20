from models.employee import EmployeeModel
from views.request_view import RequestView

class RequestController:
    def __init__(self, parent_view_widget, emp_id, pc_no):
        # We pass the parent widget to the View so the dialog centers correctly
        self.view = RequestView(parent_view_widget)
        self.emp_id = emp_id
        self.pc_no = pc_no

        self.view.bind_submit(self.submit)

    def show(self):
        self.view.exec()

    def submit(self):
        reason = self.view.get_reason()

        if not reason.strip():
            self.view.show_error("Please enter the reason.")
            return

        try:
            EmployeeModel.save_request(self.pc_no, self.emp_id, "PC Issue", reason)
            self.view.show_success("Report submitted.")
            self.view.close_dialog()
        except Exception as e:
            self.view.show_error(f"Failed: {e}")