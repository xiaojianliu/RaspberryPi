# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:32:13 2015
@author: bling
"""

import os, glob, time
import serial

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

transmit = 'ON' # ON, OFF

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c*1000, temp_f*1000

while True:
    #print("temp C=%f\ttemp F=%f" % read_temp())
    # Send data every 10 minutes.
    time.sleep(300)

    mes = "%.6d0%.6d" % read_temp()
    print mes
    if transmit == 'ON':
        #ser=serial.Serial('COM16', 9600) # in Windows
        ser=serial.Serial('/dev/ttyUSB0',9600) # linux
        #print 'Open serial port.'
        # send the data
        time.sleep(1)
        ser.writelines('\n')
        time.sleep(1)
        ser.writelines('\n')
        time.sleep(1)
        ser.writelines('yab'+'\n') # Force the given message to idle.
        time.sleep(5)
        ser.writelines('\n')
        time.sleep(1)
        ser.writelines('\n')
        time.sleep(1)
        #ser.writelines('ylb9'+meandepth+rangedepth+time_len+meantemp+sdeviatemp+'\n')
        ser.writelines('ylb90'+mes+'\n')
        #time.sleep(3)
        #print 'Sending data: '+meandepth+rangedepth+time_len+meantemp+sdeviatemp
        #print datetime.now()
        time.sleep(2) # 1100s 18 minutes
        ser.close() # close port
        time.sleep(288)
    except:
        print 'Can not send data.'
