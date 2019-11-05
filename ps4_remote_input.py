#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import os, sys
import time
import pygame
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set which GPIO pins the drive outputs are connected to
DRIVE_1 = 4
DRIVE_2 = 18
DRIVE_3 = 8
DRIVE_4 = 7

# Set all of the drive pins as output pins
GPIO.setup(DRIVE_1, GPIO.OUT)
GPIO.setup(DRIVE_2, GPIO.OUT)
GPIO.setup(DRIVE_3, GPIO.OUT)
GPIO.setup(DRIVE_4, GPIO.OUT)

# Function to set all drives off
def MotorOff():
    GPIO.output(DRIVE_1, GPIO.LOW)
    GPIO.output(DRIVE_2, GPIO.LOW)
    GPIO.output(DRIVE_3, GPIO.LOW)
    GPIO.output(DRIVE_4, GPIO.LOW)

# Settings for JoyBorg
leftDrive = DRIVE_1                     # Drive number for left motor
rightDrive = DRIVE_4                    # Drive number for right motor
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 3                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time


#os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
#screen = pygame.display.set_mode([300,300])
#pygame.display.set_caption("JoyBorg - Press [ESC] to quit")
#pygame.display.init()
# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = True
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = False
        elif event.type == pygame.JOYAXISMOTION:
            # A joystick has been moved, read axis positions (-1 to +1)
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
            # Invert any axes which are incorrect
            if axisUpDownInverted:
                upDown = -upDown
            if axisLeftRightInverted:
                leftRight = -leftRight
            # Determine Up / Down values
            if upDown < -0.1:
                moveUp = True
                moveDown = False
                print('forward',upDown)
            elif upDown > 0.1:
                moveUp = False
                moveDown = True
                print('backward',upDown)
            else:
                moveUp = False
                moveDown = False
            # Determine Left / Right values
            if leftRight < -0.1:
                moveLeft = True
                moveRight = False
                print('Left',leftRight)
            elif leftRight > 0.1:
                moveLeft = False
                moveRight = True
                print('right',leftRight)
            else:
                moveLeft = False
                moveRight = False
                print('No Move')

try:
#    print('Press [ESC] to quit')
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            if moveQuit:
                break
            elif moveLeft:
                leftState = GPIO.LOW
                rightState = GPIO.HIGH
            elif moveRight:
                leftState = GPIO.HIGH
                rightState = GPIO.LOW
            elif moveUp:
                leftState = GPIO.HIGH
                rightState = GPIO.HIGH
            else:
                leftState = GPIO.LOW
                rightState = GPIO.LOW
            GPIO.output(leftDrive, leftState)
            GPIO.output(rightDrive, rightState)
        # Wait for the interval period
        time.sleep(interval)
    # Disable all drives
    MotorOff()
except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    GPIO.cleanup()
    MotorOff()
