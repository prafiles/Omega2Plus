import os
import time
from requests import get


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