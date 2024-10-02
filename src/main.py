# Library imports
from vex import *
import time

class ports:
    LeftTopPort =  Ports.PORT2
    LeftBtmPort =  Ports.PORT4
    RightTopPort = Ports.PORT1
    RightBtmPort = Ports.PORT3

class gears:
    RedGear = GearSetting.RATIO_36_1
    GreenGear = GearSetting.RATIO_18_1
    BlueGear = GearSetting.RATIO_6_1

class ctrl:
    controller = Controller()
    ActiveRange = FORWARD
    ActiveTurn = LEFT
    RightHori = controller.axis1
    RightVert = controller.axis2
    LeftVert = controller.axis3
    LeftHori = controller.axis4
    

# Brain should be defined by default
brain=Brain()

brain.screen.print("Hello V5")

# We want to dynamically change ports and active devices

# Lets Init our Motors
LeftTMtr = Motor(ports.LeftTopPort, gears.GreenGear, False)
LeftBMtr = Motor(ports.LeftBtmPort, gears.GreenGear, False)
RightTMtr = Motor(ports.RightTopPort, gears.GreenGear, True)
RightBMtr= Motor(ports.RightBtmPort, gears.GreenGear, True)

# These are the motor objects we use. They are MotorGroups which control serveral motors at oncce.
LeftMotor = MotorGroup(LeftTMtr,LeftBMtr)
RightMotor = MotorGroup(RightTMtr,RightBMtr)
Body = DriveTrain(LeftMotor,RightMotor)

def changeSpeed():
    range = ctrl.LeftVert.position()
    brain.screen.print(range)
    if range > 0:
        Body.set_drive_velocity(100, PERCENT)
        ctrl.ActiveRange = FORWARD
    elif range < 0:
        Body.set_drive_velocity(50, PERCENT)
        ctrl.ActiveRange = REVERSE
    else:
        Body.set_drive_velocity(0)
    range = ctrl.LeftHori.position()
    if range > 0:
        ctrl.ActiveTurn = LEFT
    elif range < 0:
        ctrl.ActiveTurn = RIGHT
    Body.set_turn_velocity(abs(range), PERCENT)

def move():
    changeSpeed()
    if ctrl.ActiveTurn == LEFT:
        Body.turn(LEFT)
    elif ctrl.ActiveTurn == RIGHT:
        Body.turn(RIGHT)
    if ctrl.ActiveRange == FORWARD:
        Body.drive(FORWARD)
    elif ctrl.ActiveRange == REVERSE:
        Body.drive(REVERSE)

def test():
    # We refer to the group of all the Motors as the Body    
    Body.set_drive_velocity(100, PERCENT)
    Body.drive_for(FORWARD, 12, INCHES)
    time.sleep(3)
    Body.drive_for(REVERSE, 12, INCHES)
    
while True:
     move()

# test()