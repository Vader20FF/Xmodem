from checksums import calculate_default_checksum, calculate_crc16
from string_and_bytes import *


# def prepare_packets(message, crc):
#     print("Przechodze do tworzenia pakietow")
#     data_to_packets = [message[i:i+128] for i in range(0, len(message), 128)]
#     packets = []
#     packet_number = 0
#     for data_packet in data_to_packets:
#         if packet_number == 256:
#             packet_number = 0
#         start_bytes = bytearray(b'\x01')
#         packet_number_bytes = bytearray(packet_number.to_bytes(2, 'big'))
#         data_bytes = bytearray(data_packet)
#         if len(data_bytes) != 128:
#             # data_bytes = data_bytes + bytearray(b'!EOP!')
#             data_bytes = data_bytes + bytearray(int(0).to_bytes(128-len(data_bytes), 'big'))
#         if crc:
#             checksum_bytes = bytearray(calculate_crc16(data_bytes).to_bytes(2, 'big'))
#         else:
#             checksum_bytes = bytearray(calculate_default_checksum(data_bytes).to_bytes(2, 'big'))
#         packet_bytes = start_bytes + packet_number_bytes + data_bytes + checksum_bytes
#         packets.append(packet_bytes)
#         packet_number += 1
#     print("Ukonczylem tworzenie pakietow")
#     print(*packets)
#     return packets

def prepare_packets(message, crc):
    print("Przechodze do tworzenia pakietow")
    data_to_packets = [message[i:i+128] for i in range(0, len(message), 128)]
    packets = []
    packet_number = 1
    for data_packet in data_to_packets:
        if packet_number == 256:
            packet_number = 0
        start_bytes = b'\x01'
        packet_number_byte_one = packet_number.to_bytes(1, 'big')
        packet_number_byte_two = (255 - packet_number).to_bytes(1, 'big')
        data_bytes = bytearray(data_packet)
        if len(data_bytes) != 128:
            data_bytes = data_bytes + bytearray(int(26).to_bytes(128-len(data_bytes), 'big'))
        if crc:
            checksum_bytes = calculate_crc16(data_bytes).to_bytes(2, 'big')
        else:
            checksum_bytes = calculate_default_checksum(data_bytes).to_bytes(1, 'big')
        data_bytes = bytes(data_bytes)
        packet_bytes = start_bytes + packet_number_byte_one + packet_number_byte_two + data_bytes + checksum_bytes
        packets.append(packet_bytes)
        packet_number += 1
    print("Ukonczylem tworzenie pakietow")
    for packet in packets:
        print(packet)
    print()
    return packets


def send(data, crc, sender_port):
    packets = prepare_packets(data, crc)
    print("ROZPOCZYNAM WYSYLANIE")
    received_hex = bytes.hex(sender_port.read(1))
    print("TO BYLO 1")
    print(received_hex)
    if received_hex == "18":
        received_hex = bytes.hex(sender_port.read(1))
        while received_hex != "43" or received_hex != "15" or received_hex != "01":
            received_hex = bytes.hex(sender_port.read(1))
    if received_hex == "43" or received_hex == "15" or received_hex == "01":
        it = 2
        for send_packet in packets:
            sender_port.write(send_packet)
            print(f"TO BYLO {it}")
            received_hex = bytes.hex(sender_port.read(1))
            print(received_hex)
            if received_hex != bytearray.fromhex("06"):
                it += 1
                continue
            else:
                while received_hex != bytearray.fromhex("06"):
                    sender_port.write(send_packet)
                    received_hex = bytes.hex(sender_port.read(1))
                    print(received_hex)
            it += 1
    sender_port.write(bytearray.fromhex("04"))
    print("TO BYLO FINAL")
    received_hex = bytes.hex(sender_port.read(1))
    print("KOMUNIKACJA ZAKONCZONA POWODZENIEM!")


def receive(crc, receiver_port):
    received_bytes = bytearray()
    if crc:
        # C
        receiver_port.write(bytearray.fromhex("43"))
    else:
        # NAK
        receiver_port.write(bytearray.fromhex("15"))
    received_packet = bytearray(receiver_port.read(133))
    while received_packet != bytearray.fromhex("04"):
        if crc:
            checksum_bytes = bytearray(calculate_crc16(received_packet[3:131]).to_bytes(2, 'big'))
        else:
            checksum_bytes = bytearray(calculate_default_checksum(received_packet[3:131]).to_bytes(2, 'big'))
        if checksum_bytes == received_packet[131:133]:
            # ACK
            receiver_port.write(bytearray.fromhex("06"))
            received_bytes = received_bytes + received_packet[3:131]
        else:
            # NAK
            receiver_port.write(bytearray.fromhex("15"))
            while checksum_bytes != received_packet[131:133]:
                received_packet = receiver_port.read(133)
                if crc:
                    checksum_bytes = bytearray(calculate_crc16(received_packet[3:131]).to_bytes(2, 'big'))
                else:
                    checksum_bytes = bytearray(
                        calculate_default_checksum(received_packet[3:131]).to_bytes(2, 'big'))
                if checksum_bytes == received_packet[131:133]:
                    # ACK
                    receiver_port.write(bytearray.fromhex("06"))
                    received_bytes = received_bytes + received_packet[3:131]
                    break
                else:
                    receiver_port.write(bytearray.fromhex("15"))
        received_packet = bytearray(receiver_port.read(133))
    receiver_port.write(bytearray.fromhex("06"))
    return received_bytes
