"""
plugin.video.surveillanceroom

A Kodi add-on by Maikito26

Supporting functions that have no dependencies from the main add-on
"""
from future import standard_library
standard_library.install_aliases()
from builtins import str
import xbmc, xbmcaddon, xbmcvfs, xbmcgui
import os, urllib.request, urllib.parse, urllib.error, requests, sys
import sqlite3 as lite
import socket


__addon__ = xbmcaddon.Addon() 
__addonid__ = __addon__.getAddonInfo('id')
__version__ = __addon__.getAddonInfo('version')
__icon__  = __addon__.getAddonInfo('icon')
__path__ = xbmcvfs.translatePath(('special://home/addons/{0}').format(__addonid__))  
__data_path__ = xbmcvfs.translatePath('special://profile/addon_data/%s' %__addonid__ )
__log_level__ = int(__addon__.getSetting('log_level'))
__log_info__ = __addonid__ + ' v' + __version__ + ': '
TIMEOUT = int(__addon__.getSetting('request_timeout'))
socket.setdefaulttimeout(TIMEOUT)

_atleast_python27 = False
if '2.7.' in sys.version:
    _atleast_python27 = True

# Makes sure folder path exists
if not xbmcvfs.exists(__data_path__):
    try:
        xbmcvfs.mkdir(__data_path__)
    except:
        pass

def log_level():
    global __addon__
    global __log_level__
    __addon__ = xbmcaddon.Addon()
    __log_level__ = int(__addon__.getSetting('log_level'))
    
    if __log_level__ == 0:
        return 'Off'
    elif __log_level__ == 1:
        return 'Normal'
    elif __log_level__ == 2:
        return 'Verbose'
    else:
        return 'Debug'
    
def translation(id): 
    return __addon__.getLocalizedString(id)

def dialog_ok(msg):
    addon_name = translation(32000)
    xbmcgui.Dialog().ok(addon_name, msg)

def notify(msg):        
    if 'true' in __addon__.getSetting('notifications'):
        addon_name = translation(32000)
        xbmcgui.Dialog().notification(addon_name, msg, icon = __icon__) 

def log(level=4, value=''):
    msg = str(value)
    if level == 3:                              #Error
        xbmc.log(__log_info__ + '### ERROR ### : ' + msg, xbmc.LOGERROR)

    elif __log_level__ > 0 and level == 1: #Normal
        xbmc.log(__log_info__ + msg, xbmc.LOGNOTICE)

    elif __log_level__ > 1 and level == 2:                  #Verbose
        xbmc.log(__log_info__ + msg, xbmc.LOGNOTICE)
        
    elif __log_level__ > 2 and level == 4:                            #DEBUG
        xbmc.log(__log_info__ + msg, xbmc.LOGNOTICE)
  
def cleanup_images():
    """ Final Cleanup of images when Kodi shuts down """
    
    for i in xbmcvfs.listdir(__data_path__)[1]:
        if (i != 'settings.xml') and (not 'fanart_camera' in i):
            xbmcvfs.delete(os.path.join(__data_path__, i))
            log(4, 'CLEANUP IMAGES :: %s' %i)

def remove_leftover_images(filename_prefix):
    """ Attempts to remove leftover images after player stops """
    xbmc.sleep(1000)
    for i in xbmcvfs.listdir(__data_path__)[1]:
        if filename_prefix in i:
            xbmcvfs.delete(os.path.join(__data_path__, i))
            log(4, 'CLEANUP IMAGES :: %s' %i)
            
            
def remove_cached_art(art):
    """ Removes cached art from textures database and cached folder """
    
    _db_path = xbmcvfs.translatePath('special://home/userdata/Database').decode('utf-8')
    _tbn_path = xbmcvfs.translatePath('special://home/userdata/Thumbnails').decode('utf-8')
    db = None
    
    try:         
        db = lite.connect(os.path.join(_db_path, 'Textures13.db'))
        db = db.cursor()

        #Get cached image name to remove                  
        db.execute("SELECT cachedurl FROM texture WHERE url = '%s';" %art)
        data = db.fetchone()
        
        try:
            
            log(4, 'Removing Cached Art :: SQL Output: %s' %data[0])
            file_to_delete = os.path.join(_tbn_path, data[0])
            log(4, 'Removing Cached Art :: File to be removed: %s' %file_to_delete)

            xbmcvfs.delete(file_to_delete)
            db.execute("DELETE FROM texture WHERE url = '%s';" %art)

        except:
            pass
        
    except lite.Error as e:
        log(3, "Error %s:" %e.args[0])
        #sys.exit(1)
        
    finally:
        if db:
            db.close()
            
    try:
        log(4, 'Removing Original Artwork if Exists :: File to be removed: %s' %art)
        xbmcvfs.delete(art)
        
    except:
        pass

def get_icon(name_or_number):
    """ Determines which icon to display """
    #Copied from api_camera_wrapper.py
    FOSCAM_HD = 0
    FOSCAM_SD = 1
    FOSCAM_HD_OVERRIDE = 2
    GENERIC_IPCAM = 3
        
    if name_or_number == 'default':
        icon = os.path.join(__path__, 'icon.png')
        
    elif name_or_number == 'settings':
        icon = os.path.join(__path__, 'resources', 'media', 'icon-settings.png')
        
    elif name_or_number == 'advanced':
        icon = os.path.join(__path__, 'resources', 'media', 'icon-advanced-menu.png')
        
    else:
        camera_type = int(__addon__.getSetting('type%s' %name_or_number))
        ptz = int(__addon__.getSetting('ptz%s' %name_or_number))
        
        if camera_type == FOSCAM_HD or camera_type == FOSCAM_HD_OVERRIDE:
            if ptz > 0:
                icon = os.path.join(__path__, 'resources', 'media', 'icon-foscam-hd-ptz.png')
            else:
                icon = os.path.join(__path__, 'resources', 'media', 'icon-foscam-hd.png')
            
        elif camera_type == FOSCAM_SD:
            if ptz > 0:
                icon = os.path.join(__path__, 'resources', 'media', 'icon-foscam-sd-ptz.png')
            else:
                icon = os.path.join(__path__, 'resources', 'media', 'icon-foscam-sd.png')
            
        else:
            icon = os.path.join(__path__, 'resources', 'media', 'icon-generic.png')

    return icon

def get_fanart(name_or_number, new_art_url = None, update = False):
    """ Determines which fanart to show """
    if str(name_or_number) == 'default':
        fanart = os.path.join(__path__, 'fanart.jpg')
        
    else:
        fanart = os.path.join(__data_path__,'fanart_camera' + str(name_or_number) + '.jpg')

        if __addon__.getSetting('fanart') == 0 or update == True:
            remove_cached_art(fanart)

        if not xbmcvfs.exists(fanart) and new_art_url != None:            
            try:
                log(4, 'Retrieving new Fanart for camera %s : %s' %(name_or_number, new_art_url))
                urllib.request.urlretrieve(new_art_url, fanart)
            except:
                log(4, 'Failed to Retrieve Snapshot from camera %s.' %name_or_number)
                fanart = os.path.join(__path__, 'fanart.jpg')

    return fanart

def get_mjpeg_frame(stream, filename):
    """ Extracts JPEG image from MJPEG """
   
    line = b''  # Initialize as bytes
    try:
        x = 0
        while not b'length' in line.lower():  # Compare bytes with bytes
            if b'500 - Internal Server Error' in line or x > 10:
                return False
            #log(4, 'GETMJPEGFRAME: %s' %line)
            line = stream.readline()  # This returns bytes
            x += 1
            
        # Decode only when needed for parsing
        line_str = line.decode('utf-8', errors='ignore')
        bytes_count = int(line_str.split(':')[-1])
        
        # Read remaining headers
        while len(line) > 3:
            line = stream.readline()
            
        frame = stream.read(bytes_count)
   
    except requests.RequestException as e:
        log(3, str(e))
        return False

    if frame:
        with open(filename, 'wb') as jpeg_file:
            jpeg_file.write(frame)

    return True





