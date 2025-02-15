#!/bin/bash

INTERFACE="enp1s0f3" #"enp1s0f2" #"enp1s0f1"
NETWORK_RANGE="192.168.30.0/24"

ARP_RESULTS=$(mktemp)
NMAP_RESULTS=$(mktemp)

### arp-scan
echo "Running arp-scan on $NETWORK_RANGE..."
arp-scan --interface=$INTERFACE $NETWORK_RANGE > "$ARP_RESULTS"

printf "%-15s %-20s %-50s %-20s\n" "IP Address" "MAC Address" "Vendor" "Hostname"
while read line; do
    IP=$(echo $line | awk '{print $1}')
    MAC=$(echo $line | awk '{print $2}')
    VENDOR=$(echo $line | cut -d ' ' -f 3-)
    if [ "$VENDOR" = "(Unknown)" ]; then
	VENDOR="Unknown"
    fi
    if [[ $IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
	HOSTNAME=$(host $IP | awk '/pointer/ {print $5}' | sed 's/\.$//')
	printf "%-15s %-20s %-50s %-20s\n" "$IP" "$MAC" "$VENDOR" "${HOSTNAME:-Unknown}"
    fi
done < "$ARP_RESULTS"

rm "$ARP_RESULTS" "$NMAP_RESULTS"
