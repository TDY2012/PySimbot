#!/usr/bin/python3
import os, sys

from kivy.config import Config
Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
import platform
from kivy.properties import NumericProperty,\
                            ReferenceListProperty,\
                            ObjectProperty

from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.logger import Logger
from .scaler import Scaler

from . import Obstacle
from . import Objective

DEFAULT_INTERVAL = 1.0/60.0
MAP_DIRECTORY = '/maps'
DEFAULT_MAP_NAME = 'default_map.kv'

class PySimbotMap(Widget):
    playground = ObjectProperty(None)
    obstacles = ObjectProperty(None)
    objectives = ObjectProperty(None)
    iteration = NumericProperty(0)
    max_iter = NumericProperty(0)

    def __init__(self, mapPath, **kwargs):
        super(PySimbotMap, self).__init__(**kwargs)
        self.mapPath = mapPath
        self.robots = list()
    
    def before_update(self):
        # Update robots index 0 to UI
        if len(self.robots) > 0:
            distances = self.robots[0].distance()
            smell = self.robots[0].smell()

        Logger.info('Map: Iteration: {}'.format(self.iteration))
    
    def after_update(self):
        Logger.info('Map: End Iteration')

    def update(self, dt):
        if self.max_iter > 0 and self.iteration >= self.max_iter:
            return
        self.iteration += 1
        self.before_update()
        for robot in self.robots:
            #robot.before_update()
            robot.update()
        self.after_update()


class PySimbotApp(App):
    title = 'PySimbot (Created by Saran(Bird) Khotsathian CPE25)'

    def __init__(self, robotCls, numRobot=1, mapPath=os.path.join(MAP_DIRECTORY, DEFAULT_MAP_NAME), interval=DEFAULT_INTERVAL, maxtick=5000, **kwargs):
        super(PySimbotApp, self).__init__(**kwargs)
        Logger.info('Map Path: %s' % mapPath)
        self.numRobot = numRobot
        self.robotCls = robotCls
        self.mapPath = mapPath
        self.interval = interval
        self.maxtick = maxtick
        self.simbotMap = None
    
    def build(self):
        Window.size = (700, 600)
        obmap = Builder.load_file(self.mapPath)
        robot = Builder.load_file('pysimbotlib/widget/robot.kv')
        sbmap = Builder.load_file('pysimbotlib/widget/simbotmap.kv')

        self.simbotMap = PySimbotMap(self.mapPath)
        self.simbotMap.robots = []
        self.simbotMap.max_iter = self.maxtick

        obs = Obstacle.Obstacle()
        self.simbotMap.obstacles = obs
        obj = Objective.Objective()
        self.simbotMap.objectives = obj

        if(self.simbotMap.playground):
            self.simbotMap.playground.add_widget(obs)
            self.simbotMap.playground.add_widget(obj)
        else:
            self.simbotMap.add_widget(obs)
            self.simbotMap.add_widget(obj)

        for i in range(self.numRobot):
            r = self.robotCls()
            r._sm = self.simbotMap
            if(self.simbotMap.playground):
                self.simbotMap.playground.add_widget(r)
            else:
                self.simbotMap.add_widget(r)
            self.simbotMap.robots.append(r)

        Clock.schedule_interval(self.simbotMap.update, self.interval)

        if platform.system() == 'Darwin':
            self._scaler = Scaler(size=Window.size, scale=2)
            Window.add_widget(self._scaler)
            parent = self._scaler or Window
            parent.add_widget(self.simbotMap)
        else:
            return self.simbotMap
