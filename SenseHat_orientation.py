from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

while (True):
    orientation = sense.get_orientation()
    print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
    sleep(1)
    