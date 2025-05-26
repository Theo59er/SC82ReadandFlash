from j2534_interface import J2534Interface
import time

def request_seed(j2534):
    print("🧩 Sende Seed-Anfrage (0x27 0x01)...")
    j2534.send_message(0x7E0, [0x02, 0x27, 0x01, 0x55, 0x55, 0x55, 0x55, 0x55])
    time.sleep(0.1)
    response = j2534.receive_message()

    if response and response[1] == 0x67:
        seed = response[3:3+response[2]-2]
        print(f"🧬 Seed erhalten: {seed}")
        return seed
    else:
        print("❌ Keine gültige Seed-Antwort.")
        return None

def send_key(j2534, key_bytes):
    print(f"🔑 Sende Key: {key_bytes}")
    message = [len(key_bytes)+2, 0x27, 0x02] + key_bytes
    message += [0x55] * (8 - len(message))  # Auffüllen auf 8 Byte
    j2534.send_message(0x7E0, message)
    response = j2534.receive_message()
    return response
