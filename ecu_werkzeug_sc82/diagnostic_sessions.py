# diagnostic_sessions.py

import time

def start_session(j2534, session_id):
    """
    Startet eine UDS-Diagnose-Sitzung mit gegebenem Session-ID.
    Beispiele: 0x01 = Default, 0x03 = Extended, 0x85 = OEM
    """
    print(f"🛠 Starte Diagnose-Sitzung: 0x{session_id:02X}...")
    message = [0x02, 0x10, session_id] + [0x55] * 5
    j2534.send_message(0x7E0, message)
    time.sleep(0.1)
    response = j2534.receive_message()

    if response and response[1] == 0x50 and response[2] == session_id:
        print(f"✅ Sitzung 0x{session_id:02X} erfolgreich gestartet.")
        return True
    elif response and response[1] == 0x7F:
        print(f"❌ Sitzung abgelehnt. Fehlercode: 0x{response[3]:02X}")
    else:
        print("❌ Keine gültige Antwort erhalten.")
    return False
