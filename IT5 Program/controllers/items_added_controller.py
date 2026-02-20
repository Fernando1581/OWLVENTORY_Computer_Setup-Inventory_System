from datetime import datetime, timedelta
from models.admin import AdminModel
from views.items_added_view import ItemsAddedView

try:
    from fpdf import FPDF

    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False


class ItemsAddedController:
    def __init__(self):
        self.view = ItemsAddedView()

        self.view.bind_filter_change(self.handle_combo_change)
        self.view.bind_apply(self.apply_filter)
        self.view.bind_generate(self.generate_pdf_report)

        self.load_initial()

    def exec(self):
        self.view.exec()

    def load_initial(self):
        try:
            data = AdminModel.get_stock_logs()
            self.view.update_table(data)
        except:
            pass

    def handle_combo_change(self):
        selection = self.view.get_filter_mode()
        today = datetime.now().date()
        start_date = today

        if selection == "Weekly":
            start_date = today - timedelta(days=7)
        elif selection == "Monthly":
            start_date = today - timedelta(days=30)
        elif selection == "Yearly":
            start_date = today - timedelta(days=365)

        self.view.set_date_range(start_date, today)

    def apply_filter(self):
        d1, d2 = self.view.get_date_range()

        if d1 > d2:
            self.view.show_message("Date Error", "Start Date cannot be after End Date.", True)
            return

        try:
            data = AdminModel.get_stock_logs_filtered(str(d1), str(d2))
            self.view.update_table(data)
            if not data:
                self.view.show_message("Result", "No logs found for this period.")
        except Exception as e:
            self.view.show_message("Error", str(e), True)

    def generate_pdf_report(self):
        if not HAS_FPDF:
            self.view.show_message("Error", "FPDF library is missing.", True)
            return

        headers, data = self.view.get_table_data_for_pdf()

        if not data:
            self.view.show_message("Empty", "No data to generate report.", True)
            return

        filename = f"Items_Added_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
        path = self.view.open_save_dialog(filename)

        if not path: return

        try:
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.add_page()

            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "OWLVENTORY - LOGS REPORT", ln=True, align='C')

            d1, d2 = self.view.get_date_range()
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, 6, f"Period: {d1} to {d2}", ln=True, align='C')

            timestamp = datetime.now().strftime('%B %d, %Y %I:%M %p')
            pdf.set_font("Arial", 'I', 9) # Italic, slightly smaller
            pdf.cell(0, 6, f"Generated on: {timestamp}", ln=True, align='C')

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
            self.view.show_message("Success", "Report saved successfully.")

        except Exception as e:
            self.view.show_message("Error", f"Failed to generate PDF:\n{e}", True)