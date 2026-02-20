import os
from PyQt6 import QtWidgets, QtGui, QtCore
from views.ui_Employee import Ui_MainWindow
from views.ui_notification import Ui_NotificationDialog


class EmployeeView(QtWidgets.QMainWindow):
    def __init__(self, emp_id):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_images()
        self.ui.label_3.setText(f"Employee ID: {emp_id}")

    def setup_images(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_folder = os.path.join(base_dir, "Images")
        try:
            self.ui.label.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "Untitled design (2).png")))
            self.ui.personIcon.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "person icon.png")))
            self.ui.label_5.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "pc logo white.png")))
            self.ui.label_7.setPixmap(QtGui.QPixmap(os.path.join(img_folder, "pc pic (1000 x 1000 px).png")))
            self.ui.logoutButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "logout.png")))
            self.ui.reportButton.setIcon(QtGui.QIcon(os.path.join(img_folder, "warning.png")))
        except Exception:
            pass

    def bind_actions(self, logout_cb, report_cb, notif_cb):
        self.ui.logoutButton.clicked.connect(logout_cb)
        self.ui.reportButton.clicked.connect(report_cb)
        if hasattr(self.ui, 'notification'):
            self.ui.notification.clicked.connect(notif_cb)

    def set_pc_label(self, text):
        self.ui.label_6.setText(text)

    def show_alert(self, title, msg, is_error=False):
        if is_error:
            QtWidgets.QMessageBox.critical(self, title, msg)
        else:
            QtWidgets.QMessageBox.warning(self, title, msg)

    def ask_confirm(self, title, msg):
        reply = QtWidgets.QMessageBox.question(self, title, msg,
                                               QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        return reply == QtWidgets.QMessageBox.StandardButton.Yes

    def show_notification_dialog(self, data_list):
        if not data_list:
            QtWidgets.QMessageBox.information(self, "Notifications", "No notifications yet.")
            return

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Dialog)
        dialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        ui_notif = Ui_NotificationDialog()
        ui_notif.setupUi(dialog)
        ui_notif.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)

        for hardware, status, date_obj in data_list:
            d_str = str(date_obj).split()[0]
            ui_notif.listWidget.addItem(f"{d_str} | Request for {hardware}: {status}")

        ui_notif.closeButton.clicked.connect(dialog.accept)
        dialog.exec()

    def close_view(self):
        self.close()

    def show_view(self):
        self.show()