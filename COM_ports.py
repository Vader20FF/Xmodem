import serial.tools.list_ports


def available_ports():
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    return connected


def open_port(port):
    port.open()


def close_port(port):
    port.close()


def check_is_open(port):
    return port.isOpen()
