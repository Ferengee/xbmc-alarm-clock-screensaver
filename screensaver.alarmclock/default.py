# import the XBMC libraries so we can use the controls and functions of XBMC
import xbmc, xbmcgui, xbmcaddon
import os
 
 
addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__cwd__ = __addon__.getAddonInfo('path').decode("utf-8")
__resource__ = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")

sys.path.append(__resource__)


if __name__ == '__main__':
    import gui
    screensaver_gui = gui.Screensaver(
        'alarmclock.xml',
        addon_path,
        'default',
    )
    
    player = gui.PlayerMonitor()
    player.setScreen(screensaver_gui)
    
    screensaver_gui.doModal()
    del screensaver_gui
    del player
    sys.modules.clear()
