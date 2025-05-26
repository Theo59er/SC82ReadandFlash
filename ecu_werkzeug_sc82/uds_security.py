from j2534_interface import J2534Interface
import time

def request_seed(j2534):
    print("🧩 Sende Seed-Anfrage (0x27 0x01)...")

    # Sende 0x27 0x01 (SecurityAccess: Request Seed Level 1)
    # Padding mit 0x55 wie bei anderen UDS-Kommandos
    message = [0x02, 0x27, 0x01] + [0x55] * 5
    j2534.send_message(0x7E0, message)

    time.sleep(0.1)
    response = j2534.receive_message()

    if response:
        if response[1] == 0x67:
            level = response[2]
            seed_length = response[0] - 2
            seed = response[3:3+seed_length]
            print(f"✅ Seed (Level {level}) erhalten: {seed}")
            return seed
        elif response[1] == 0x7F:
            print(f"❌ Negativer UDS-Response: 0x7F Service {hex(response[2])} Fehlercode {hex(response[3])}")
        else:
            print(f"⚠️ Unerwartete Antwort: {response}")
    else:
        print("❌ Keine Antwort erhalten.")
    return None
