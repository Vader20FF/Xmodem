import sys
from string_and_bytes import *
from COM_ports import *
from communication import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import gui
from xmodem import XMODEM

port = inicialize_ports()
file_to_save_path = None
file_to_send_path = None


def getc(size, timeout=8):
    gbytes = port.read(size)
    print(f'Read Byte: {gbytes}')
    return gbytes or None


def putc(data, timeout=8):
    pbytes = port.write(data)
    print(f'Put Byte: {pbytes}')
    return pbytes or None


modem = XMODEM(getc, putc)


class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.erase_button.clicked.connect(self.clear_all)
        self.exit_button.clicked.connect(self.close)
        self.send_button.clicked.connect(self.send_button_method)
        self.receive_button.clicked.connect(self.receive_button_method)
        self.choose_file_to_send_path_button.clicked.connect(self.choose_file_to_send_path_button_method)
        self.choose_file_to_receive_path_button.clicked.connect(self.choose_file_to_receive_path_button_method)

    def clear_all(self):
        self.file_to_send_path_text_field.clear()
        self.file_to_receive_path_text_field.clear()
        self.operation_status_text_field.clear()

    def send_button_method(self):
        if not self.send_file_radio_button.isChecked:
            return None
        crc = self.crc16_algorithm_radio_button.isChecked
        data_to_be_sent = self.get_data_from_choosen_file(file_to_send_path)
        send(data_to_be_sent, crc, port)
        # with open(file_to_send_path, 'rb') as stream:
        #     modem.send(stream, retry=8)
        self.operation_status_text_field.setPlainText("Operacja wysyłania zakończona pomyślnie!")

    def receive_button_method(self):
        if not self.receive_file_radio_button.isChecked:
            return None
        crc = self.crc16_algorithm_radio_button.isChecked
        received_data = receive(crc, port)
        self.operation_status_text_field.setPlainText("Operacja odbierania zakończona pomyślnie!")
        self.save_received_data_to_choosen_file(received_data, file_to_save_path)


    def choose_file_to_send_path_button_method(self):
        global file_to_send_path
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.file_to_send_path_text_field.setPlainText(fileName)
            file_to_send_path = fileName
        return None

    def choose_file_to_receive_path_button_method(self):
        global file_to_save_path
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.file_to_receive_path_text_field.setPlainText(fileName)
            file_to_save_path = fileName
        return None

    def get_data_from_choosen_file(self, file_path):
        with open(file_path, 'rb') as file_data:
            return file_data.read()

    def save_received_data_to_choosen_file(self, received_data, file_path):
        with open(file_path, 'wb') as file_to_save:
            file_to_save.write(received_data)

def main():

    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

