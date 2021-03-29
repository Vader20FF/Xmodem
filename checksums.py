import binascii
import xmodem


def getc(size, timeout=1):
    return size or None


def putc(data, timeout=1):
    return data or None


modem = xmodem.XMODEM(getc, putc)


# def calculate_crc(data):
#     return binascii.crc_hqx(data, 0)


# def crc16(data: bytes, poly=0x8408):
#     data = bytearray(data)
#     crc = 0xFFFF
#     for b in data:
#         cur_byte = 0xFF & b
#         for _ in range(0, 8):
#             if (crc & 0x0001) ^ (cur_byte & 0x0001):
#                 crc = (crc >> 1) ^ poly
#             else:
#                 crc >>= 1
#             cur_byte >>= 1
#     crc = (~crc & 0xFFFF)
#     crc = (crc << 8) | ((crc >> 8) & 0xFF)
#
#     return crc & 0xFFFF


def calculate_default_checksum(data):
    return modem.calc_checksum(data)


def calculate_crc16(data):
    return modem.calc_crc(data)
