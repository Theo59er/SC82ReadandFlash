import ctypes

# DLL-Pfad für Tactrix Openport 2.0
DLL_PATH = r"C:\WINDOWS\SysWOW64\op20pt32.dll"


# Konstanten
PROTOCOL_ID_CAN = 0x00000005
BAUDRATE = 500000

class J2534Interface:
    def __init__(self):
        self.dll = ctypes.WinDLL(DLL_PATH)
        self.device_id = ctypes.c_void_p()
        self.channel_id = ctypes.c_void_p()

    def open_device(self):
        result = self.dll.PassThruOpen(None, ctypes.byref(self.device_id))
        if result != 0:
            raise Exception(f"PassThruOpen fehlgeschlagen (Code: {result})")
        print("✅ Gerät geöffnet:", self.device_id)

    def connect_can(self):
        result = self.dll.PassThruConnect(
            self.device_id,
            PROTOCOL_ID_CAN,
            0,
            BAUDRATE,
            ctypes.byref(self.channel_id)
        )
        if result != 0:
            raise Exception(f"PassThruConnect fehlgeschlagen (Code: {result})")
        print("✅ CAN-Verbindung geöffnet:", self.channel_id)

    def close(self):
        try:
            self.dll.PassThruDisconnect(self.channel_id)
            self.dll.PassThruClose(self.device_id)
            print("🔌 Verbindung geschlossen.")
        except:
            print("Verbindung konnte nicht korrekt geschlossen werden.")
