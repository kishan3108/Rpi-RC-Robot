#!usr/bin/env python3

import time
import pygame
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

Drive_Wheel = 26
Drive_Servo = 12

GPIO.setup(Drive_Wheel, GPIO.OUT)
GPIO.setup(Drive_Servo, GPIO.OUT)

Drive_Wheel = GPIO.PWM(Drive_Wheel, 50)
Drive_Servo = GPIO.PWM(Drive_Servo, 50)

Drive_Wheel.start(0)
Drive_Servo.start(0)

#Sleep for initial boot up
time.sleep(5)
print("Operation Begins!")
# Joystick Control Parameters
axisLeftRight = 3
axisUpDown = 1
axisUpDownInverted = True #The up Down axis is reversed
axisLeftRightInverted = False
leftRight = 0
upDown = 0
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


# Turn off All motors in unexpected and key board interruption.
def MotorOff():
  Drive_Wheel.ChangeDutyCycle(0)
  Drive_Servo.ChangeDutyCycle(0)

MotorOff()
# Scale the signal from -1 to 1 to Control signal
def Scale(upDown, leftRight):
  if upDown >9: upDown = 9
  if upDown < -9: upDown = -9
  if leftRight >9: leftRight = 9
  if leftRight < -9: leftRight = -9
# From 1 to 9
#  leftRight = int((((leftRight + 9)*8)/18)+1)
# Fromt 9 to 1
  upDown = int((((upDown + 9)* (4))/18)+ 5)
  leftRight = int((((leftRight + 9)*(-6))/18)+10)
  return(upDown, leftRight)

#Control the signal by changing PWM duty cycle.
def control_op(upDown, leftRight):
  Drive_Wheel.ChangeDutyCycle(upDown)
  Drive_Servo.ChangeDutyCycle(leftRight)


# Main Program which will read the signal, scale it and send control_op signals.
def PygameHandler(events):
    global leftRight
    global upDown
    for event in events:
      if event.type == pygame.JOYAXISMOTION:
        upDown = int(joystick.get_axis(axisUpDown)*10)
        leftRight = int(joystick.get_axis(axisLeftRight)*10)
        if axisUpDownInverted:
          upDown = -upDown
        if axisLeftRightInverted:
          leftRight = -leftRight
        upDown, leftRight = Scale(upDown, leftRight)
        control_op(upDown, leftRight)
      else:
        control_op(7,7)
      print(upDown, leftRight)


#Main Loop which will exit if KeyboardInterrupt and cleanup the GPIO signal.
try:
  while 1:
    PygameHandler(pygame.event.get())
except KeyboardInterrupt:
  MotorOff()
  GPIO.cleanup()
  print("Exiting")

