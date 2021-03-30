from checksums import calculate_default_checksum, calculate_crc16
from string_and_bytes import *


def prepare_packets(message, crc):
    data_to_packets = [message[i:i+128] for i in range(0, len(message), 128)]
    packets = []
    packet_number = 0
    for data_packet in data_to_packets:
        if packet_number == 256:
            packet_number = 0
        start_bytes = bytearray(b'\x01')
        packet_number_bytes = bytearray(packet_number.to_bytes(2, 'big'))
        data_bytes = bytearray(data_packet)
        if len(data_bytes) != 128:
            # data_bytes = data_bytes + bytearray(b'!EOP!')
            data_bytes = data_bytes + bytearray(int(0).to_bytes(128-len(data_bytes), 'big'))
        if crc:
            checksum_bytes = bytearray(calculate_crc16(data_bytes).to_bytes(2, 'big'))
        else:
            checksum_bytes = bytearray(calculate_default_checksum(data_bytes).to_bytes(2, 'big'))
        packet_bytes = start_bytes + packet_number_bytes + data_bytes + checksum_bytes
        packets.append(packet_bytes)
        packet_number += 1
    return packets


def start_communication(message, crc, sender_port, receiver_port):
    bytesText = string_to_bytes(message)
    packets = prepare_packets(bytesText, crc)
    if crc:
        # C
        receiver_port.write(bytearray.fromhex("43"))
    else:
        # NAK
        receiver_port.write(bytearray.fromhex("15"))
    received_hex = bytes.hex(sender_port.readline())
    # print("RECEIVED FIRST:", received)
    if received_hex == "43" or received_hex == "15":
        received_data = ""
        for send_packet in packets:
            print("WYSLANE:")
            print(bytes(send_packet))
            sender_port.write(bytes(send_packet))
            received_packet = bytearray(receiver_port.read(133))
            if crc:
                checksum_bytes = bytearray(calculate_crc16(received_packet[3:131]).to_bytes(2, 'big'))
            else:
                checksum_bytes = bytearray(calculate_default_checksum(received_packet[3:131]).to_bytes(2, 'big'))
            if checksum_bytes == received_packet[131:133]:
                # ACK
                receiver_port.write(bytearray.fromhex("06"))
                received_hex = bytes.hex(sender_port.readline())
            else:
                # NAK
                receiver_port.write(bytearray.fromhex("15"))
                received_hex = bytes.hex(sender_port.readline())
                while checksum_bytes != received_packet[131:133]:
                    sender_port.write(bytes(send_packet))
                    received_packet = receiver_port.read(133)
                    if crc:
                        checksum_bytes = bytearray(calculate_crc16(received_packet[3:131]).to_bytes(2, 'big'))
                    else:
                        checksum_bytes = bytearray(
                            calculate_default_checksum(received_packet[3:131]).to_bytes(2, 'big'))
                    if checksum_bytes == received_packet[131:133]:
                        # ACK
                        receiver_port.write(bytearray.fromhex("06"))
                        received_hex = bytes.hex(sender_port.readline())
                        break
                    else:
                        receiver_port.write(bytearray.fromhex("15"))
                        received_hex = bytes.hex(sender_port.readline())
            print("OTRZYMANE:")
            print(bytes(received_packet))
            received_data = received_data + bytes_to_string(received_packet[3:131])
            print("FINAL:")
            print(received_data)
        # END OF TRANSMISSION
        sender_port.write(bytes(bytearray.fromhex("04")))
        received_hex = bytes.hex(receiver_port.readline())
        if received_hex == "04":
            receiver_port.write(bytearray.fromhex("06"))
            received_hex = bytes.hex(sender_port.readline())
        print("KOMUNIKACJA ZAKONCZONA POWODZENIEM!")




