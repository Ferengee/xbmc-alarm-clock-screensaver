#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random
import datetime, time
import os

import xbmcaddon, xbmcgui, xbmc

import controller

CENTERX=2
CENTERY=4

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')
image_dir = xbmc.translatePath( os.path.join( addon_path, 'resources', 'skins', 'default', 'media' ,'').encode("utf-8") ).decode("utf-8")


class PlayerMonitor(xbmc.Player) :
    
    def __init__ (self):
        xbmc.Player.__init__(self)

    def onPlayBackStarted(self):
        self.screen.updateSongInfo()

    def onPlayBackEnded(self):
        self.screen.updateSongInfo()
      
        
    def onPlayBackStopped(self):
        self.screen.updateSongInfo()
        
    def setScreen(self, screen):
      self.screen = screen

class Screensaver(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            self.exit_callback()
            
        def onAbortRequested(self):
            self.exit_callback()
            
 
    def onInit(self):       
        self.addon = xbmcaddon.Addon('screensaver.alarmclock')
        
        def convertColor(dec):
          return str(hex(int(dec)))[2:].upper()
        
        color = "".join(map(convertColor, [ self.addon.getSetting('setting_alpha_color'),
        self.addon.getSetting('setting_red_color'),
        self.addon.getSetting('setting_green_color'),
        self.addon.getSetting('setting_blue_color')]))
        color = "ff00baff"
        shadow = "DDBBBBBB"
        
        def constructImage(offsetX):
          return xbmcgui.ControlImage(x=offsetX, y=100, width=200, height=277, filename=(image_dir + "colon.png"))
          
        self.images = map(constructImage, [160, 360, 560, 760, 960])
        
        self.background = xbmcgui.ControlImage(x=0, y=0, width=1280, height=720, filename=(image_dir + "black.png"))
        
        for image in self.images:
          self.addControl(image)
            

        self.dateLabel = xbmcgui.ControlLabel(x=160, y=400, width=860, height=20, label="", font="font35_title", textColor=color, disabledColor=shadow, alignment=CENTERX | CENTERY); 
        self.addControl(self.dateLabel)
        self.songLabel = xbmcgui.ControlLabel(x=160, y=460, width=860, height=20, label="", font="font35_title", textColor=color, disabledColor=shadow, alignment=CENTERX | CENTERY); 
        self.addControl(self.songLabel)
        
        self.exitMonitor = self.ExitMonitor(self.exit)
        self.controller = controller.Controller(self.update)
        self.controller.start()
        self.updateSongInfo()
        
        
    def update(self):
      day = datetime.datetime.today()
      #self.timeLabel.setLabel(day.strftime("%H:%M:%S"))
      def drawImage(image, timepart):
        if timepart == ":":
          timepart = "colon"
        image.setImage((image_dir) + timepart + ".png")
        
      map(drawImage, self.images, day.strftime("%H:%M"))
      self.dateLabel.setLabel(day.strftime("%A %d. %B %Y"))      

    def exit(self):
        self.controller.stop()
        del self.exitMonitor
        del self.controller
        for image in self.images:
          self.removeControl(image)
        self.removeControl(self.dateLabel)
        self.removeControl(self.songLabel)
        self.close()
        
      
    def updateSongInfo(self):
      self.songLabel.setLabel("")
      if xbmc.Player.isPlaying:
        response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "album", "artist", "duration", "thumbnail", "file", "fanart", "streamdetails"], "playerid": 0 }, "id": "AudioGetItem"}')
        dec = json.loads(response)
        if dec.get("error") == None:
          self.songLabel.setLabel(dec["result"]["item"]["label"])
          
      
    
                

