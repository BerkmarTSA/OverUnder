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
    Chain = Ports.PORT19
    Extra4 = Ports.PORT20

class gears:
    RedGear = GearSetting.RATIO_36_1
    GreenGear = GearSetting.RATIO_18_1
    BlueGear = GearSetting.RATIO_6_1

class ctrl:
    controller = Controller()
    ActiveRange = FORWARD
    ActiveTurn = LEFT
    ActiveRArms = FORWARD
    ActiveLArms = FORWARD
    RightHori = controller.axis1
    RightVert = controller.axis2
    LeftVert = controller.axis3
    LeftHori = controller.axis4
    XBtn = controller.buttonX
    BBtn = controller.buttonB
    RSb = controller.buttonR1
    RTr = controller.buttonR2
    

# Brain should be defined by default
brain=Brain()

brain.screen.print("Hello V5")

# We want to dynamically change ports and active devices

# Lets Init our Motors
LeftTMtr = Motor(ports.LeftTopPort, gears.GreenGear, False)
LeftBMtr = Motor(ports.LeftBtmPort, gears.GreenGear, False)
RightTMtr = Motor(ports.RightTopPort, gears.GreenGear, True)
RightBMtr= Motor(ports.RightBtmPort, gears.GreenGear, True)
LeftArm= Motor(ports.LeftARM, gears.GreenGear, False)
RightArm= Motor(ports.RightARM, gears.GreenGear, False)
Chain= Motor(ports.Chain, gears.GreenGear, False)
# These are the motor objects we use. They are MotorGroups which control serveral motors at oncce.
LeftMotor = MotorGroup(LeftTMtr,LeftBMtr)
RightMotor = MotorGroup(RightTMtr,RightBMtr)
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
        ctrl.ActiveRange = FORWARD
    elif range < 0:
        ctrl.ActiveRange = REVERSE
    Body.drive(ctrl.ActiveRange, Body.velocity())
    
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

def rightVertMove():
    range = ctrl.RightVert.position()
    brain.screen.print("\n",range)
    print("Vert Axis: ", range)
    if range > 0:
        Body.set_drive_velocity(range, PERCENT)
    elif range < 0:
        Body.set_drive_velocity(abs(range), PERCENT)
    else:
        Body.set_drive_velocity(0)

def armMove(range):
    # TODO: Don't limit the range of the arms!!
    brain.screen.print("/n", range)
    print("Right Arm Axis: ", range)
    print(LeftArm.position())
    print(RightArm.position())
    # Bring the Arm Up
    if range == "X":
        RightArm.set_velocity(100, PERCENT)
        LeftArm.set_velocity(100, PERCENT)
        ctrl.ActiveRArms = FORWARD
        ctrl.ActiveLArms = REVERSE
        RightArm.spin_to_position(245, DEGREES, 100, PERCENT, False)
        LeftArm.spin_to_position(-245, DEGREES, 100, PERCENT, False)
    # Bring the Arm Down
    elif range == "B":
        RightArm.set_velocity(100, PERCENT)
        LeftArm.set_velocity(100, PERCENT)
        ctrl.ActiveRArms = REVERSE
        ctrl.ActiveLArms = FORWARD
        RightArm.spin_to_position(-10, DEGREES, 100, PERCENT, False)
        LeftArm.spin_to_position(10, DEGREES, 100, PERCENT, False)
    else:
        RightArm.set_velocity(0)
        LeftArm.set_velocity(0)

# TODO: Check chain spinning     
def chainMove(input):
    if (input == "R1"):
        print("Right Shoulder button pressed")
        Chain.set_velocity(100, PERCENT)
        Chain.spin(FORWARD)
    elif (input == "R2"):
        print("Right trigger pressed")
        Chain.set_velocity(100, PERCENT)
        Chain.spin(REVERSE)
    else:
        print("Buttons released")
        Chain.stop()
    # Arms.spin(FORWARD)
    

# ? We don't want to reset the arm position (as per moses's request)
RightArm.reset_position()
LeftArm.reset_position()
ctrl.LeftVert.changed(leftVertMove)
ctrl.LeftHori.changed(leftHoriMove) 
ctrl.RightVert.changed(rightVertMove)
ctrl.XBtn.pressed(armMove, ("X",))
ctrl.BBtn.pressed(armMove, ("B",))
ctrl.RSb.pressed(chainMove, ("R1",))
ctrl.RTr.pressed(chainMove, ("R2",))
ctrl.BBtn.released(armMove, ("None",))
ctrl.XBtn.released(armMove, ("None",))
ctrl.RTr.released(chainMove, ("None",))
ctrl.RSb.released(chainMove, ("None",))
# ctrl.RightVert.changed(rightVertPower)
# test()
