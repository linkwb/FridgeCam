from sense_hat import SenseHat
from time import sleep

my_sensehat = SenseHat()

while (True):
	acceleration = my_sensehat.get_accelerometer_raw()
	print(acceleration['y'])
	sleep(1)
