
# Initialize the API
api = dType.load()
if api is None:
    print("Failed to load Dobot API!")
else:
    print("Dobot API loaded successfully!")




import DobotDllType as dType

# Initialize the connection to Dobot
api = dType.load()
if api is None:
    print("Failed to load Dobot API!")
    exit()

# Parameter Setup
count_r = None
count_g = None
count_b = None
x = None
y = None
z = None
color_list = None
r = None
g = None
b = None
home_x = None
home_y = None
home_z = None

# Functions
def move_to_trash():
    global x, y, z
    get_coordinates()
    dType.SetPTPCmdEx(api, 0, x, y, z, 0, 1)
    dType.SetEndEffectorSuctionCupEx(api, 0, 1)

def count_by_color():
    global color_list, r, count_r, g, count_g, b, count_b
    if color_list == r:
        count_r = count_r + 1
    elif color_list == g:
        count_g = count_g + 1
    elif color_list == b:
        count_b = count_b + 1

def set_up():
    global count_r, count_g, count_b, home_x, home_y, home_z
    dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)
    dType.SetInfraredSensor(api, 1, 3, 1)
    dType.SetInfraredSensor(api, 1, 2, 1)
    dType.SetPTPJumpParamsEx(api, 20, 100, 1)
    count_r = 0
    count_g = 0
    count_b = 0
    home_x = 253.898
    home_y = 11.621
    home_z = 135.3884

def color_check():
    global r, g, b, color_list
    dType.SetColorSensor(api, 1, 1, 1)
    dType.dSleep(1000)
    r = dType.GetColorSensorEx(api, 0)
    g = dType.GetColorSensorEx(api, 1)
    b = dType.GetColorSensorEx(api, 2)
    color_list = max([r, g, b])
    dType.SetColorSensor(api, 0, 1, 1)

def get_coordinates():
    global color_list, r, x, y, z
    if color_list == r:
        x = 95.1635
        y = -245.3083
        z = 38.3771
    else:
        x = 112.6687
        y = -166.282
        z = 43.768

def photosensor():
    return dType.GetInfraredSensor(api, 3)[0]

def pick_and_check():
    dType.SetPTPCmdEx(api, 0, 230.3866, -71.8092, 11.4657, 0, 1)
    dType.SetEndEffectorSuctionCupEx(api, 1, 1)
    dType.SetPTPCmdEx(api, 0, 297.6839, -41.9456, 18.3578, 0, 1)

def print2():
    global count_r, count_g, count_b
    print('red', count_r)
    print('green', count_g)
    print('blue', count_b)

# Main Loop
set_up()
while dType.GetInfraredSensor(api, 2)[0] == 0:
    pass
while True:
    current_pose = dType.GetPose(api)
    dType.SetPTPCmdEx(api, 2, home_x, home_y, home_z, current_pose[3], 1)
   
