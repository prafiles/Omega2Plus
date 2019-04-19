#!/bin/sh
#Information Gather Phase
expled 00004B #Green
ip=$(curl -s https://api.ipify.org)
#Screen Setup Phase
expled 790000 #Red
oled-exp -c
oled-exp -i
oled-exp dim on
#oled-exp cursor 0,0 write 'Omega Onion2+'
#Display Phase
expled 00EF00
oled-exp cursor 0,0 write "`date +\"%d-%m-%y %H:%M:%S\"`"
oled-exp cursor 1,0 write "$ip"
sleep 5
#Cleanup
expled 000000
