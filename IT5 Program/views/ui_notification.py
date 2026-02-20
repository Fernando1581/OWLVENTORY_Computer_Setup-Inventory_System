from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_NotificationDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 350)

        # Stylesheet for the Frameless window look
        Dialog.setStyleSheet("""
            QDialog {
                background-color: rgb(255, 255, 255);
                border: 2px solid #41237F;
                border-radius: 15px;
            }
        """)

        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        # Remove border from label so it looks clean against the background
        self.label.setStyleSheet("color: rgb(44, 10, 113); border: none;")
        self.label.setText("Notifications")

        self.listWidget = QtWidgets.QListWidget(parent=Dialog)
        self.listWidget.setGeometry(QtCore.QRect(20, 60, 361, 221))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 5px;
                background-color: #f9f9f9;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
        """)

        self.closeButton = QtWidgets.QPushButton(parent=Dialog)
        self.closeButton.setGeometry(QtCore.QRect(130, 300, 141, 35))
        font = QtGui.QFont()
        font.setBold(True)
        self.closeButton.setFont(font)
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: #41237F;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        self.closeButton.setText("Okay, got it")

        QtCore.QMetaObject.connectSlotsByName(Dialog)