import ctypes

# DLL-Pfad für Tactrix Openport 2.0 (32-bit)
DLL_PATH = r"C:\WINDOWS\SysWOW64\op20pt32.dll"

# Protokoll-Konstanten
PROTOCOL_ID_CAN = 0x00000005
PROTOCOL_ID_ISO9141 = 0x00000003
BAUDRATE_CAN = 500000
BAUDRATE_KLINE = 10400

class J2534Interface:
    def __init__(self):
        self.dll = ctypes.WinDLL(DLL_PATH)
        self.device_id = ctypes.c_void_p()
        self.channel_id = ctypes.c_void_p()
        self.current_protocol = None

    def open_device(self):
        result = self.dll.PassThruOpen(None, ctypes.byref(self.device_id))
        if result != 0:
            raise Exception(f"PassThruOpen fehlgeschlagen (Code: {result})")
        print("✅ Gerät geöffnet:", self.device_id)

    def connect_can(self):
        self.current_protocol = PROTOCOL_ID_CAN
        result = self.dll.PassThruConnect(
            self.device_id,
            PROTOCOL_ID_CAN,
            0,
            BAUDRATE_CAN,
            ctypes.byref(self.channel_id)
        )
        if result != 0:
            raise Exception(f"PassThruConnect (CAN) fehlgeschlagen (Code: {result})")
        print("✅ CAN-Verbindung geöffnet:", self.channel_id)

    def connect_kline(self):
        self.current_protocol = PROTOCOL_ID_ISO9141
        result = self.dll.PassThruConnect(
            self.device_id,
            PROTOCOL_ID_ISO9141,
            0,
            BAUDRATE_KLINE,
            ctypes.byref(self.channel_id)
        )
        if result != 0:
            raise Exception(f"PassThruConnect (K-Line) fehlgeschlagen (Code: {result})")
        print("✅ K-Line-Verbindung geöffnet:", self.channel_id)

    def send_message(self, arbitration_id, data):
        class PASSTHRU_MSG(ctypes.Structure):
            _fields_ = [
                ("ProtocolID", ctypes.c_ulong),
                ("RxStatus", ctypes.c_ulong),
                ("TxFlags", ctypes.c_ulong),
                ("Timestamp", ctypes.c_ulong),
                ("DataSize", ctypes.c_ulong),
                ("ExtraDataIndex", ctypes.c_ulong),
                ("Data", ctypes.c_ubyte * 4128)
            ]

        msg = PASSTHRU_MSG()
        msg.ProtocolID = self.current_protocol
        msg.TxFlags = 0x00000000 if self.current_protocol == PROTOCOL_ID_ISO9141 else 0x00000001  # ISO15765 for CAN
        msg.DataSize = len(data)
        msg.ExtraDataIndex = 0

        for i in range(len(data)):
            msg.Data[i] = data[i]

        num_msgs = ctypes.c_ulong(1)

        result = self.dll.PassThruWriteMsgs(
            self.channel_id,
            ctypes.byref(msg),
            ctypes.byref(num_msgs),
            1000
        )

        if result != 0:
            raise Exception(f"❌ Senden fehlgeschlagen. Fehlercode: {result}")
        print(f"📤 Gesendet: {data}")

    def receive_message(self, timeout=1000):
        class PASSTHRU_MSG(ctypes.Structure):
            _fields_ = [
                ("ProtocolID", ctypes.c_ulong),
                ("RxStatus", ctypes.c_ulong),
                ("TxFlags", ctypes.c_ulong),
                ("Timestamp", ctypes.c_ulong),
                ("DataSize", ctypes.c_ulong),
                ("ExtraDataIndex", ctypes.c_ulong),
                ("Data", ctypes.c_ubyte * 4128)
            ]

        msg = PASSTHRU_MSG()
        num_msgs = ctypes.c_ulong(1)

        result = self.dll.PassThruReadMsgs(
            self.channel_id,
            ctypes.byref(msg),
            ctypes.byref(num_msgs),
            timeout
        )

        if result == 0 and num_msgs.value > 0:
            empfang = [msg.Data[i] for i in range(msg.DataSize)]
            print(f"📥 Empfang: {empfang}")
            return empfang
        else:
            print("⌛️ Keine Antwort erhalten.")
            return None

    def close(self):
        try:
            self.dll.PassThruDisconnect(self.channel_id)
            self.dll.PassThruClose(self.device_id)
            print("🔌 Verbindung geschlossen.")
        except:
            print("Verbindung konnte nicht korrekt geschlossen werden.")
