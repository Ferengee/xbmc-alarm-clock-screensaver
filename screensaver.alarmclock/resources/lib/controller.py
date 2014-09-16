#!/usr/bin/python
# -*- coding: utf-8 -*-


import threading
import datetime, time

import xbmc

class Controller(threading.Thread):
  
    def __init__(self, update):
      super(Controller, self).__init__()
      self.update = update
      self.waitCondition = threading.Condition()
      self.running = True
      
    def run(self):
         self.waitCondition.acquire()
         while self.isRunning():
             self.update()
             time.sleep(1)
             
      
    def isRunning(self):
        return not xbmc.abortRequested and self.running
        
    def stop(self):
        self.running = False
        