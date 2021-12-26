import time
import onionGpio
from OmegaExpansion import oledExp
from requests import get
from dns import resolver
from datetime import datetime

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

flag_global_error = False

def color_blink(r,g,b,duration=0.25,sleep=0.25):
    #LED GPIO 1 means LOW and 0 means HIGH
    gpio_rled.setValue(1-r)
    gpio_gled.setValue(1-g)
    gpio_bled.setValue(1-b)
    if duration > 0: 
        time.sleep(duration)
        gpio_rled.setValue(1)
        gpio_gled.setValue(1)
        gpio_bled.setValue(1)
        time.sleep(sleep)

def led_start():
    global flag_global_error
    flag_global_error = False
    color_blink(0,0,1)
    
def led_error(blink=True):
    global flag_global_error
    flag_global_error = True
    
    color_blink(1,0,0)
    color_blink(1,0,0)

    if blink == False:
        color_blink(1,0,0,duration=-1)
    

def led_success(blink=True):
    color_blink(0,1,0)
    if blink == False:
        color_blink(0,1,0,duration=-1)


def check_website(url, name, line):
    oledExp.setCursor(line,0)
    try:
        get(url,timeout=5).text
        oledExp.write(name + " OK")
        led_success() #All Good
    except:
        oledExp.write(name + " BAD")
        print ("HTTP Request Failed")
        led_error()


while True:    
    led_start()
    oledExp.clear()

    time.sleep(300)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    oledExp.setCursor(0,0)
    oledExp.write(current_time)

    #DNS Try
    oledExp.setCursor(1,0)
    try:
        res = resolver.Resolver()
        res.nameservers = ['10.0.0.3']
        answers = res.query('prafiles.in', lifetime=5)
        oledExp.write("DNS Good")
    except:
        oledExp.write("DNS Bad")
        led_error()
        continue

    #Internet HTTP Try
    check_website('https://grafana.prafiles.in',"Personal",2)
    check_website('https://nl-dev.solulever.com',"NL-Dev",3)
    check_website('https://dev.solulever.com',"E2E",4)
    check_website('https://aalborg.solulever.com',"Aalborg",5)
    check_website('https://ep.solulever.com',"EP",6)

    if flag_global_error:
        led_error(blink=False)
    else:
        led_success(blink=False)

    #readings = get_interface_val('ppp0')
    #oledExp.setCursor(2,0)
    #oledExp.write("WAN Mbps Rx " + str (readings['rx_rate']) + " Tx " + str (readings['tx_rate']))
    #readings = get_interface_val('eth0')
    #oledExp.setCursor(3,0)
    #oledExp.write("ETH Mbps Rx " + str (readings['rx_rate']) + " Tx " + str (readings['tx_rate']))