from picamera import PiCamera
from sense_hat import SenseHat
from time import sleep

# Create instance of SenseHat object
sense = SenseHat()
# Create instance of PiCamera object
camera = PiCamera()

# Initialize orientation
initial_orientation = sense.get_orientation()

# Initiliaze global constant values
ACCELERATION_THRESHOLD = 10
ORIENTATION_THRESHOLD = initial_orientation['yaw']
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
                
                print (orientation_data)
                sleep(1)
                
                # If orientation detects that the fridge door has been opened
                if (yaw_value > ORIENTATION_THRESHOLD+10 or yaw_value < ORIENTATION_THRESHOLD-10):
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

# Function for getting orientation data from the sense hat


def get_orientation():
    # Call the get_orientation method of the SenseHat object
    orientation = sense.get_orientation()
    # Return the orientation values from the orientation dictionary in a tuple
    return (orientation['pitch'], orientation['roll'], orientation['yaw'])

# Function for taking a picture with the Pi Camera


def take_picture():
    global IMAGE_DIRECTORY
    # Create the image_filepath string
    image_filepath = IMAGE_DIRECTORY + str(image_counter) + '.jpg'
    # Take a picture
    camera.rotation = 270
    sense.clear((255,255,255))
    camera.start_preview()
    sleep(2)
    camera.capture(image_filepath)
    camera.stop_preview()
    sense.clear()

# Function to determine when the fridge door has been closed for an acceptable amount of time


def detect_fridge_door_close():
    global FRIDGE_DOOR_OPEN
    global ACCELERATION_THRESHOLD
    global ORIENTATION_THRESHOLD

    seconds_passed = 0

    while (FRIDGE_DOOR_OPEN):
        orientation_data = get_orientation()
                
        pitch_value = orientation_data[0]
        roll_value = orientation_data[1]
        yaw_value = orientation_data[2]
                    
        #if yaw > ORIENTATION_THRESHOLD, 
        
        if (yaw_value < ORIENTATION_THRESHOLD+10 or yaw_value > ORIENTATION_THRESHOLD-10):
            FRIDGE_DOOR_OPEN = False
            print("checking yaw against threshold.")

            while (seconds_passed < 3 and (not FRIDGE_DOOR_OPEN)):
                orientation_data2 = get_orientation()
                yaw_value2 = orientation_data2[2]

                if (yaw_value2 > ORIENTATION_THRESHOLD+10 or yaw_value < ORIENTATION_THRESHOLD-10):
                    seconds_passed = 0
                    FRIDGE_DOOR_OPEN = True
                    print("Fridge door open = true")
                    sleep(1)
                else:
                    sleep(1)
                    print("sleeping for a sec...")
                    seconds_passed += 1


if __name__ == "__main__":
    main()
