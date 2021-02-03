from picamera import Picamera
from sense_hat import SenseHat
from time import sleep

# Create instance of SenseHat object
my_sensehat = SenseHat()
# Create instance of PiCamera object
camera = PiCamera()

# Initiliaze global constant values
ACCELERATION_THRESHOLD = 10
ORIENTATION_THRESHOLD = 30
FRIDGE_DOOR_OPEN = False
IMAGE_DIRECTORY = '/home/pi/Desktop/fridge_pictures/image'
image_counter = 0

# Main Function


def main():

    # Pull in global variables
    global FRIDGE_DOOR_OPEN
    global image_counter

    # Run the program - stop execution if the user presses Ctrl-C
    try:
        while True:

            # If the FRIDGE_DOOR_OPEN bool is still set to false
            if (not FRIDGE_DOOR_OPEN):
                orientation_data = get_orientation()

                pitch_value = orientation_data[0]
                roll_value = orientation_data[1]
                yaw_value = orientation_data[2]
                
                # If orientation detects that the fridge door has been opened
                if (yaw_value >= ORIENTATION_THRESHOLD):
                    # Update FRIDGE_DOOR_OPEN value
                    FRIDGE_DOOR_OPEN = True
                    
            else:
                # Call the detect_fridge_door_close function
                detect_fridge_door_close()
                # Call the take_picture function once the door has been closed
                take_picture()
                # Increment the image_counter variable
                image_counter += 1

    except (KeyboardInterrupt):
        print("Goodbye - Quitting Now")
        exit(0)

###################################################################################################

# Function for getting acceleration data from the sense hat


def get_acceleration():
    # Call the get_accelerometer_raw method of the SenseHat object
    acceleration = my_sensehat.get_accelerometer_raw()
    # Return the acceleration values from the acceleration dictionary in a tuple
    return (acceleration['x'], acceleration['y'], acceleration['z'])

# Function for getting orientation data from the sense hat


def get_orientation():
    # Call the get_orientation method of the SenseHat object
    orientation = my_sensehat.get_orientation()
    # Return the orientation values from the orientation dictionary in a tuple
    return (orientation['pitch'], orientation['roll'], orientation['yaw'])

# Function for taking a picture with the Pi Camera


def take_picture():
    global IMAGE_DIRECTORY
    # Create the image_filepath string
    image_filepath = IMAGE_DIRECTORY + image_counter + '.jpg'
    # Take a picture
    camera.start_preview()
    sleep(2)
    camera.capture(image_filepath)

# Function to determine when the fridge door has been closed for an acceptable amount of time


def detect_fridge_door_close():
    global FRIDGE_DOOR_OPEN
    global ACCELERATION_THRESHOLD
    global ORIENTATION_THRESHOLD

    seconds_passed = 0

    while (FRIDGE_DOOR_OPEN):
        acceleration_data = get_acceleration()
        orientation_data = get_orientation()
        
        x_acceleration = acceleration_data[0]
        y_acceleration = acceleration_data[1]
        z_acceleration = acceleration_data[2]
        
        pitch_value = orientation_data[0]
        roll_value = orientation_data[1]
        yaw_value = orientation_data[2]
                    
        #if yaw > ORIENTATION_THRESHOLD, 
        
        if (yaw_value >= ORIENTATION_THRESHOLD):
            FRIDGE_DOOR_OPEN = False

            while (seconds_passed < 10 and (not FRIDGE_DOOR_OPEN)):
                orientation_data2 = get_orientation()
                yaw_value2 = orientation_data2[2]

                if (yaw_value2 >= ORIENTATION_THRESHOLD):
                    seconds_passed = 0
                    FRIDGE_DOOR_OPEN = True
                else:
                    sleep(1)
                    seconds_passed += 1


if __name__ == "__main__":
    main()
