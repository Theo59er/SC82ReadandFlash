# uds_memory.py

import time

def read_memory_by_address(j2534, address, length):
    """
    Sendet ein UDS ReadMemoryByAddress (0x23)-Kommando.
    Address = Zieladresse (z. B. 0x00000000)
    Length = Anzahl der Bytes (z. B. 4)
    """
    addr_len_format = 0x24  # 3 Byte Address + 1 Byte Length

    addr_bytes = [(address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
    len_bytes = [length & 0xFF]

    data = [len(addr_bytes) + len(len_bytes) + 1, 0x23, addr_len_format] + addr_bytes + len_bytes
    data += [0x55] * (8 - len(data))  # Padding

    print(f"📤 Lese Flash: Addr 0x{address:06X}, Len {length} Byte")
    j2534.send_message(0x7E0, data)

    time.sleep(0.1)
    response = j2534.receive_message()

    if response and response[1] == 0x63:
        datalen = response[0] - 2
        content = response[2:2 + datalen]
        print(f"📥 Flash-Inhalt: {content}")
        return content
    elif response and response[1] == 0x7F:
        print(f"❌ Zugriff verweigert (0x7F). Fehlercode: 0x{response[3]:02X}")
    else:
        print("❌ Keine Antwort erhalten.")
    return None
