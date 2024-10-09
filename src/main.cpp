/*----------------------------------------------------------------------------*/
/*                                                                            */
/*    Module:       main.cpp                                                  */
/*    Author:       VEX                                                       */
/*    Created:      Thu Sep 26 2019                                           */
/*    Description:  Competition Template                                      */
/*                                                                            */
/*----------------------------------------------------------------------------*/

// ---- START VEXCODE CONFIGURED DEVICES ----
// Robot Configuration:
// [Name]               [Type]        [Port(s)]
// Controller1          controller                    
// Drivetrain           drivetrain    2, 1, 9, 10     
// spinners             motor_group   11, 20          
// Arm                  motor_group   7, 17           
// DigitalOutA          digital_out   A               
// DigitalOutD          digital_out   D               
// ---- END VEXCODE CONFIGURED DEVICES ----

#include "vex.h"

using namespace vex;

// A global instance of competition
competition Competition;

// define your global instances of motors and other devices here

void SpinF() {
  spinners.spin(forward);
}

void SpinStop() {
  spinners.stop();
}

void OpenArm() {
  DigitalOutA.set(true);
  DigitalOutD.set(true);
}
void CloseArm() {
  DigitalOutA.set(false);
  DigitalOutD.set(false);
}

void ArmLift() {
  Arm.spin(forward);
}

void ArmFall() {
  Arm.spin(reverse);
}

void ArmStop() {
  Arm.stop();
}

/*---------------------------------------------------------------------------*/
/*                          Pre-Autonomous Functions                         */
/*                                                                           */
/*  You may want to perform some actions before the competition starts.      */
/*  Do them in the following function.  You must return from this function   */
/*  or the autonomous and usercontrol tasks will not be started.  This       */
/*  function is only called once after the V5 has been powered on and        */
/*  not every time that the robot is disabled.                               */
/*---------------------------------------------------------------------------*/

void pre_auton(void) {
  // Initializing Robot Configuration. DO NOT REMOVE!
  vexcodeInit();

  Drivetrain.setDriveVelocity(600, rpm);
  spinners.setStopping(brake);
  spinners.setVelocity(600, rpm);
  Arm.setVelocity(200, rpm);

  // All activities that occur before the competition starts
  // Example: clearing encoders, setting servo positions, ...
}

/*---------------------------------------------------------------------------*/
/*                                                                           */
/*                              Autonomous Task                              */
/*                                                                           */
/*  This task is used to control your robot during the autonomous phase of   */
/*  a VEX Competition.                                                       */
/*                                                                           */
/*  You must modify the code to add your own robot specific commands here.   */
/*---------------------------------------------------------------------------*/

void autonomous(void) {

  Drivetrain.drive(forward);
  wait(10, seconds);
  Drivetrain.driveFor(reverse, 1, inches);
  // ..........................................................................
  // Insert autonomous user code here.
  // ..........................................................................
}


/*---------------------------------------------------------------------------*/
/*                                                                           */
/*                              User Control Task                            */
/*                                                                           */
/*  This task is used to control your robot during the user control phase of */
/*  a VEX Competition.                                                       */
/*                                                                           */
/*  You must modify the code to add your own robot specific commands here.   */
/*---------------------------------------------------------------------------*/

void usercontrol(void) {
  // User control code here, inside the loop
  while (1) {
    // This is the main execution loop for the user control program.
    // Each time through the loop your program should update motor + servo
    // values based on feedback from the joysticks.

    // ........................................................................
    // Insert user code here. This is where you use the joystick values to
    // update your motors, etc.
    // ........................................................................

    Controller1.ButtonR2.pressed(SpinF);
    Controller1.ButtonR2.released(SpinStop);

    Controller1.ButtonX.pressed(OpenArm);
    Controller1.ButtonY.pressed(CloseArm);

    Controller1.ButtonB.pressed(ArmLift);
    Controller1.ButtonA.pressed(ArmFall);
    Controller1.ButtonA.released(ArmStop);
    Controller1.ButtonB.released(ArmStop);    

    wait(20, msec); // Sleep the task for a short amount of time to
                    // prevent wasted resources.
  }
}

//
// Main will set up the competition functions and callbacks.
//
int main() {
  // Set up callbacks for autonomous and driver control periods.
  Competition.autonomous(autonomous);
  Competition.drivercontrol(usercontrol);

  // Run the pre-autonomous function.
  pre_auton();

  // Prevent main from exiting with an infinite loop.
  while (true) {
    wait(100, msec);
  }
}
