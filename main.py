import sys
from string_and_bytes import *
from COM_ports import *
from communication import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import gui

ports = inicialize_ports()


class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.clear_button.clicked.connect(self.clear_all)
        self.exit_button.clicked.connect(self.close)
        self.start_communication_button.clicked.connect(self.start_communication_button_method)

    def clear_all(self):
        self.message_text_field.clear()
        self.sender_text_field.clear()
        self.receiver_text_field.clear()

    def start_communication_button_method(self):
        input_text = self.message_text_field.toPlainText()
        crc = self.crc_checksum_check.isChecked
        if self.COM1_port_check.isChecked:
            port_nadawcy, port_odbiorcy = ports
        else:
            port_odbiorcy, port_nadawcy = ports
        sender_log, receiver_log = start_communication(input_text, crc, port_nadawcy, port_odbiorcy)
        self.sender_text_field.setText(sender_log)
        self.receiver_text_field.setText(receiver_log)


def main():

    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

