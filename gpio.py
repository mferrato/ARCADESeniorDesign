## this is GPIO implementation
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(2, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
while True:
	GPIO.output(11, GPIO.LOW)
	GPIO.output(12, GPIO.HIGH)
else:
	GPIO.cleanup()
