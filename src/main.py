# Library imports
from vex import *
import time

## CLASSES

class ports:
    LeftTopPort =  Ports.PORT2
    LeftBtmPort =  Ports.PORT4
    RightTopPort = Ports.PORT1
    RightBtmPort = Ports.PORT3
    RightARM = Ports.PORT11
    LeftARM = Ports.PORT12
    Chain = Ports.PORT19
    Elevator = Ports.PORT20

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
    LSb = controller.buttonL1
    LTr = controller.buttonL2

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
Elevator= Motor(ports.Elevator, gears.GreenGear, False)
# These are the motor objects we use. They are MotorGroups which control serveral motors at oncce.
LeftMotor = MotorGroup(LeftTMtr,LeftBMtr)
RightMotor = MotorGroup(RightTMtr,RightBMtr)
Body = DriveTrain(LeftMotor,RightMotor)


## DEFINITIONS
def test():
    # We refer to the group of all the Motors as the Body    
    Body.set_drive_velocity(100, PERCENT)
    Body.drive_for(FORWARD, 12, INCHES)
    time.sleep(3)
    Body.drive_for(REVERSE, 12, INCHES)

def leftVertMove():
    range = ctrl.RightVert.position()
    LRange = ctrl.LeftHori.position()
    brain.screen.print("\n",range)
    print("Vert Axis: ", range)
    if range < 0:
        Body.set_drive_velocity(abs(range), PERCENT)
        ctrl.ActiveRange = FORWARD
        if (LRange > 0):
            ctrl.ActiveTurn = RIGHT
            Body.set_turn_velocity(abs(LRange / 2), PERCENT)
            Body.turn(ctrl.ActiveTurn)
        elif (LRange < 0):
            ctrl.ActiveTurn = LEFT
            Body.set_turn_velocity(abs(LRange / 2), PERCENT)
            Body.turn(ctrl.ActiveTurn)
        Body.drive(ctrl.ActiveRange)
    elif range > 0:
        Body.set_drive_velocity(range, PERCENT)
        ctrl.ActiveRange = REVERSE
        if (LRange > 0):
            ctrl.ActiveTurn = RIGHT
            Body.set_turn_velocity(abs(LRange / 1.33), PERCENT)
            Body.turn(ctrl.ActiveTurn)
        elif (LRange < 0):
            ctrl.ActiveTurn = LEFT
            Body.set_turn_velocity(abs(LRange / 1.33), PERCENT)
            Body.turn(ctrl.ActiveTurn)
        Body.drive(ctrl.ActiveRange)
    else:
        Body.set_drive_velocity(0)

def leftHoriMove():
    range = ctrl.LeftHori.position()
    brain.screen.print("\n",range)
    print("Horizon Axis: ", range)
    if range > 0:
        ctrl.ActiveTurn = RIGHT
        Body.set_turn_velocity(abs(range / 1.33), PERCENT)
        Body.turn(ctrl.ActiveTurn)
    elif range < 0:
        ctrl.ActiveTurn = LEFT
        Body.set_turn_velocity(abs(range / 1.33), PERCENT)
        Body.turn(ctrl.ActiveTurn)
    else:
        Body.set_turn_velocity(0)

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
        RightArm.spin(ctrl.ActiveRArms)
        LeftArm.spin(ctrl.ActiveLArms)
    # Bring the Arm Down
    elif range == "B":
        RightArm.set_velocity(100, PERCENT)
        LeftArm.set_velocity(100, PERCENT)
        ctrl.ActiveRArms = REVERSE
        ctrl.ActiveLArms = FORWARD
        RightArm.spin(ctrl.ActiveRArms)
        LeftArm.spin(ctrl.ActiveLArms)
    else:
        RightArm.set_velocity(0)
        LeftArm.set_velocity(0)
        RightArm.stop()
        LeftArm.stop()

# TODO: Check chain spinning     
def chainMove(input):
    if (input == "R1"):
        print("Right Shoulder button pressed")
        Chain.set_velocity(100, PERCENT)
        Chain.spin(REVERSE)
    elif (input == "R2"):
        print("Right trigger pressed")
        Chain.set_velocity(100, PERCENT)
        Chain.spin(FORWARD)
    else:
        print("Buttons released")
        Chain.stop()
    # Arms.spin(FORWARD)

def elevatorMove(input):
    if (input == "L1"):
        print("Left Shoulder button pressed")
        Elevator.set_velocity(100, PERCENT)
        Elevator.spin(FORWARD)
    elif (input == "L2"):
        print("Left trigger pressed")
        Elevator.set_velocity(100, PERCENT)
        Elevator.spin(REVERSE)
    else:
        print("Buttons released")
        Elevator.stop()
    # Arms.spin(FORWARD)

## HANDLERS

# ? We don't want to reset the arm position (as per moses's request)
RightArm.reset_position()
LeftArm.reset_position()
Body.set_turn_velocity(0)
Body.set_drive_velocity(0)
ctrl.RightVert.changed(leftVertMove)
ctrl.LeftHori.changed(leftHoriMove)
ctrl.XBtn.pressed(armMove, ("X",))
ctrl.BBtn.pressed(armMove, ("B",))
ctrl.RSb.pressed(chainMove, ("R1",))
ctrl.RTr.pressed(chainMove, ("R2",))
ctrl.LSb.pressed(elevatorMove, ("L1",))
ctrl.LTr.pressed(elevatorMove, ("L2",))
ctrl.BBtn.released(armMove, ("None",))
ctrl.XBtn.released(armMove, ("None",))
ctrl.RTr.released(chainMove, ("None",))
ctrl.RSb.released(chainMove, ("None",))
ctrl.LTr.released(elevatorMove, ("None",))
ctrl.LSb.released(elevatorMove, ("None",))
# ctrl.RightVert.changed(rightVertPower)
# test()
