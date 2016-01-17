#!/usr/bin/python

import threading
import time
import logging
import RPi.GPIO as GPIO
import socket, os, os.path

#Initializing logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
					    format='[%(asctime)s %(threadName)s] %(message)s',
	                                    datefmt='%H:%M:%S')

# Removing socket before start (if exists)

if os.path.exists("/tmp/relay_socket"):
	os.remove("/tmp/relay_socket")

led_pin = 18
button_pin = 24
relay1_pin = 23

# Configure the Pi to use the BCM (Broadcom) pin names
GPIO.setmode(GPIO.BCM)
# Configure the output pins
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(relay1_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(relay1_pin, True)# Starts relay1_pin active

#This class controlls the raspberry GPIO
class GPIOManager(threading.Thread):
	def __init__(self):
		logger.info("[GPIO Manager] Created")
		threading.Thread.__init__(self)
		self.status = 0
		self.daemon = True  # OK for main to exit even if instance is still running
		self.paused = True  # start out paused
		self.state = threading.Condition()

	def run(self):
		logger.info("[GPIO Manager] Running")
		while True:
			with self.state:
				if self.paused:
					self.state.wait() # block until notified
			if self.button_pressed():
				logger.info("[GPIO Manager] Button pressed")
				if self.status == 0:
					self.status = 1
				else:
					self.status = 0

	def resume(self):
		logger.info("[GPIO Manager] Resumed")
		with self.state:
			self.paused = False
			self.state.notify()  # unblock self if waiting

	def pause(self):
		logger.info("[GPIO Manager] Paused")
		with self.state:
			self.paused = True  # make self block and wait

	def button_pressed(self):
		if not GPIO.input( button_pin ):
			while not GPIO.input( button_pin ):
				pass
			return 1
		else:
			return 0

#This class controlls the socket server
class ServerManager(threading.Thread):
	def __init__(self):
		logger.info("[Server Manager] Created")
		threading.Thread.__init__(self)
		self.status = 0
		self.daemon = True  # OK for main to exit even if instance is still running
		self.paused = True  # start out paused
		self.state = threading.Condition()
		# Sockets stuff
		logger.info("[Server Manager] Opening IPC connection")
		self.serverRx = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		self.serverRx.bind("/tmp/serverRx_socket")
		self.serverTx = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		
	def run(self):
		logger.info("[Server Manager] Listening ")
		while True:
			with self.state:
				if self.paused:
						self.state.wait() # block until notified
			
			datagram, addr = self.serverRx.recvfrom(1024)
			logger.info("[Server Manager] Receiving ")
			if not datagram:
				break
			else:
				logger.info("[Server Manager] Control message received (%s)", datagram)
				if "ON" == datagram:
					self.status = 1
				elif "OFF" == datagram:
					self.status = 0
				elif "STATUS" == datagram:
					logger.info("[Server Manager] Connecting...")
					self.serverTx.connect("/tmp/clientRx_socket")
					self.serverTx.send(str(self.status))
				else: 
					logger.info("[Server Manager] Unknown message received")
				
				
			

	def resume(self):
		logger.info("[Server Manager] Resumed")
		with self.state:
			self.paused = False
			self.state.notify()  # unblock self if waiting

	def pause(self):
		logger.info("[Server Manager] Paused")
		with self.state:
			self.paused = True  # make self block and wait


##### Main functions ######
def blink():
	blinks = 0
	while (blinks < 5):
		GPIO.output(led_pin, True)
       		time.sleep(0.3)
		GPIO.output(led_pin, False)
		time.sleep(0.3)
		blinks += 1
	return

def switch_status( status ):
	blink()
	if ( status == 0 ):
		logger.info("[GPIO Main] Turning ON")
		GPIO.output(relay1_pin, False)
		GPIO.output(led_pin, True)
		return 1 
	else:
		logger.info("[GPIO Main] Turning OFF")
		GPIO.output(relay1_pin, True)
		GPIO.output(led_pin, False)
		return 0  

status = 0
gpio_status = 0
server_status = 0

gpio = GPIOManager()
server = ServerManager()

# Calls run() method
gpio.start()
server.start()

gpio.resume()
server.resume()

try:
		
	while True:	
		gpio_status = gpio.status
		server_status = server.status

		if status != gpio_status:
			logger.info("[Main] Status change from GPIO")
			gpio.pause()
			server.pause()
			status = switch_status( status )
			server.status = status
			gpio.resume()
			server.resume()
		elif status != server_status:
			logger.info("[Main] Status change from Server")
			gpio.pause()
			server.pause()
			status = switch_status( status )
			gpio.status = status
			gpio.resume()
			server.resume()
	 		
finally:  	
	print("Cleaning up")
	GPIO.cleanup()
	
	print("Close and removing connection")
	server.serverRx.close()
	os.remove("/tmp/serverRx_socket")
	server.serverTx.close()

