import time
import onionGpio
from OmegaExpansion import oledExp
from requests import get
from dns import resolver

oledExp.driverInit(1)
oledExp.setBrightness(0)
oledExp.setTextColumns()

gpio_rled = onionGpio.OnionGpio(17)
gpio_gled = onionGpio.OnionGpio(16)
gpio_bled = onionGpio.OnionGpio(15)
gpio_rled.setOutputDirection(0)
gpio_gled.setOutputDirection(0)
gpio_bled.setOutputDirection(0)
time.sleep(0.25) #Blink white 1 second to confirm LED function

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

def blink_start():
    color_blink(0,0,1)
    
def blink_error():
    color_blink(1,0,0)
    color_blink(1,0,0)
    
def blink_success():
    color_blink(0,1,0)

def check_website(url, name, line) :
    oledExp.setCursor(line,0)
    try:
        get(url,timeout=5).text
        oledExp.write(name + " OK")
        blink_success() #All Good
    except:
        oledExp.write(name + " BAD")
        print ("HTTP Request Failed")
        blink_error()



while True:
    time.sleep(300)
    blink_start()
    oledExp.clear()
    #DNS Try
    oledExp.setCursor(0,0)
    try:
        res = resolver.Resolver()
        res.nameservers = ['10.0.0.10']
        answers = res.query('prafiles.in', lifetime=5)
        oledExp.write("DNS Good")
    except:
        oledExp.write("DNS Bad")
        color_blink(1,0,0)
        continue

    #Internet HTTP Try
    check_website('https://grafana.prafiles.in',"Personal",1)
    check_website('https://nl-dev.solulever.com',"NL-Dev",2)
    check_website('https://dev.solulever.com',"E2E",3)
    check_website('https://aalborg.solulever.com',"Aalborg",4)
    check_website('https://ep.solulever.com',"EP",5)

    #readings = get_interface_val('ppp0')
    #oledExp.setCursor(2,0)
    #oledExp.write("WAN Mbps Rx " + str (readings['rx_rate']) + " Tx " + str (readings['tx_rate']))
    #readings = get_interface_val('eth0')
    #oledExp.setCursor(3,0)
    #oledExp.write("ETH Mbps Rx " + str (readings['rx_rate']) + " Tx " + str (readings['tx_rate']))