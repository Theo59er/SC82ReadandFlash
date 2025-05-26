from j2534_interface import J2534Interface
from uds_security import request_seed

def main():
    print("🔍 Test: ECU SecurityAccess Seed anfordern")

    try:
        j2534 = J2534Interface()
        j2534.open_device()
        j2534.connect_can()

        seed = request_seed(j2534)

        if seed:
            print("🎯 Seed erhalten. Jetzt bereit für Key oder Brute-Force.")
        else:
            print("❌ Kein Seed erhalten. Zugriff eventuell gesperrt.")

    except Exception as e:
        print(f"❌ Fehler: {e}")
    finally:
        try:
            j2534.close()
        except:
            pass

if __name__ == "__main__":
    main()
