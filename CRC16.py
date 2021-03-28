def CRC16(file_buffer):
    tmp = 0
    val = 0x18005 << 15

    for i in range(0, 3):
        tmp = tmp * 256 + file_buffer[i]

    tmp *= 256

    for i in range(3, 134):
        if i < 128:
            tmp += file_buffer[i]
        for j in range(0, 8):
            if tmp & 1 << 31:
                tmp ^= val
            tmp <<= 1

    return tmp >> 16
