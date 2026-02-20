from datetime import datetime, timedelta
from models.admin import AdminModel
from models.employee import EmployeeModel
from views.dialog_view import (
    StockOutView, ItemsAddedView, ReportFormView,
    ActionView, FixView, HWView
)

try:
    from fpdf import FPDF

    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False


class StockOutController:
    def __init__(self):
        self.view = StockOutView()
        self.reason = None
        self.view.bind(self.set_transfered, self.set_damaged)

    def set_transfered(self):
        self.reason = "Transfered"
        self.view.accept()

    def set_damaged(self):
        self.reason = "Damaged/Defective"
        self.view.accept()

    def exec(self):
        return self.view.exec()

    def get_reason(self):
        return self.reason


class RequestController:
    def __init__(self, emp_id, pc_no):
        self.view = ReportFormView()
        self.emp_id = emp_id
        self.pc_no = pc_no
        self.view.bind(self.submit)

    def submit(self):
        text = self.view.get_text()
        if not text.strip():
            self.view.show_msg("Enter a reason.", True)
            return
        try:
            EmployeeModel.save_request(self.pc_no, self.emp_id, "PC Issue", text)
            self.view.show_msg("Submitted.")
            self.view.accept()
        except Exception as e:
            self.view.show_msg(str(e), True)

    def run(self):
        self.view.exec()


class ItemsAddedController:
    def __init__(self):
        self.view = ItemsAddedView()
        self.view.bind(self.filter_combo, self.apply_filter, self.generate_pdf)
        self.load_initial()

    def run(self):
        self.view.exec()

    def load_initial(self):
        try:
            data = AdminModel.get_stock_logs()
            self.view.update_table(data)
        except:
            pass

    def filter_combo(self):
        mode = self.view.get_combo_text()
        today = datetime.now().date()
        start = today
        if mode == "Weekly":
            start = today - timedelta(days=7)
        elif mode == "Monthly":
            start = today - timedelta(days=30)
        elif mode == "Yearly":
            start = today - timedelta(days=365)
        self.view.set_dates(start, today)

    def apply_filter(self):
        d1, d2 = self.view.get_dates()
        if d1 > d2:
            self.view.show_msg("Start date cannot be after end date.")
            return
        data = AdminModel.get_stock_logs_filtered(d1, d2)
        self.view.update_table(data)

    def generate_pdf(self):
        if not HAS_FPDF: return
        headers, data = self.view.get_table_headers_and_data()
        if not data: return

        path = self.view.open_save_dialog(f"Items_Added_{datetime.now().strftime('%Y%m%d')}.pdf")
        if not path: return

        try:
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "OWLVENTORY - LOGS REPORT", ln=True, align='C')

            pdf.set_font("Arial", '', 10)
            d1, d2 = self.view.get_dates()
            pdf.cell(0, 10, f"Period: {d1} to {d2}", ln=True, align='C')
            pdf.ln(5)

            col_widths = [70, 25, 60, 50, 50]
            pdf.set_font("Arial", 'B', 10)
            pdf.set_fill_color(200, 200, 200)
            for i, h in enumerate(headers):
                w = col_widths[i] if i < len(col_widths) else 40
                pdf.cell(w, 10, h, border=1, fill=True, align='C')
            pdf.ln()

            pdf.set_font("Arial", '', 9)
            pdf.set_fill_color(255, 255, 255)
            for row in data:
                for i, val in enumerate(row):
                    w = col_widths[i] if i < len(col_widths) else 40
                    text = str(val)
                    if len(text) > 35: text = text[:32] + "..."
                    pdf.cell(w, 8, text, border=1, align='C')
                pdf.ln()

            pdf.output(path)
            self.view.show_msg("PDF Saved.")
        except Exception as e:
            self.view.show_msg(f"Error: {e}")


class ReqActionController:
    def __init__(self, data, admin_id):
        self.data = data
        self.req_id = data[5]
        self.admin_id = admin_id
        self.success = False

        self.view_act = ActionView()
        self.view_fix = FixView()
        self.view_hw = HWView()

        self.view_act.set_info(data[0], data[2], data[4])
        self.view_act.bind(self.on_ignore, self.on_check)
        self.view_fix.bind(self.on_fix_normal, self.on_fix_hardware)
        self.view_hw.bind(self.on_grant_hw)

    def run(self):
        self.view_act.exec()
        return self.success

    def on_ignore(self):
        try:
            AdminModel.update_request_status(self.req_id, "Ignored", self.admin_id)
            self.view_act.show_msg("Ignored.")
            self.success = True
            self.view_act.accept()
        except Exception as e:
            self.view_act.show_msg(str(e))

    def on_check(self):
        try:
            AdminModel.update_request_status(self.req_id, "Checked", self.admin_id)
        except:
            return

        self.view_act.hide()
        res = self.view_fix.exec()
        if res == 1:  # Accepted
            self.view_act.accept()
        else:
            try:
                AdminModel.update_request_status(self.req_id, "Pending", self.admin_id)
            except:
                pass
            self.view_act.close()

    def on_fix_normal(self):
        try:
            AdminModel.complete_normal_fix(self.req_id, self.admin_id)
            self.success = True
            self.view_fix.accept()
        except Exception as e:
            pass

    def on_fix_hardware(self):
        self.view_fix.hide()
        res = self.view_hw.exec()
        if res == 1:
            self.view_fix.accept()
        else:
            self.view_fix.reject()

    def on_grant_hw(self):
        hw, tech = self.view_hw.get_selection()
        success, msg = AdminModel.complete_hardware_change(self.req_id, hw, tech, self.admin_id)
        if success:
            self.view_hw.show_msg(msg)
            self.success = True
            self.view_hw.accept()
        else:
            self.view_hw.show_msg(msg, True)