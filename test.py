import onionGpio
# for delay
import time

# Create GPIO object
gpioObject17 = onionGpio.OnionGpio(17)
gpioObject16 = onionGpio.OnionGpio(16)
gpioObject15 = onionGpio.OnionGpio(15)

time.sleep(0.01)

status = gpioObject17.setOutputDirection(1)
status = gpioObject16.setOutputDirection(1)
status = gpioObject15.setOutputDirection(1)

while True:
    for r in range(0,2):
        for g in range(0,2):
            for b in range(0,2):
                status = gpioObject17.setOutputDirection(r)
                status = gpioObject16.setOutputDirection(g)
                status = gpioObject15.setOutputDirection(b)
                time.sleep(0.01)