#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''

@File   : tb4w11.py   
@Author : alexander.here@gmail.com
@Date   : 2024-08-20 16:49    (+0800)   
@Brief  :  

'''

import os, sys, subprocess
import pystray, pymsgbox
from PIL import Image
from functools import partial

def on_open_folder_clicked( stray_icon, item):
    global working_folder
    if sys.platform == 'win32':
        os.startfile( working_folder)
    elif sys.platform == 'darwin':
        subprocess.call(('open', working_folder))
    elif sys.platform.startswith == 'linux':
        subprocess.call(('xdg-open', working_folder))

def on_refresh_clicked( stray_icon, item):
    global keep_running
    keep_running = True
    stray_icon.stop()

def on_exit_clicked( stray_icon, item):
    global keep_running
    keep_running = False
    stray_icon.stop()

def on_item_clicked( stray_icon, item, fullpath):
    print( f'"{fullpath}" clicked.')
    try:
        if sys.platform == 'win32':
            os.startfile( fullpath)
        elif sys.platform == 'darwin':
            subprocess.call(('open', fullpath))
        elif sys.platform.startswith == 'linux':
            subprocess.call(('xdg-open', fullpath))
    except Exception as e:
        pymsgbox.alert( f'Failed opening file "{working_folder}": {e}', 'ERROR')

logo_path = "logo.png"
if hasattr(sys, '_MEIPASS'): # running in PyInstaller package
    logo_path = os.path.join( sys._MEIPASS, logo_path)
logo = Image.open( logo_path)

working_folder = 'folder'
if len( sys.argv) > 1:
    working_folder = sys.argv[ 1]

keep_running = True
while keep_running:
    item_list = []
    def travel_menuitems( fullpath):
        if os.path.isfile( fullpath):
            name = os.path.basename( fullpath)
            return pystray.MenuItem( name, partial( on_item_clicked, fullpath=fullpath))
        elif os.path.isdir( fullpath):
            name = os.path.basename( fullpath)
            subitem_list = []
            for f in os.listdir( fullpath):
                subitem_list.append( travel_menuitems( os.path.join( fullpath, f)))
            return pystray.MenuItem( name, pystray.Menu( *subitem_list))
        return None
    try:
        for f in os.listdir( working_folder):
            item_list.append( travel_menuitems( os.path.join( working_folder, f)))
    except Exception as e:
        pymsgbox.alert( f'Failed scaning folder "{working_folder}": {e}', 'ERROR')
        exit( 1)

    item_list.append( pystray.Menu.SEPARATOR)
    item_list.append( pystray.MenuItem( 'Open Folder ...', on_open_folder_clicked))
    item_list.append( pystray.MenuItem( 'Refresh', on_refresh_clicked))
    item_list.append( pystray.Menu.SEPARATOR)
    item_list.append( pystray.MenuItem( 'Exit', on_exit_clicked))

    menu = pystray.Menu( *item_list)
    stray_icon = pystray.Icon( 'Toolbar4W11', icon=logo, menu=menu)
    stray_icon.run()

# End of 'tb4w11.py' 

