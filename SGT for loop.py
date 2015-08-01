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

BUTTON = 5

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

for port_sol in range(1,5):
    # write resistance from a port_sol to cell
    port_sol = 1
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print('Attach banana plugs to firing line % for port guns' %i port_sol)
    print('Press green button when done')
    GPIO.wait_for_edge(BUTTON, GPIO.FALLING)
    adc.read_voltage(1)
    calccurrent(v1)
    Pws['F37'] = calcresistance(v1)
    GPIO.cleanup(BUTTON)
    port_sol += 1


for port_tcoil in range(1,5):
    port_tcoil = 1
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print('Attach banana plugs to detect line % for port guns' %i port_tcoil)
    print('Press green button when done')
    GPIO.wait_for_edge(BUTTON, GPIO.FALLING)
    adc.read_voltage(1)
    calccurrent(v1)
    Pws['F37'] = calcresistance(v1)
    GPIO.cleanup(BUTTON)
    port_tcoil += 1

for stbd_sol in range(1,5):
    # write resistance from a port_sol to cell
    port_sol = 1
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print('Attach banana plugs to firing line % for stbd guns' %i stbd_sol)
    print('Press green button when done')
    GPIO.wait_for_edge(BUTTON, GPIO.FALLING)
    adc.read_voltage(1)
    calccurrent(v1)
    Pws['F37'] = calcresistance(v1)
    GPIO.cleanup(BUTTON)
    stbd_sol += 1

for stbd_tcoil in range(1,5):
    stbd_tcoil = 1
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print('Attach banana plugs to detect line % for stbd guns' %i stbd_tcoil)
    print('Press green button when done')
    GPIO.wait_for_edge(BUTTON, GPIO.FALLING)
    adc.read_voltage(1)
    calccurrent(v1)
    Pws['F37'] = calcresistance(v1)
    GPIO.cleanup(BUTTON)
    stbd_tcoil += 1