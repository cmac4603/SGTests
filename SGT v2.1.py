#!/usr/bin/python

from datetime import date
from openpyxl import load_workbook
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import os
import time
import RPi.GPIO as GPIO

today = date.today()

wb = load_workbook('SGT_Blank.xlsx')
Pws = wb.get_sheet_by_name("Port")
Sws = wb.get_sheet_by_name("Stbd")

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 12)

# Configure the GPIO pins
BUTTON1 = 5
BUTTON2 = 6
BUTTON3 = 13
BUTTON4 = 19
EXIT_BUTTON = 23
END_BUTTON = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(EXIT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(END_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

def pre_exit(channel):
    print('Exit button pressed, quiting program...')
    print('Note, nothing saved...')
    GPIO.cleanup()
    time.sleep(1)
    exit()

def quit_program():
    print('Exit button pressed, quiting program...')
    GPIO.cleanup()
    time.sleep(1)
    exit()


def start():
    os.system('clear')
    print('Sleeve Gun Tester v2.0 2015')
    print('Note you can press the red button anytime to quit')
    GPIO.add_event_detect(EXIT_BUTTON, GPIO.FALLING, callback=pre_exit)
    try:
        # write resistance from S1 to cell
        print('Attach banana plugs to firing line 1 for port guns')
        print('Press green button when done')
        GPIO.wait_for_edge(BUTTON1, GPIO.FALLING)
        adc.read_voltage(1)
        calccurrent(v1)
        Pws['F37'] = calcresistance(v1)
        print('Solenoid resistance recorded')
        time.sleep(1)
        # write resistance from S2 to cell
        os.system('clear')
        print('Attach banana plugs to firing line 2 for port guns')
        print('Press green button when done')
        GPIO.wait_for_edge(BUTTON2, GPIO.FALLING)
        adc.read_voltage(1)
        calccurrent(v1)
        Pws['F38'] = calcresistance(v1)
        print('Solenoid resistance recorded')
        time.sleep(1)
        # write resistance from S3 to cell
        os.system('clear')
        print('Attach banana plugs to firing line 3 for port guns')
        print('Press green button when done')
        GPIO.wait_for_edge(BUTTON3, GPIO.FALLING)
        adc.read_voltage(1)
        calccurrent(v1)
        Pws['F39'] = calcresistance(v1)
        print('Solenoid resistance recorded')
        time.sleep(1)
        # write resistance from S4 to cell
        os.system('clear')
        print('Attach banana plugs to firing line 4 for port guns')
        print('Press green button when done')
        GPIO.wait_for_edge(BUTTON4, GPIO.FALLING)
        adc.read_voltage(1)
        calccurrent(v1)
        Pws['F40'] = calcresistance(v1)
        print('Solenoid resistance recorded')
        time.sleep(1)
    finally:
        os.system('clear')
        print('Press the blue button to save to workbook & exit the program')
        print('Press the red button to just quit')
        GPIO.wait_for_edge(END_BUTTON, GPIO.FALLING)
        wb.save('SGT_rename.xlsx')
        print('Workbook saved as SGT_rename.xlsx')
        time.sleep(0.5)
        quit_program()

start()
