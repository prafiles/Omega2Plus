import os
import time
import socket
import onionGpio
from OmegaExpansion import oledExp
from requests import get
from dns import resolver

gpio_rled = onionGpio.OnionGpio(17)
gpio_gled = onionGpio.OnionGpio(16)
gpio_bled = onionGpio.OnionGpio(15)
gpio_rled.setOutputDirection(0)
gpio_gled.setOutputDirection(0)
gpio_bled.setOutputDirection(0)
time.sleep(0.25) #Blink white 1 second to confirm LED function
oledExp.driverInit(1)
oledExp.setBrightness(0)
oledExp.setTextColumns()
rx_bytes=0
tx_bytes=0
timestamp = time.time()

def color_blink(r,g,b,duration=0.25,sleep=0.25):
    #LED GPIO 1 means LOW and 0 means HIGH
    gpio_rled.setValue(1-r)
    gpio_gled.setValue(1-g)
    gpio_bled.setValue(1-b)
    time.sleep(duration)
    gpio_rled.setValue(1)
    gpio_gled.setValue(1)
    gpio_bled.setValue(1)
    time.sleep(sleep)

while True:
    time.sleep(5)
    oledExp.clear()
    time.sleep(10)
    #DNS Try
    oledExp.setCursor(0,0)
    try:
        res = resolver.Resolver()
        res.nameservers = ['10.0.0.3']
        answers = res.query('stackexchange.com', lifetime=5)
        oledExp.write("DNS Good")
    except:
        oledExp.write("DNS Bad")
        color_blink(1,0,0)
        continue
    #Internet HTTP Try
    oledExp.setCursor(1,0)
    try:
        ip = get('https://api.ipify.org').text
        oledExp.write("Internet Good")
    except:
        oledExp.write("Internet Bad")
        print ("HTTP Request Failed")
        color_blink(1,0,0)
        color_blink(1,0,0)
        continue
    color_blink(0,1,0) #Internet Good
    text = get('https://10.0.0.1/fetchif.cgi?ppp0',verify=False,auth=(os.environ['USER'],os.environ['PASSWORD'])).text.split('\n')[1]
    timestamp_new = time.time()
    text_cols = text.split()
    rx_bytes_new = int (text_cols[1])
    tx_bytes_new = int (text_cols[9])
    rx_kilobyte_rate = int ((rx_bytes_new - rx_bytes) / ((timestamp_new - timestamp) * 1000))
    tx_kilobyte_rate = int ((tx_bytes_new - tx_bytes) / ((timestamp_new - timestamp) * 1000))
    rx_bytes = rx_bytes_new
    tx_bytes = tx_bytes_new
    timestamp = timestamp_new
    oledExp.setCursor(2,0)
    oledExp.write("Rx " + str (rx_kilobyte_rate) + " KB/s")
    oledExp.setCursor(3,0)
    oledExp.write("Tx " + str (tx_kilobyte_rate) + " KB/s")
