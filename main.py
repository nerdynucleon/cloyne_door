import serial
import RPi.GPIO as GPIO
import time
import logging

#Initialize LogFile
logging.basicConfig(filename='door.log',level=logging.DEBUG)

# Set System Time
import subprocess
#import os
try:
	import ntplib
	client = ntplib.NTPClient()
	response = client.request('pool.ntp.org')
	date_time = subprocess.check_output('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)), shell=True)
	#date_time = os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
	logging.info(date_time)
except:
	logging.info('Failed to Set System Time')


# Initialize GPIO
#GPIO drives optoisolator which in turns opens door
optoisolator_pin = 2
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(optoisolator_pin, GPIO.OUT) # OptoIsolator pin set as output
GPIO.output(optoisolator_pin, GPIO.LOW)# Initial state for Optoisolator : closed

# Initialize Serial Connection with HID KeyCard Reader
HID = serial.Serial('/dev/ttyUSB0') # Open port at 9600,8,N,1, no timeout:

def open_door():
	# Turn optoisolator on
	GPIO.output(optoisolator_pin, GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(optoisolator_pin, GPIO.LOW)

def calculate_id(hex_string):
	#TO DO ADD CHECKSUM
	try:
		id_value = int(bin(int(hex_string[7:-4], 16))[:-1],2)
	except:
		id_value = -1
	return id_value

def valid_ID(id_num):
	return id_num > 0

def main():
	while(1):
		hex_string = HID.readline()
		id_num = calculate_id(hex_string)
		if( valid_ID(id_num)):
			open_door()
			logging.info([hex_string, id_num, 'GRANTED'])
		else:
			logging.info([hex_string, id_num, 'DENIED'])
	
main()
