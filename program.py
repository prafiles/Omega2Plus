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


interface_readings_dict={}

def get_interface_last_val(interface):
    global interface_readings_dict
    interface_readings = interface_readings_dict.get(interface, None)
    if interface_readings is None:
        interface_readings = {
            'rx' : 0,
            'tx' : 0,
            'time' : time.time()
        }
        interface_readings_dict[interface] = interface_readings
    return interface_readings

def set_interface_value(interface, rx, tx, timestamp):
    global interface_readings_dict
    interface_readings_dict[interface] = {
        'rx':rx,
        'tx':tx,
        'time': timestamp
    }


def get_interface_val(interface):
    last_readings = get_interface_last_val(interface)
    text = get('https://10.0.0.1/fetchif.cgi?' + interface, verify=False, auth=(os.environ['USER'],os.environ['PASSWORD'])).text.split('\n')[1]
    text_cols = text.split()
    rx_bytes_new = int (text_cols[1])
    tx_bytes_new = int (text_cols[9])
    timestamp_new = time.time()
    set_interface_value(interface, rx_bytes_new, tx_bytes_new, timestamp_new)
    rx_kilobyte_rate = int ((rx_bytes_new - last_readings['rx'])*8 / ((timestamp_new - last_readings['time']) * 1000))
    tx_kilobyte_rate = int ((tx_bytes_new - last_readings['tx'])*8 / ((timestamp_new - last_readings['time']) * 1000))
    return {
        'rx_rate':rx_kilobyte_rate / 1000,
        'tx_rate':tx_kilobyte_rate / 1000
    }


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
    readings = get_interface_val('ppp0')
    oledExp.setCursor(2,0)
    oledExp.write("WAN Mbps Rx " + str (readings['rx_rate']) + " Tx " + str (readings['tx_rate']))
    readings = get_interface_val('eth0')
    oledExp.setCursor(3,0)
    oledExp.write("ETH Mbps Rx " + str (readings['rx_rate']) + " Tx " + str (readings['tx_rate']))
