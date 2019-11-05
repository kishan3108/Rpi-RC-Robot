#!usr/bin/env python3

import time
import pygame
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
time.sleep(7)
#GPIO Parameters
Drive_Left_R = 12
Drive_Left_F = 13
Drive_Right_R =19
Drive_Right_F = 26

GPIO.setup(Drive_Left_F, GPIO.OUT)
GPIO.setup(Drive_Left_R, GPIO.OUT)
GPIO.setup(Drive_Right_F, GPIO.OUT)
GPIO.setup(Drive_Right_R, GPIO.OUT)

Drive_Left_F = GPIO.PWM(Drive_Left_F, 100)
Drive_Left_R = GPIO.PWM(Drive_Left_R, 100)
Drive_Right_F = GPIO.PWM(Drive_Right_F, 100)
Drive_Right_R = GPIO.PWM(Drive_Right_R, 100)

Drive_Left_F.start(0)
Drive_Left_R.start(0)
Drive_Right_F.start(0)
Drive_Right_R.start(0)

def MotorOff():
  Drive_Left_F.ChangeDutyCycle(0)
  Drive_Left_R.ChangeDutyCycle(0)
  Drive_Right_F.ChangeDutyCycle(0)
  Drive_Right_R.ChangeDutyCycle(0)

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



#Control Parameters
new_u = 0

def scale(updown, leftright):
  if updown > 90: updown = 100
  if updown <-90: updown = -100
  if leftright > 90: leftright = 100
  if leftright < -90: leftright = -100
  return (int(updown), int(leftright))

def control_op(updown, leftright):
#  global new_u
  if updown > 10 and (-10<  leftright < 10) :
    Drive_Left_F.ChangeDutyCycle(updown)
    Drive_Right_F.ChangeDutyCycle(updown)
  elif updown <-10 and (-10<  leftright < 10):
    Drive_Left_R.ChangeDutyCycle(-updown)
    Drive_Right_R.ChangeDutyCycle(-updown)
  elif updown > 10 and leftright > 10 :
    Drive_Left_F.ChangeDutyCycle(min(updown+leftright,100))
    Drive_Right_F.ChangeDutyCycle(max(abs(updown-leftright),0))
  elif updown > 10 and leftright < -10 :
    Drive_Left_F.ChangeDutyCycle(max(updown+leftright,0))
    Drive_Right_F.ChangeDutyCycle(min(abs(updown-leftright),100))

  elif leftright > 10:
    Drive_Left_F.ChangeDutyCycle(leftright) #abs(50 - leftright))
    Drive_Right_F.ChangeDutyCycle(0)
  elif leftright < -10:
    Drive_Left_F.ChangeDutyCycle(0)
    Drive_Right_F.ChangeDutyCycle(-leftright) #abs(50+leftright))
  else:
    MotorOff()




def PygameHandler(events):
    global leftRight
    global upDown
    for event in events:
      if event.type == pygame.JOYAXISMOTION:
        upDown = joystick.get_axis(axisUpDown)*100
        leftRight = joystick.get_axis(axisLeftRight)*100
        if axisUpDownInverted:
          upDown = -upDown
        if axisLeftRightInverted:
          leftRight = -leftRight
        upDown,leftRight=scale(upDown,leftRight)
        control_op(upDown,leftRight)
        print(upDown, leftRight)


try:
  while 1:
    (PygameHandler(pygame.event.get()))
#    scale(upDown,leftRight)
#    print(control_op(upDown,leftRight))
#    print(upDown, '##', leftRight)
except KeyboardInterrupt:
  print('Exiting')
  MotorOff()
  GPIO.cleanup()
except:
  print('Crashed Exit')
  MotorOff()
  GPIO.cleanup()
