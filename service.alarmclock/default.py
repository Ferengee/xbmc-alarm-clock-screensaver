import xbmc, xbmcaddon
import time, datetime
import glob

addon = xbmcaddon.Addon('screensaver.alarmclock')
active = False
 
while (not xbmc.abortRequested):
  time.sleep(1)

  
  alarmtime = "%s:%s" % (addon.getSetting('alarm_hour'), addon.getSetting('alarm_minute'))
  xbmc.log("alarm clock service tick, alarm at: %s" % alarmtime);
  now = datetime.datetime.today()
  if now.strftime("%H:%M") == alarmtime:
    if not active:
      xbmc.log(" ---- activating alarm !!!")
      music_folder = addon.getSetting('alarm_music')
      xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params":{"playlistid":1}, "id": 1}')
      
      for item in glob.glob("%s/*" % music_folder):
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Add", "params":{"playlistid":1, "item" :{ "file" : "%s"}}, "id" : 1}' % item)

      xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.Open", "params":{"item":{"playlistid":1, "position" : 0}}, "id": 1}')
      active = True
  else:
    active = False