from CRC16 import crc16


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
            checksum_bytes = bytearray(crc16(data_packet))
        else:
            checksum_bytes = 0
            for byte in data_packet:
                checksum_bytes += byte
            checksum_bytes %= 256
            checksum_bytes = bytearray(checksum_bytes)
        packet_bytes = start_bytes + packet_number_bytes + data_bytes + checksum_bytes
        packets.append(packet_bytes)
        packet_number += 1
    return packets


def start_communication(CRC, ):
    pass