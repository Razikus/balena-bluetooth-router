#!/bin/bash

sleep 1
/bin/hciconfig hci0 lm master,accept/bin
sleep 1
/bin/hciconfig hci0 piscan
sleep 1
/bin/hciconfig hci0 sspmode 1
sleep 1
sysctl -w net.ipv4.ip_forward=1
sleep 1
iptables -A INPUT -i pan0 -j ACCEPT
sleep 1
iptables -A FORWARD -i pan0 -j ACCEPT
sleep 1