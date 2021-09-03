#!/bin/sh

CLIENT_IP=$2
BROADCAST_IP=$(ip a show eth0 | awk '/inet \S+ brd \S+/{print $4}')
BROADCAST_PORT=12345

ip route del $CLIENT_IP || true
echo "$CLIENT_IP" | socat - UDP-DATAGRAM:$BROADCAST_IP:$BROADCAST_PORT,broadcast
exit 0
