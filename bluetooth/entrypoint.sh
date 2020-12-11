#!/bin/bash

python3 /bridge.py

bash /bluetooth.sh
bash /bluetoothserver.sh &
bash /bluetoothclient.sh &

while true; do echo "$(date) ...RUNNING..."; sleep 120; done
