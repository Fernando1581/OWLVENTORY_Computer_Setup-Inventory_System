from models.admin import AdminModel
from views.req_action_view import ActionView, FixView, HardwareView


class ReqActionController:
    def __init__(self, parent_view, data, admin_id):
        # data format from DB: [pcNo, employeeID, empName, hardware, status, requestID, validator]
        self.parent = parent_view
        self.data = data
        self.request_id = data[5]
        self.admin_id = admin_id

        # Result flag to tell the main controller if data changed
        self.action_taken = False

        # Initialize Views
        self.view_action = ActionView(parent_view)
        self.view_fix = FixView(parent_view)
        self.view_hw = HardwareView(parent_view)

        # Setup Action View
        self.view_action.set_details(data[0], data[2], data[4])
        self.view_action.bind_buttons(self.action_ignore, self.action_check)

        # Setup Fix View
        self.view_fix.bind_buttons(self.fix_normal, self.fix_hardware)

        # Setup Hardware View
        self.view_hw.bind_grant(self.grant_hardware)

    def run(self):
        """Main entry point. Returns True if an action was taken."""
        self.view_action.exec()
        return self.action_taken

    # --- Step 1: Action View Logic ---
    def action_ignore(self):
        try:
            AdminModel.update_request_status(self.request_id, "Ignored", self.admin_id)
            self.view_action.show_message("Request Ignored.")
            self.action_taken = True
            self.view_action.accept()
        except Exception as e:
            self.view_action.show_message(str(e), True)

    def action_check(self):
        try:
            AdminModel.update_request_status(self.request_id, "Checked", self.admin_id)
        except Exception as e:
            self.view_action.show_message(str(e), True)
            return

        # Hide first dialog, show second
        self.view_action.hide()
        result = self.view_fix.exec()

        if result == 1:  # Accepted
            self.action_taken = True
            self.view_action.accept()
        else:
            # If they closed/canceled the Fix dialog, revert status or leave as Checked?
            # Original logic implied reverting to Pending if cancelled, let's keep it safe.
            try:
                AdminModel.update_request_status(self.request_id, "Pending", self.admin_id)
            except:
                pass
            self.view_action.close()

    # --- Step 2: Fix View Logic ---
    def fix_normal(self):
        try:
            AdminModel.complete_normal_fix(self.request_id, self.admin_id)
            self.view_fix.show_success("Normal fix recorded.")
            self.view_fix.accept()
        except Exception as e:
            self.view_fix.show_error(str(e))

    def fix_hardware(self):
        self.view_fix.hide()
        result = self.view_hw.exec()

        if result == 1:
            self.view_fix.accept()
        else:
            self.view_fix.reject()

    # --- Step 3: Hardware View Logic ---
    def grant_hardware(self):
        hw_name, tech_name = self.view_hw.get_selection()
        success, msg = AdminModel.complete_hardware_change(self.request_id, hw_name, tech_name, self.admin_id)

        if success:
            self.view_hw.show_message(msg)
            self.view_hw.accept()
        else:
            self.view_hw.show_message(msg, True)