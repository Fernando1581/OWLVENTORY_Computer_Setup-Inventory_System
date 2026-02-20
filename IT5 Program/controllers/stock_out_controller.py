from views.stock_out_view import StockOutView


class StockOutController:
    def __init__(self, parent_view_widget=None):
        self.view = StockOutView(parent_view_widget)
        self.selected_reason = None

        self.view.bind_buttons(self.set_transfered, self.set_damaged)

    def exec(self):
        """Returns True if a selection was made, False otherwise."""
        result = self.view.exec()
        return result == 1  # 1 is QDialog.Accepted

    def set_transfered(self):
        self.selected_reason = "Transfered"
        self.view.close_dialog()

    def set_damaged(self):
        self.selected_reason = "Damaged/Defective"
        self.view.close_dialog()

    def get_reason(self):
        return self.selected_reason