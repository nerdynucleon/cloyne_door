## Cloyne Front Door

# Hardware Components:
1. HID 5352A rfid card reader
2. Raspberry Pi running dietpi
3. Optoisolator connected to gpio, driving door opener
4. RS232 to USB converter

# Software Components:
1. rc.local bash script - this is run at startup, starts main.py automatically
2. main.py - communicates with reader, drives gpio, checks valid ID's, logging
3. .log - log of what ID's were used at what time, access granted or denied

# Troubleshooting:
1. Raspberry Disk Gets Corrupted from improper shutdown (power outages):
    -Solution: reformat SD card, reinstall OS, apt-get libraries (rpio,pyserial), git pull repo, replace rc.local
2. Log says door opened, but door does not open:
    -Solution: Check connections with multimeter, reference schematic
3. Log too large, disk full
    -Solution: Delete log?
