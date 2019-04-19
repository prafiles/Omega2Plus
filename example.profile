export USER=user
export PASSWORD=password
echo timer > /sys/class/leds/omega2p\:amber\:system/trigger
echo 75 > /sys/class/leds/omega2p\:amber\:system/delay_on
echo 4925 > /sys/class/leds/omega2p\:amber\:system/delay_off
