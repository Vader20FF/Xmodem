import serial.tools.list_ports


def available_ports():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    return connected


def inicialize_ports():
    ser1 = serial.Serial()
    ser1.baudrate = 9600
    ser1.port = 'COM1'
    ser1.timeout = 0
    ser1.open()

    ser2 = serial.Serial()
    ser2.baudrate = 9600
    ser2.port = 'COM2'
    ser2.timeout = 0
    ser2.open()

    return ser1, ser2


def open_port(port):
    port.open()


def close_port(port):
    port.close()


def check_is_open(port):
    return port.isOpen()
