import serial
import RPi.GPIO as GPIO
import time
import datetime
import logging

#Initialize LogFile
logging.basicConfig(filename='/root/cloynefrontdoor.log',level=logging.DEBUG)

# Set System Time
import subprocess
try:
	import ntplib
	client = ntplib.NTPClient()
	response = client.request('pool.ntp.org')
	date_time = subprocess.check_output('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)), shell=True)
	logging.info(date_time)
except:
	logging.info('Failed to Set System Time')


# Initialize GPIO
#GPIO drives optoisolator which in turns opens door
optoisolator_pin = 2
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setwarnings(False)
GPIO.setup(optoisolator_pin, GPIO.OUT) # OptoIsolator pin set as output
GPIO.output(optoisolator_pin, GPIO.LOW)# Initial state for Optoisolator : closed

def open_door():
	# Turn optoisolator on
	print 'Opening Door!'
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
	# TO DO CREATE DATABASE TO CHECK
	datetime.datetime.now() # check if valid for this academic semester
	return id_num > 0

def HID_initialize():
	HIDinitialized = False
	while(not HIDinitialized):
		try:
			HID = serial.Serial('/dev/ttyUSB0') # Open port at 9600,8,N,1, no timeout:
			return HID
		except:
			print 'Could not connect to HID CalID rfid reader'
			logging.info('Failed to Initialize HID serial connection')
			time.sleep(5)
	
# Initialize Serial Connection with HID KeyCard Reader
HID = HID_initialize()
	
def main():
	while(1):
		try:
			hex_string = HID.readline()
		except:
			HID = HID_initialize()
			continue
		id_num = calculate_id(hex_string)
		if( valid_ID(id_num)):
			open_door()
			logging.info([hex_string, id_num, 'GRANTED', datetime.datetime.now()])
		else:
			logging.info([hex_string, id_num, 'DENIED', datetime.datetime.now()])
	
main()
