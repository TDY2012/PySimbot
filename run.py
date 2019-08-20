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
START_POINT = (400, 200)

# Map file
MAP_FILE = 'maps/default_map.kv'

STEP_SIZE = 5
COLLISION_AVOID_ANGLE = 50
COLLISION_DISTANCE_EPSILON = 25

class MyRobot(Robot):
    def __init__(self):
        super(MyRobot, self).__init__()
        self.pos = START_POINT
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
    
    def getTurnToFoodAngle(self):
        ''' Compute angle to turn to food
        '''

        #   Get minimum distance from all sensors
        minDistance = self.getMinDistance()

        #   Get smell angle
        smellAngle = self.smell()

        #   Compute angle ratio to determine if the robot should avoid the obstable
        #   or move toward the food
        angleRatio = max(min(minDistance/COLLISION_DISTANCE_EPSILON,1.0),0.0)

        #   Compute the angle with angle ratio
        turnAngle = (1-angleRatio)*COLLISION_AVOID_ANGLE + angleRatio*smellAngle

        return turnAngle

    def getMinDistance(self):
        ''' Get minimum distance from all sensors
        '''
        allDistanceList = self.distance()
        return min(allDistanceList)

    def update(self):
        ''' Update method which will be called each frame
        '''

        angle = self.getTurnToFoodAngle()
        self.turn(angle)
        self.move(STEP_SIZE)

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
        elif keycode[1] == 'r':
            self.randomStart()    

    def randomStart(self):
        # MAP SIZE 790, 490
        OFFSET = 10
        START_POINT = ( random.randint( OFFSET, 790-OFFSET ),
                        random.randint( OFFSET, 490-OFFSET ) )
        self.pos = START_POINT    

if __name__ == '__main__':
    app = PySimbotApp(MyRobot, ROBOT_NUM, mapPath=MAP_FILE, interval=TIME_INTERVAL, maxtick=MAX_TICK)
    app.run()



