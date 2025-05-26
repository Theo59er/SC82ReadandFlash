from j2534_interface import J2534Interface
from uds_security import request_seed
from diagnostic_sessions import start_session
from uds_memory import read_memory_by_address

def main():
    print("🔍 Test: ECU OEM-Sitzung & SecurityAccess & Flash-Lesen")

    try:
        j2534 = J2534Interface()
        j2534.open_device()
        j2534.connect_can()

        # Schritt 1: OEM-Diagnosesitzung (0x10 0x85)
        if not start_session(j2534, 0x85):
            print("❌ OEM-Sitzung konnte nicht gestartet werden.")
            return

        # Schritt 2: Seed anfragen (SecurityAccess Level 1)
        seed = request_seed(j2534)

        if not seed:
            print("❌ Kein Seed erhalten. SecurityAccess eventuell blockiert.")
            return
        print("🎯 Seed erhalten. Jetzt bereit für Key oder Brute-Force.")

        # Schritt 3: Testweise einen Speicherbereich lesen (optional)
        read_memory_by_address(j2534, address=0x000000, length=4)

    except Exception as e:
        print(f"❌ Fehler: {e}")
    finally:
        try:
            j2534.close()
        except:
            pass

if __name__ == "__main__":
    main()
