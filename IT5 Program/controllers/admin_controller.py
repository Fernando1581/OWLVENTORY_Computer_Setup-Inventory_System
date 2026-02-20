import hashlib
from datetime import datetime, timedelta
from models.admin import AdminModel
from models.employee import EmployeeModel
from views.admin_view import AdminView

# --- IMPORTS ---
from controllers.stock_out_controller import StockOutController
from controllers.items_added_controller import ItemsAddedController
from controllers.req_action_controller import ReqActionController

try:
    from fpdf import FPDF

    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False


class AdminController:
    def __init__(self, admin_id, admin_name):
        self.admin_id = admin_id
        self.admin_name = admin_name  # Store name for reports
        self.view = AdminView(admin_name)

        self.bind_signals()
        self.refresh_all()

    def show(self):
        self.view.show_view()

    def bind_signals(self):
        # Navigation
        self.view.bind_nav(
            self.show_dashboard, self.show_setups, self.show_inventory,
            self.show_requests, self.show_registration, self.logout
        )
        self.view.bind_dashboard_clicks(
            self.show_setups, self.open_logs, self.show_inventory
        )

        # Inventory Actions
        self.view.bind_inventory_actions(
            self.add_computer, self.generate_current_status_report, None
        )
        self.view.bind_stock_buttons(lambda r, n, a: (lambda: self.mod_stock(r, n, a)))

        # Request Actions
        self.view.bind_request_actions(
            self.handle_request_action, self.generate_history_report,
            self.load_requests_filtered, self.toggle_date_filter
        )

        # Setup/Employee Actions
        self.view.bind_setup_actions(self.retire_employee)
        self.view.bind_register_action(self.register_new_employee)

    def refresh_all(self):
        self.load_setups()
        self.load_computers()
        self.load_requests()
        self.load_hardware()
        self.load_kpi()

    # --- Navigation Logic ---
    def show_dashboard(self):
        self.view.switch_page("dashboard")
        self.load_kpi()
        self.check_dashboard_warnings()

    def show_setups(self):
        self.view.switch_page("setups")
        self.load_setups()

    def show_inventory(self):
        self.view.switch_page("inventory")
        self.load_computers()
        self.load_hardware()

    def show_requests(self):
        self.view.switch_page("requests")
        self.load_requests()

    def show_registration(self):
        self.view.switch_page("register")

    def logout(self):
        if self.view.ask_confirm("Logout", "Are you sure you want to log out?"):
            from controllers.login_controller import LoginController
            self.lc = LoginController()
            self.lc.show()
            self.view.close_view()

    # --- Data Loading Logic ---
    def load_setups(self):
        data = AdminModel.get_all_setups()
        self.view.update_generic_table("assigned", data)

    def load_computers(self):
        data = AdminModel.get_all_computers()
        self.view.update_generic_table("computers", data)

    def load_hardware(self):
        data = AdminModel.get_hardware_inventory()
        self.view.update_hardware_table(data)

    def load_requests(self):
        self.load_requests_filtered(None)

    def load_requests_filtered(self, date_str_ignored):
        # 1. Active Requests (Pending)
        active = AdminModel.get_all_requests()
        self.view.update_generic_table("active_req", active, [0, 1, 4])

        # 2. History Requests
        all_history = AdminModel.get_request_history()

        show_all = self.view.is_show_all_checked()
        selected_pydate = self.view.get_date_filter_value()

        formatted_rows = []

        for row in all_history:
            # row structure: [0:pcNo, 1:empId, 2:empName, 3:hardware, 4:status, 5:dateAction, 6:validator]
            status = row[4]
            if status in ["Ignored", "Pending"]:
                continue

            # --- Date Handling ---
            db_date = row[5]
            if isinstance(db_date, str):
                try:
                    db_date = datetime.strptime(db_date, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    db_date = datetime.now()

            # Date Filter Logic
            include = False
            if show_all:
                include = True
            else:
                if db_date.date() == selected_pydate:
                    include = True

            if include:
                date_started = db_date
                date_finished = date_started + timedelta(days=2)

                str_started = date_started.strftime("%Y-%m-%d")
                str_finished = date_finished.strftime("%Y-%m-%d")
                str_full_date = date_started.strftime("%Y-%m-%d %H:%M")

                ui_row = [
                    row[0],  # PC No
                    row[2],  # Requested By
                    row[3],  # Hardware Change
                    row[4],  # Tech / Status
                    str_started,
                    str_finished,
                    str_full_date,
                    row[6]  # Validator
                ]
                formatted_rows.append(ui_row)

        self.view.update_generic_table("history_req", formatted_rows, None)

    def toggle_date_filter(self, checked):
        self.view.toggle_date_edit(not checked)
        self.load_requests()

    def load_kpi(self):
        stats = AdminModel.get_dashboard_kpis()
        self.view.update_kpi(stats['active'], stats['items'], stats['available'])

        graph_data = AdminModel.get_graph_data()
        if graph_data:
            names = [row[0] for row in graph_data]
            qtys = [row[1] for row in graph_data]
            self.view.draw_graph(names, qtys)

    def check_dashboard_warnings(self):
        data = AdminModel.get_graph_data()
        low = [f"{n} ({q})" for n, q in data if q < 5]
        if low:
            msg = "Low Stock Warning (< 5):\n" + "\n".join(low)
            self.view.show_alert("Dashboard Warning", msg, "warning")

    # --- Inventory Actions ---
    def add_computer(self):
        self.view.show_alert("Requirements", "Creating a new computer requires 1 unit of each hardware component.")
        if self.view.ask_confirm("Confirm Creation", "Are you sure you want to proceed?"):
            success, msg = AdminModel.create_new_computer(self.admin_id)
            self.view.show_alert("Result", msg, "info" if success else "warning")
            if success: self.refresh_all()

    def mod_stock(self, row, name, amount):
        curr = self.view.get_hardware_qty_at_row(row)
        if curr + amount < 0:
            self.view.show_alert("Stock Error", "Cannot reduce below 0.", "warning")
            return

        action_type = "add" if amount > 0 else "remove"
        if not self.view.ask_confirm("Confirm", f"Are you sure you want to {action_type} 1 unit of {name}?"):
            return

        reason = "Stocking"
        if amount < 0:
            dialog = StockOutController(self.view)
            if dialog.exec():
                reason = dialog.get_reason()
            else:
                return

        try:
            AdminModel.update_hardware_stock(name, amount, self.admin_id, reason)
            self.load_hardware()
            self.load_kpi()

            new_qty = self.view.get_hardware_qty_at_row(row)
            if new_qty < 5:
                self.view.show_alert("Low Stock", f"{name} is running low!", "warning")
        except Exception as e:
            self.view.show_alert("Error", str(e), "error")

    # --- Logs & Request Processing ---
    def open_logs(self):
        dialog = ItemsAddedController()
        dialog.exec()

    def handle_request_action(self):
        idx = self.view.get_selected_request_row_index()
        if idx < 0: return

        requests = AdminModel.get_all_requests()
        if idx >= len(requests): return

        data = requests[idx]
        dialog = ReqActionController(self.view, data, self.admin_id)
        if dialog.run():
            self.load_requests()

    # --- Employee Management ---
    def retire_employee(self):
        emp_id, pc_no = self.view.get_selected_setup_id()
        if not emp_id:
            self.view.show_alert("Selection", "Select a row first.", "warning")
            return
        if self.view.ask_confirm("Confirm Removal", "This cannot be undone. Proceed?"):
            success, msg = AdminModel.retire_employee(emp_id, pc_no)
            self.view.show_alert("Result", msg, "info" if success else "error")
            self.refresh_all()

    def register_new_employee(self):
        fn, mn, ln, pw = self.view.get_registration_inputs()
        if not fn or not ln or not pw:
            self.view.show_alert("Error", "Fill required fields.", "warning")
            return

        hashed = hashlib.sha256(pw.encode()).hexdigest()
        try:
            new_id = EmployeeModel.register(fn, mn, ln, hashed)
            self.view.show_alert("Success", f"Registered! ID: {new_id}")
            self.view.clear_registration_inputs()
        except Exception as e:
            self.view.show_alert("Error", str(e), "error")

    # --- PDF Reporting ---
    def generate_current_status_report(self):
        if not HAS_FPDF:
            self.view.show_alert("Error", "FPDF library missing.", "error")
            return

        data = AdminModel.get_inventory_snapshot()
        kpi = AdminModel.get_dashboard_kpis()
        if not data:
            self.view.show_alert("Empty", "No data.", "warning")
            return

        default_name = f"Inventory_Snapshot_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        path = self.view.open_save_dialog(default_name)
        if not path: return

        try:
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "OWLVENTORY - CURRENT INVENTORY STATUS", ln=True, align='C')
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, 10, f"Generated: {datetime.now()}", ln=True, align='C')
            pdf.ln(5)

            pdf.cell(0, 8, f"Active PCs: {kpi['active']}", ln=True)
            pdf.cell(0, 8, f"Available PCs: {kpi['available']}", ln=True)
            pdf.ln(5)

            cols = ["Hardware", "Brand", "Qty", "Status"]
            widths = [60, 50, 40, 40]

            pdf.set_font("Arial", 'B', 10)
            pdf.set_fill_color(200, 200, 200)
            for i, c in enumerate(cols):
                pdf.cell(widths[i], 10, c, border=1, fill=True, align='C')
            pdf.ln()

            pdf.set_font("Arial", '', 10)
            for row in data:
                name, brand, qty = str(row[0]), str(row[1]), int(row[2])
                status = "Good"
                r, g, b = 0, 0, 0
                if qty < 5:
                    status, r, g, b = "CRITICAL", 220, 0, 0
                elif qty < 10:
                    status, r, g, b = "Low", 220, 150, 0

                pdf.set_text_color(0, 0, 0)
                pdf.cell(widths[0], 10, name, border=1)
                pdf.cell(widths[1], 10, brand, border=1)
                pdf.cell(widths[2], 10, str(qty), border=1, align='C')

                pdf.set_text_color(r, g, b)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(widths[3], 10, status, border=1, align='C')
                pdf.set_font("Arial", '', 10)
                pdf.ln()

            pdf.output(path)
            self.view.show_alert("Success", "Report Saved.")
        except Exception as e:
            self.view.show_alert("Error", str(e), "error")

    def generate_history_report(self):
        if not HAS_FPDF: return
        data = AdminModel.get_request_history()
        if not data:
            self.view.show_alert("Empty", "No history.", "warning")
            return

        path = self.view.open_save_dialog(f"Hardware_Change_Report_{datetime.now().strftime('%Y%m%d')}.pdf")
        if not path: return

        try:
            # A4 Landscape width is roughly 297mm
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.add_page()

            # --- HEADER SECTION ---
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "OWLVENTORY - HARDWARE REPLACEMENT REPORT", ln=True, align='C')

            pdf.set_font("Arial", 'I', 10)
            # Add Generated By and Date
            pdf.cell(0, 5, f"Generated by: {self.admin_name}", ln=True, align='C')
            pdf.cell(0, 5, f"Date Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}", ln=True, align='C')
            pdf.ln(5)

            # --- TABLE SETUP ---
            # Columns and Widths
            cols = ["PC", "Emp Name", "Item", "Tech", "Start", "Finish"]
            widths = [15, 50, 40, 40, 35, 35]

            # Calculate Centering
            total_table_width = sum(widths)
            page_width = 297  # A4 Landscape width in mm
            x_offset = (page_width - total_table_width) / 2

            # Set Left Margin to center the table
            pdf.set_left_margin(x_offset)

            # --- TABLE HEADER ---
            pdf.set_font("Arial", 'B', 10)
            pdf.set_fill_color(200, 200, 200)  # Light Gray
            for i, c in enumerate(cols):
                pdf.cell(widths[i], 10, c, border=1, fill=True, align='C')
            pdf.ln()

            # --- TABLE BODY ---
            pdf.set_font("Arial", '', 9)
            pdf.set_fill_color(255, 255, 255)  # White

            for row in data:
                # row: [pcNo, empId, empName, hw, status, dateAction, validator]
                status, hw = str(row[4]), str(row[3])
                if status in ["Ignored", "Pending"]: continue

                # Calculate dates for PDF
                d_start = row[5]
                if isinstance(d_start, str):
                    try:
                        d_start = datetime.strptime(d_start, "%Y-%m-%d %H:%M:%S")
                    except:
                        d_start = datetime.now()

                d_end = d_start + timedelta(days=2)

                vals = [
                    str(row[0]),
                    str(row[2]),
                    hw,
                    status,
                    d_start.strftime("%Y-%m-%d"),
                    d_end.strftime("%Y-%m-%d")
                ]

                for i, v in enumerate(vals):
                    pdf.cell(widths[i], 8, v[:25], border=1, align='C')
                pdf.ln()

            pdf.output(path)
            self.view.show_alert("Success", "Report Saved.")
        except Exception as e:
            self.view.show_alert("Error", str(e), "error")