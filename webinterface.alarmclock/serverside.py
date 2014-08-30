import xbmc, xbmcaddon
import time, datetime
import urlparse

addon = xbmcaddon.Addon('screensaver.alarmclock')
active = False
 
##
# get argv when called from JsonRPC
# get different commands
# setAlarm
# getMusicPath for setting alarm folder
# parse an alarm time and update settings for the alarmclock
if __name__ == '__main__':
    
    params = urlparse.parse_qs('&'.join(sys.argv[1:]))
    xbmc.log(",".join(sys.argv[1:]))
    method = str(params.get("method")[0])
    if method == "setAlarm":
      addon.setSetting('alarm_hour', str(params.get("hour")[0]))
      addon.setSetting('alarm_minute', str(params.get("minute")[0]))
   
    if method == "getAlarm" or method == "setAlarm":
      alarmtime = "%s:%s" % (addon.getSetting('alarm_hour').zfill(2), addon.getSetting('alarm_minute').zfill(2))
      xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "JSONRPC.NotifyAll", "params": {"sender":"webinterface.alarmclock", "message":"Clock.UpdateAlarm", "data": "%s"}, "id":"updateAlarm"}' % alarmtime) 
    
    if method == "getClock":
      xbmc.log(" -- getClock")
      now = time.time()
      xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "JSONRPC.NotifyAll", "params": {"sender":"webinterface.alarmclock", "message":"Clock.UpdateClock", "data": "%s"}, "id":"updateClock"}' % str(now)) 

                     