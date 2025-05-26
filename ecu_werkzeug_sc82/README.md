# ECU Werkzeug SC82

Ein freies Python-Werkzeug zur Kommunikation mit dem Steuergerät (ECU) der Honda CBR1000RR-R Fireblade SC82 (Keihin, RH850).  
Ziel: Auslesen und Schreiben des Flash-Speichers über OBD mittels Tactrix Openport 2.0.

---

## ✅ Funktionen

- Verbindung zum Openport 2.0 via J2534
- UDS-Kommunikation (z. B. Diagnose-Session, SecurityAccess)
- Seed/Key-Handling (SecurityAccess)
- Vorbereitung für Flash-Dump (ReadMemoryByAddress)

---

## ⚙️ Voraussetzungen

- Python **3.13 (32-Bit)**  
- Tactrix Openport 2.0 inkl. Treiber (op20pt32.dll)
- Visual Studio Code oder CLI
- Zündung an, Motor aus

