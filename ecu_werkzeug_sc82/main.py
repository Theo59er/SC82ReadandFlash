from j2534_interface import J2534Interface
from flash_reader import lese_block
import time

def main():
    print("🧠 Starte Flash-Dump im Bench-Modus...")

    try:
        # Initialisiere Verbindung
        j2534 = J2534Interface()
        j2534.open_device()
        j2534.connect_can()

        # Optional: Session aktivieren (0x10 0x03)
        print("🛠 Starte Diagnose-Sitzung...")
        j2534.send_message(0x7E0, [0x02, 0x10, 0x03] + [0x55]*5)
        response = j2534.receive_message()
        if response and response[1] == 0x50:
            print(f"✅ Session aktiviert (SID: 0x{response[2]:02X})")
        else:
            print("⚠️  Sessionantwort fehlt oder ungültig")

        # Flash-Parameter
        base_address = 0x00000000  # Startadresse
        end_address  = 0x00080000  # Beispiel: 512 KB (je nach ECU ggf. mehr!)
        step         = 0x20        # Blockgröße: 32 Bytes pro Anfrage

        # Datei anlegen
        with open("ecu_dump.bin", "wb") as dump:
            for addr in range(base_address, end_address, step):
                block = lese_block(j2534, addr, size=step)
                if block:
                    dump.write(bytearray(block))
                    print(f"✅ 0x{addr:08X} gelesen")
                else:
                    print(f"❌ Fehler bei 0x{addr:08X} – Dump abgebrochen")
                    break

        print("🧾 Dump abgeschlossen – Datei: ecu_dump.bin")

    except Exception as e:
        print(f"❌ Fehler: {e}")
    finally:
        j2534.close()

if __name__ == "__main__":
    main()
