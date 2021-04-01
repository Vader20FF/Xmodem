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
    packet_number = 0
    for data_packet in data_to_packets:
        if packet_number == 256:
            packet_number = 0
        start_bytes = b'\x01'
        packet_number_bytes = packet_number.to_bytes(2, 'big')
        data_bytes = bytearray(data_packet)
        if len(data_bytes) != 128:
            # data_bytes = data_bytes + bytearray(b'!EOP!')
            data_bytes = data_bytes + bytearray(int(0).to_bytes(128-len(data_bytes), 'big'))
        if crc:
            checksum_bytes = calculate_crc16(data_bytes).to_bytes(2, 'big')
        else:
            checksum_bytes = calculate_default_checksum(data_bytes).to_bytes(2, 'big')
        data_bytes = bytes(data_bytes)
        packet_bytes = start_bytes + packet_number_bytes + data_bytes + checksum_bytes
        packets.append(packet_bytes)
        packet_number += 1
    print("Ukonczylem tworzenie pakietow")
    print(*packets)
    return packets


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


def send(data, crc, sender_port):
    packets = prepare_packets(data, crc)
    print("ROZPOCZYNAM WYSYLANIE")
    received_hex = bytes.hex(sender_port.readline())
    print("TO BYLO 1")
    if received_hex == "43" or received_hex == "15" or received_hex == "01":
        it = 2
        for send_packet in packets:
            sender_port.write(bytes(send_packet))
            print(f"TO BYLO {it}")
            received_hex = bytes.hex(sender_port.readline())
            if received_hex != bytearray.fromhex("06"):
                continue
            else:
                while received_hex != bytearray.fromhex("06"):
                    sender_port.write(bytes(send_packet))
                    received_hex = bytes.hex(sender_port.readline())
            it += 1
        sender_port.write(bytearray.fromhex("04"))
        print("TO BYLO FINAL")
        received_hex = bytes.hex(sender_port.readline())
        print("KOMUNIKACJA ZAKONCZONA POWODZENIEM!")


# def start_communication(message, crc, sender_port, receiver_port):
#     print("ROZPOCZYNAM KOMUNIKACJĘ")
#     sender_text = ""
#     receiver_text = ""
#     text_iteration_temp = 1
#     bytesText = string_to_bytes(message)
#     packets = prepare_packets(bytesText, crc)
#     if crc:
#         # C
#         receiver_port.write(bytearray.fromhex("43"))
#         receiver_text = receiver_text + f"{text_iteration_temp}\n"
#         receiver_text = receiver_text + "WYSYLAM: 'C'\n"
#         receiver_text = receiver_text + "\n"
#         text_iteration_temp += 1
#     else:
#         # NAK
#         receiver_port.write(bytearray.fromhex("15"))
#         receiver_text = receiver_text + f"{text_iteration_temp}\n"
#         receiver_text = receiver_text + "WYSYLAM: 'NAK'\n"
#         receiver_text = receiver_text + "\n"
#         text_iteration_temp += 1
#     received_hex = bytes.hex(sender_port.readline())
#     sender_text = sender_text + f"{text_iteration_temp}\n"
#     sender_text = sender_text + f"OTRZYMALEM: {received_hex}" + "\n"
#     sender_text = sender_text + "\n"
#     text_iteration_temp += 1
#     if received_hex == "43" or received_hex == "15":
#         received_data = ""
#         for send_packet in packets:
#             print("WYSLANE:")
#             print(bytes(send_packet))
#             sender_port.write(bytes(send_packet))
#             sender_text = sender_text + f"{text_iteration_temp}\n"
#             sender_text = sender_text + f"WYSYLAM: {bytes(send_packet)}\n"
#             sender_text = sender_text + "\n"
#             text_iteration_temp += 1
#             received_packet = bytearray(receiver_port.read(133))
#             receiver_text = receiver_text + f"{text_iteration_temp}\n"
#             receiver_text = receiver_text + f"OTRZYMALEM: {received_packet}\n"
#             receiver_text = receiver_text + "\n"
#             text_iteration_temp += 1
#             if crc:
#                 checksum_bytes = bytearray(calculate_crc16(received_packet[3:131]).to_bytes(2, 'big'))
#             else:
#                 checksum_bytes = bytearray(calculate_default_checksum(received_packet[3:131]).to_bytes(2, 'big'))
#             if checksum_bytes == received_packet[131:133]:
#                 # ACK
#                 receiver_port.write(bytearray.fromhex("06"))
#                 receiver_text = receiver_text + f"{text_iteration_temp}\n"
#                 receiver_text = receiver_text + f"WYSYLAM: 'ACK'\n"
#                 receiver_text = receiver_text + "\n"
#                 text_iteration_temp += 1
#                 received_hex = bytes.hex(sender_port.readline())
#                 sender_port.write(bytes(send_packet))
#                 sender_text = sender_text + f"{text_iteration_temp}\n"
#                 sender_text = sender_text + f"OTRZYMALEM: {received_hex}\n"
#                 sender_text = sender_text + "\n"
#                 text_iteration_temp += 1
#             else:
#                 # NAK
#                 receiver_port.write(bytearray.fromhex("15"))
#                 receiver_text = receiver_text + f"{text_iteration_temp}\n"
#                 receiver_text = receiver_text + f"WYSYLAM: 'NAK'\n"
#                 receiver_text = receiver_text + "\n"
#                 text_iteration_temp += 1
#                 received_hex = bytes.hex(sender_port.readline())
#                 sender_text = sender_text + f"{text_iteration_temp}\n"
#                 sender_text = sender_text + f"OTRZYMALEM: {received_hex}\n"
#                 sender_text = sender_text + "\n"
#                 text_iteration_temp += 1
#                 while checksum_bytes != received_packet[131:133]:
#                     sender_port.write(bytes(send_packet))
#                     sender_text = sender_text + f"{text_iteration_temp}\n"
#                     sender_text = sender_text + f"WYSYLAM: {bytes(send_packet)}\n"
#                     sender_text = sender_text + "\n"
#                     text_iteration_temp += 1
#                     received_packet = receiver_port.read(133)
#                     receiver_text = receiver_text + f"{text_iteration_temp}\n"
#                     receiver_text = receiver_text + f"OTRZYMALEM: {received_packet}\n"
#                     receiver_text = receiver_text + f"WYSYLAM: 'NAK'\n"
#                     receiver_text = receiver_text + "\n"
#                     if crc:
#                         checksum_bytes = bytearray(calculate_crc16(received_packet[3:131]).to_bytes(2, 'big'))
#                     else:
#                         checksum_bytes = bytearray(
#                             calculate_default_checksum(received_packet[3:131]).to_bytes(2, 'big'))
#                     if checksum_bytes == received_packet[131:133]:
#                         # ACK
#                         receiver_port.write(bytearray.fromhex("06"))
#                         receiver_text = receiver_text + f"{text_iteration_temp}\n"
#                         receiver_text = receiver_text + f"WYSYLAM: 'ACK'\n"
#                         receiver_text = receiver_text + "\n"
#                         text_iteration_temp += 1
#                         received_hex = bytes.hex(sender_port.readline())
#                         sender_text = sender_text + f"{text_iteration_temp}\n"
#                         sender_text = sender_text + f"OTRZYMALEM: {received_hex}\n"
#                         sender_text = sender_text + "\n"
#                         text_iteration_temp += 1
#                         break
#                     else:
#                         receiver_port.write(bytearray.fromhex("15"))
#                         receiver_text = receiver_text + f"{text_iteration_temp}\n"
#                         receiver_text = receiver_text + f"WYSYLAM: 'NAK'\n"
#                         receiver_text = receiver_text + "\n"
#                         text_iteration_temp += 1
#                         received_hex = bytes.hex(sender_port.readline())
#                         sender_text = sender_text + f"{text_iteration_temp}\n"
#                         sender_text = sender_text + f"OTRZYMALEM: {received_hex}\n"
#                         sender_text = sender_text + "\n"
#                         text_iteration_temp += 1
#             print("OTRZYMANE:")
#             print(bytes(received_packet))
#             received_data = received_data + bytes_to_string(received_packet[3:131])
#         print("FINAL:")
#         print(received_data)
#         # END OF TRANSMISSION
#         sender_port.write(bytearray.fromhex("04"))
#         sender_text = sender_text + f"{text_iteration_temp}\n"
#         sender_text = sender_text + f"WYSYLAM: 'EOT'\n"
#         sender_text = sender_text + "\n"
#         text_iteration_temp += 1
#         received_hex = bytes.hex(receiver_port.readline())
#         received_hex = received_hex[-2] + received_hex[-1]
#         receiver_text = receiver_text + f"{text_iteration_temp}\n"
#         receiver_text = receiver_text + f"OTRZYMALEM: {received_hex}\n"
#         receiver_text = receiver_text + "\n"
#         text_iteration_temp += 1
#         if received_hex == "04":
#             receiver_port.write(bytearray.fromhex("06"))
#             receiver_text = receiver_text + f"{text_iteration_temp}\n"
#             receiver_text = receiver_text + f"WYSYLAM: 'ACK'\n"
#             receiver_text = receiver_text + "\n"
#             text_iteration_temp += 1
#             received_hex = bytes.hex(sender_port.readline())
#             sender_text = sender_text + f"{text_iteration_temp}\n"
#             sender_text = sender_text + f"OTRZYMALEM: {received_hex}\n"
#             sender_text = sender_text + "\n"
#             text_iteration_temp += 1
#         print("KOMUNIKACJA ZAKONCZONA POWODZENIEM!")
#         return sender_text, receiver_text