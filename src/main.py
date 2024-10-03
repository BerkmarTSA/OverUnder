# Library imports
from vex import *
import time

class ports:
    LeftTopPort =  Ports.PORT2
    LeftBtmPort =  Ports.PORT4
    RightTopPort = Ports.PORT1
    RightBtmPort = Ports.PORT3
    RightARM = Ports.PORT11
    LeftARM = Ports.PORT12
    Extra3 = Ports.PORT19
    Extra4 = Ports.PORT20

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
LeftArm= Motor(ports.LeftARM, gears.GreenGear)
RightArm= Motor(ports.RightARM, gears.GreenGear)
# These are the motor objects we use. They are MotorGroups which control serveral motors at oncce.
LeftMotor = MotorGroup(LeftTMtr,LeftBMtr)
RightMotor = MotorGroup(RightTMtr,RightBMtr)
Arms= MotorGroup(LeftArm,RightArm)
Body = DriveTrain(LeftMotor,RightMotor)

def test():
    # We refer to the group of all the Motors as the Body    
    Body.set_drive_velocity(100, PERCENT)
    Body.drive_for(FORWARD, 12, INCHES)
    time.sleep(3)
    Body.drive_for(REVERSE, 12, INCHES)

def leftVertMove():
    range = ctrl.LeftVert.position()
    brain.screen.print("\n",range)
    print("Vert Axis: ", range)
    if range > 0:
        Body.set_drive_velocity(100, PERCENT)
        ctrl.ActiveRange = FORWARD
    elif range < 0:
        Body.set_drive_velocity(100, PERCENT)
        ctrl.ActiveRange = REVERSE
    else:
        Body.set_drive_velocity(0)
    Body.drive(ctrl.ActiveRange)

def leftHoriMove():
    range = ctrl.LeftHori.position()
    brain.screen.print("\n",range)
    print("Horizon Axis: ", range)
    if range > 0:
        ctrl.ActiveTurn = RIGHT
    elif range < 0:
        ctrl.ActiveTurn = LEFT
    Body.set_turn_velocity(abs(range / 2), PERCENT)
    Body.turn(ctrl.ActiveTurn)

def armMove():
    # TODO: Limit the range of the arms!!
    range = ctrl.RightVert.position()
    brain.screen.print("/n", range)
    print("Right Arm Axis: ", range)
    if range > 0:
        Arms.set_velocity((range / 2), PERCENT)
    elif range < 0:
        Arms.set_velocity((Arms.velocity() - (abs(range))) / 2)
    Arms.spin(FORWARD)
    


# Initially reset the arms

ctrl.LeftVert.changed(leftVertMove)
ctrl.LeftHori.changed(leftHoriMove)
ctrl.RightVert.changed(armMove)
# test()
