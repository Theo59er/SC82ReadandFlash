import time

def lese_block(j2534, address, size=0x20):
    # UDS 0x23 – ReadMemoryByAddress
    addr_len = 4
    size_len = 1
    message = [0x04 + size_len, 0x23, addr_len]

    message += [(address >> 24) & 0xFF, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
    message.append(size_len)
    message.append(size)

    while len(message) < 8:
        message.append(0x55)

    j2534.send_message(0x7E0, message)
    response = j2534.receive_message(timeout=500)

    if response and response[1] == 0x63:
        return response[3:3 + size]
    else:
        return None
