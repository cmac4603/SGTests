#!/usr/bin/python

from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import os
import time
import RPi.GPIO as GPIO

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 12)

# Configure the GPIO pins
BUTTON_PIN = 24
EXIT_BUTTON = 23
END_BUTTON = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(EXIT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(END_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_press = GPIO.input(BUTTON_PIN)

# voltage reading from channel 1 (v_supply) / 2, used for calccurrent()
v_i = (adc.read_voltage(1)) /2
# voltage reading from channel 1 (v_supply), used for calccurrent()
v1 = (adc.read_voltage(1))

# calculates current from channel labelled 'v_i'
# i = current calculated from adc channel 1 defined globally
def calccurrent(inval):
    global i
    i = ((inval) - v_i) / 0.066
    return ((inval) - v_i) / 0.066
    
# calculates resistance using two global variables
# voltage(V)/current(mA) = r
def calcresistance(volts):
    return volts / (i / 1000)

def quit_program(channel):
    print('Exit button pressed, quiting program...')
    GPIO.cleanup()
    time.sleep(1)
    exit()


def start():
    print('Sleeve Gun Tester v.0 2015')
    print('Press the green button for voltage, current, and resistance...')
    print('Or the red button to quit at anytime.')
    GPIO.add_event_detect(EXIT_BUTTON, GPIO.FALLING, callback=quit_program)
    try:
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        # print voltage, current & resistance on ch1
        print ('Voltage V: %02f' % adc.read_voltage(1), 'V')
        print ('Current I: %02f' % calccurrent(v1), 'mA')
        print ('Resistance R: %02f' % calcresistance(v1), 'ohms')
        # print voltage, current & resistance on ch2
        print ('Voltage V: %02f' % adc.read_voltage(2), 'V')
        print ('Current I: %02f' % calccurrent(v2), 'mA')
        print ('Resistance R: %02f' % calcresistance(v2), 'ohms')
        # print voltage, current & resistance on ch3
        print ('Voltage V: %02f' % adc.read_voltage(3), 'V')
        print ('Current I: %02f' % calccurrent(v3), 'mA')
        print ('Resistance R: %02f' % calcresistance(v3), 'ohms')
        # print voltage, current & resistance on ch4
        print ('Voltage V: %02f' % adc.read_voltage(4), 'V')
        print ('Current I: %02f' % calccurrent(v4), 'mA')
        print ('Resistance R: %02f' % calcresistance(v4), 'ohms')
        # print voltage, current & resistance on ch5
        print ('Voltage V: %02f' % adc.read_voltage(5), 'V')
        print ('Current I: %02f' % calccurrent(v5), 'mA')
        print ('Resistance R: %02f' % calcresistance(v5), 'ohms')
        # print voltage, current & resistance on ch6
        print ('Voltage V: %02f' % adc.read_voltage(6), 'V')
        print ('Current I: %02f' % calccurrent(v6), 'mA')
        print ('Resistance R: %02f' % calcresistance(v6), 'ohms')
        # print voltage, current & resistance on ch7
        print ('Voltage V: %02f' % adc.read_voltage(7), 'V')
        print ('Current I: %02f' % calccurrent(v7), 'mA')
        print ('Resistance R: %02f' % calcresistance(v7), 'ohms')
        # print voltage, current & resistance on ch8
        print ('Voltage V: %02f' % adc.read_voltage(8), 'V')
        print ('Current I: %02f' % calccurrent(v8), 'mA')
        print ('Resistance R: %02f' % calcresistance(v8), 'ohms')
    finally:
        print('Press the red button to exit the program...')
        GPIO.wait_for_edge(END_BUTTON, GPIO.FALLING)
        time.sleep(0.5)
        GPIO.cleanup()
        quit_program()

start()
