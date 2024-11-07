# Import necessary libraries
import time
from DobotDLL import dType  # Assuming you're using the Dobot SDK DLL (ensure it's properly installed and accessible)

# Initialize Dobot API
api = dType.Load()  # Load the Dobot API (ensure the Dobot device is connected)

# Global variables initialization
x = None
y = None
z = None
r = None
color_list = None
g = None
home_x = None
home_y = None
home_z = None
b = None

# Function to move to trash
def move_to_trash():
    global x, y, z
    get_coordinates()  # Get the coordinates based on detected color
    dType.SetPTPCmdEx(api, 0, x, y, z, 0, 1)  # Move to trash position
    dType.SetEndEffectorSuctionCupEx(api, 0, 1)  # Activate suction cup to pick item

# Function to set up the robot (initialization)
def set_up():
    global x, y, z, home_x, home_y, home_z
    # Set parameters for the end effector and sensors
    dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)
    dType.SetInfraredSensor(api, 1, 3, 1)  # Enable infrared sensor 3
    dType.SetInfraredSensor(api, 1, 2, 1)  # Enable infrared sensor 2
    dType.SetPTPJumpParamsEx(api, 20, 100, 1)  # Set PTP jump parameters

    # Initialize position variables
    x = 0
    y = 0
    z = 0
    home_x = 253.898
    home_y = 11.621
    home_z = 135.3884  # Home position coordinates for the robot

# Function to check the color detected by the sensor
def color_check():
    global r, g, b, color_list
    # Turn on the color sensor and read the values for RGB
    dType.SetColorSensor(api, 1, 1, 1)
    time.sleep(1)  # Wait for sensor to stabilize

    # Get RGB sensor values
    r = dType.GetColorSensorEx(api, 0)
    g = dType.GetColorSensorEx(api, 1)
    b = dType.GetColorSensorEx(api, 2)

    # Determine which color has the highest value and store it
    color_list = max([r, g, b])
    dType.SetColorSensor(api, 0, 1, 1)  # Reset color sensor

# Function to get coordinates based on detected color
def get_coordinates():
    global color_list, r, x, y, z, g
    if color_list == r:
        # Red color detected, set coordinates for red
        x = 95.1635
        y = -245.3083
        z = 38.3771
    elif color_list == g:
        # Green color detected, set coordinates for green
        x = 112.6687
        y = -166.282
        z = 43.768
    else:
        # Other color detected, set coordinates for other (likely blue)
        x = 123.2865
        y = 179.2649
        z = 55.0338

# Function to read the photosensor (infrared sensor)
def photosensor():
    return dType.GetInfraredSensor(api, 3)[0]  # Return the value of infrared sensor 3

# Function for pick and check procedure
def pick_and_check():
    # Move to pick position
    dType.SetPTPCmdEx(api, 0, 230.3866, -71.8092, 11.4657, 0, 1)
    dType.SetEndEffectorSuctionCupEx(api, 1, 1)  # Activate suction cup (pick object)
    # Move to check position
    dType.SetPTPCmdEx(api, 0, 297.6839, -41.9456, 18.3578, 0, 1)

# Main program setup
set_up()

# Wait for the photosensor to detect the object (sensor 2)
while dType.GetInfraredSensor(api, 2)[0] == 0:
    pass  # Continue looping until the sensor detects an object

# Main loop: Continuously perform actions
while True:
    current_pose = dType.GetPose(api)  # Get current pose of the robot
    dType.SetPTPCmdEx(api, 2, home_x, home_y, home_z, current_pose[3], 1)  # Move to home position
    
    # Wait for the photosensor to detect the object (sensor 3)
    while photosensor() != 1:
        # Move motor until object is detected
        STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0  # Steps per circle for motor
        MM_PER_CRICLE = 3.1415926535898 * 36.0  # MM per circle
        vel = 50 * STEP_PER_CRICLE / MM_PER_CRICLE  # Motor velocity calculation
        dType.SetEMotorEx(api, 0, 1, int(vel), 1)  # Activate motor
        
    # Stop the motor after detecting the object
    STEP_PER_CRICLE = 360.0 / 1.8 * 10.0 * 16.0
    MM_PER_CRICLE = 3.1415926535898 * 36.0
    vel = 0 * STEP_PER_CRICLE / MM_PER_CRICLE  # Stop velocity
    dType.SetEMotorEx(api, 0, 0, int(vel), 1)  # Deactivate motor
    
    # Perform pick, check, and move to trash
    pick_and_check()
    color_check()
    move_to_trash()

# Optionally: Clean up and release the Dobot API connection
dType.Release(api)
