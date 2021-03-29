from checksums import calculate_default_checksum, calculate_crc16
from string_and_bytes import bytes_to_string, string_to_bytes


def prepare_packets(message, crc):
    data_to_packets = [message[i:i+128] for i in range(0, len(message), 128)]
    packets = []
    packet_number = 0
    for data_packet in data_to_packets:
        if packet_number == 256:
            packet_number = 0
        start_bytes = bytearray(b'\x01')
        packet_number_bytes = bytearray(packet_number)
        data_bytes = bytearray(data_packet)
        if crc:
            checksum_bytes = bytearray(calculate_crc16(data_packet).to_bytes(2, 'little'))
        else:
            checksum_bytes = bytearray(calculate_default_checksum(data_packet).to_bytes(2, 'little'))
        packet_bytes = start_bytes + packet_number_bytes + data_bytes + checksum_bytes
        # print(start_bytes)
        # print(packet_number_bytes)
        # print(data_bytes)
        # print(checksum_bytes)
        # print()
        # print(packet_bytes)
        # print()
        # print()
        packets.append(packet_bytes)
        packet_number += 1
    return packets


def start_communication(message, crc, sender_port, receiver_port):
    packets = prepare_packets(message, crc)
    if crc:
        # C
        receiver_port.write(string_to_bytes("C"))
    else:
        # NAK
        receiver_port.write(0x15)
    received = sender_port.readline()
    print("RECEIVED FIRST:", received)
    if received == string_to_bytes("C") or received == 0x15:
        for send_packet in packets:
            sender_port.write(bytes(send_packet))
            print("WYSLANE:")
            print(bytes(send_packet))
            received_packet = receiver_port.read(133)
            print("OTRZYMANE:")
            print(received_packet)

