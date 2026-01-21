#!/bin/bash

echo "[*] System scan"
curl -X POST -d "mode=system" http://127.0.0.1:5000/scan

echo "[*] Network scan"
curl -X POST -d "mode=network&target=127.0.0.1" http://127.0.0.1:5000/scan

echo "[*] File scan"
curl -X POST -d "mode=files&path=./scan_data" http://127.0.0.1:5000/scan

echo "[+] Testy zakończone"