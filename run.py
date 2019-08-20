#!/usr/bin/python3

import os, sys
import random

from pysimbotlib.Window import PySimbotApp
from pysimbotlib.Robot import Robot
from kivy.core.window import Window
from kivy.logger import Logger

# Number of robot that will be run
ROBOT_NUM = 1

# Delay between update (default: 1/60 (or 60 frame per sec))
TIME_INTERVAL = 1.0/60 #10frame per second 

# Max tick
MAX_TICK = 5000

# START POINT
START_POINT = (20, 560)

# Map file
MAP_FILE = 'maps/default_map.kv'

MOVE_STEP_SIZE = 5
TURN_STEP_SIZE = 15
COLLISION_DISTANCE_EPSILON = 10
RIGHT_SIDE_SENSOR_INDEX_LIST = [0,1,2,3]

def clamp(n, minValue, maxValue):
    return max(min(n, maxValue), minValue)

class MyRobot(Robot):
    def __init__(self):
        super(MyRobot, self).__init__()
        self.pos = START_POINT
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
    
    def moveToFood(self):
        ''' Move towards food
        '''

        #   Get avoid angle and ratio
        avoidAngle, avoidRatio = self.getAvoidAngleAndRatio()

        #   Get smell angle and clamp to turn step size
        smellAngle = self.smell()
        if abs(smellAngle) > TURN_STEP_SIZE:
            smellAngle = (smellAngle/abs(smellAngle))*TURN_STEP_SIZE

        #   Compute the turn angle with avoid ratio
        turnAngle = avoidRatio*avoidAngle + (1.0-avoidRatio)*smellAngle

        #   Compute the move distance
        moveDistance = (1.5-avoidRatio)*MOVE_STEP_SIZE

        self.turn(turnAngle)
        self.move(moveDistance)

    def getAvoidAngleAndRatio(self):
        ''' Compute void angle and ratio
        '''

        #   Get distance from all sensors
        allDistanceList = self.distance()

        #   Get index of sensor which has minimum distance
        minIndex, minDistance = 0, allDistanceList[0]
        for index, distance in enumerate(allDistanceList):
            if distance < minDistance:
                minDistance = distance
                minIndex = index

        #   Compute avoid angle
        avoidAngle = TURN_STEP_SIZE
        if minIndex in RIGHT_SIDE_SENSOR_INDEX_LIST:
            avoidAngle = -avoidAngle
        
        #   Compute collision weight list
        collisionWeightList = list(map( lambda x: clamp((x/COLLISION_DISTANCE_EPSILON)-1.0,0.0,1.0), allDistanceList ))

        #   Compute avoid ratio by multiplying all collision weight
        avoidRatio = 1.0
        for collisionWeight in collisionWeightList:
            avoidRatio *= collisionWeight

        #   Invert the value
        avoidRatio = 1.0 - avoidRatio

        return avoidAngle, avoidRatio

    def update(self):
        ''' Update method which will be called each frame
        '''
        self.moveToFood()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.move(5)
        elif keycode[1] == 'a':
            self.turn(-5)
        elif keycode[1] == 'd':
            self.turn(5)
        elif keycode[1] == 's':
            self.move(-5)

if __name__ == '__main__':
    app = PySimbotApp(MyRobot, ROBOT_NUM, mapPath=MAP_FILE, interval=TIME_INTERVAL, maxtick=MAX_TICK)
    app.run()



