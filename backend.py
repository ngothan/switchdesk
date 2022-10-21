#!/usr/bin/python3 -Es
# -*- coding: utf-8 -*-
#
# Copyright (C) 2002-2018 Red Hat, Inc.
#
# Authors:
# Than Ngo <than@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os.path

PROGNAME = 'switchdesk'
COPYRIGHT = 'Copyright (C) 2002-2018 Red Hat, Inc.'
AUTHORS = ['Than Ngo <than@redhat.com>']
INFODIALOG = 1
WARNDIALOG = 2
GLADEFILE = '/usr/share/' + PROGNAME + "/" + PROGNAME +  '.glade'
HELPER = 'switchdesk-helper'
WM_NAME = 0
WIDGET_NAME = 1
OPTION_NAME = 2
ICON_NAME = 3
GNOME = 'Gnome desktop'
KDE = 'Plasma'
XFCE = 'Xfce desktop enviroment'
TWM = 'Tab Window Manager'
WINDOWMAKER = 'Window Maker'
ENLIGHTENMENT = 'Enlightenment window manager'
FVWM = 'F Virtual Window Manager'
ICEWM = 'IceWM'
FLUXBOX = 'FluxBox'
SYSTEM = 'System default'

WINDOWMANAGERS = { KDE           : [ 'startplasma-x11', 'kdeRB', 'kde' ],
                   GNOME         : [ 'gnome-session', 'gnomeRB', 'gnome' ],
                   XFCE          : [ 'startxfce4', 'xfceRB' , 'xfce' ],
                   ICEWM         : [ 'icewm', 'icewmRB', 'icewm' ],
                   FVWM          : [ 'fvwm2', 'fvwmRB', 'fvwm' ],
                   ENLIGHTENMENT : [ 'enlightenment', 'enlightenmentRB', 'enlightenment' ],
                   WINDOWMAKER   : [ 'wmaker', 'windowmakerRB', 'wmaker' ],
                   TWM           : [ 'twm', 'twmRB', 'twm' ],
                   FLUXBOX       : [ 'fluxbox', 'fluxboxRB', 'fluxbox' ],
                   SYSTEM        : [ '', 'defaultRB', 'system', '' ] 
                 }

def getValue( s ):
    if str.find( s, '=' ) < 0:
        return ''
    s = str.split( s, '=', 1 )[1]
    s = str.replace( s, '\"', '')

    return str.strip(s)

def getWmFromFile( fn, k ):
    wm = ''
    if not os.access( fn, os.R_OK ):
       return wm
    f = open( fn, 'r' )
    line = f.readline()
    while line:
        if str.find( line, k ) == 0:
           wm = getValue(line)
           break
        line = f.readline()
    f.close()

    return wm

def getSystemDefault():
    return getWmFromFile( '/etc/sysconfig/desktop', 'DESKTOP=' )

def updateList():
    w = getSystemDefault()
    if w in WINDOWMANAGERS.keys():
       WINDOWMANAGERS[SYSTEM][ICON_NAME] = WINDOWMANAGERS[w][ICON_NAME]

def checkWM( wm ):
    DESKTOP_PATH = [ '/usr/bin/', '/usr/X11R6/bin/', '/usr/local/bin/' ]

    for p in DESKTOP_PATH:
        if os.access( p + WINDOWMANAGERS[wm][WM_NAME], os.X_OK ):
            return True

    return False

def getWmList():
    wmlist = []
    for w in WINDOWMANAGERS.keys():
        if checkWM( w ):
           wmlist.append( w )
    return wmlist

def getCurrentWM():
    sub_xclients = os.environ['HOME'] + '/.Xclients-default'
    if os.access( sub_xclients, os.R_OK ):
        wm = getWmFromFile(sub_xclients, 'WM=')
    else:
        wm = getWmFromFile(os.environ['HOME'] + '/.Xclients-' + os.environ.get('HOSTNAME', '') + os.environ['DISPLAY'], 'WM=')
    if wm == '':
       return wm

    for w in WINDOWMANAGERS:
        if wm in WINDOWMANAGERS[w]:
           wm = w
           break

    return wm

WMLIST = getWmList()
CW = getCurrentWM()
updateList()

def getDefaultWm():
    w = WMLIST[0]
    if KDE in WMLIST:
       w = KDE

    return w

def switchWM( wm ):
    pass
