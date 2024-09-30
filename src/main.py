# Library imports
from vex import *
import VexLib5 as base

# Brain should be defined by default
brain=Brain()

brain.screen.print("Hello V5")



# Ports.py defines the ports we use
# We want to dynamically change ports and active devices

# Lets Init our Motors
LeftTMtr = Motor(base.LeftTopPort, base.GreenGear, False)
LeftBMtr = Motor(base.LeftBtmPort, base.GreenGear, False)
RightTMtr = Motor(base.RightTopPort, base.GreenGear, True)
RightBMtr= Motor(base.RightBtmPort, base.GreenGear, True)

# These are the motor objects we use. They are MotorGroups which control serveral motors at oncce.
LeftMotor = MotorGroup(LeftTMtr,LeftBMtr)
RightMotor = MotorGroup(RightTMtr,RightBMtr)

# We refer to the group of all the Motors as the Body
Body = DriveTrain(LeftMotor,RightMotor)
Body.set_drive_velocity(50, PERCENT)
Body.drive_for(FORWARD, 12, INCHES)