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

import signal
import os
import sys
import gettext
from backend import *

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#
# I18N
#
gettext.textdomain(PROGNAME)
_ = gettext.gettext

class SwitchDesktop:
    def __init__(self):
        self.cw = CW
        self.wmlist = WMLIST
        self.defaultw = getDefaultWm()
        self.wm = WINDOWMANAGERS[self.defaultw][OPTION_NAME]

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(PROGNAME)
        self.builder.add_from_file(GLADEFILE)

        self.handlers = {
            "infoDialog_closed" : (self.onDeleteDialog, INFODIALOG),
            "warnDialog_closed" : (self.onDeleteDialog, WARNDIALOG),
            "infoDialog_ok_clicked" : (self.onDeleteDialog, INFODIALOG),            
            "warnDialog_ok_clicked" : (self.onDeleteDialog, WARNDIALOG),         
            "onDeleteWindow" : self.onDeleteWindow,
            "on_gnomeRB_clicked" : (self.on_RB_clicked, GNOME),
            "on_kdeRB_clicked" : (self.on_RB_clicked, KDE),
            "on_xfceRB_clicked" : (self.on_RB_clicked, XFCE),
            "on_twmRB_clicked" : (self.on_RB_clicked, TWM),
            "on_windowmakerRB_clicked" : (self.on_RB_clicked, WINDOWMAKER),
            "on_enlightenmentRB_clicked" : (self.on_RB_clicked, ENLIGHTENMENT),
            "on_fvwmRB_clicked" : (self.on_RB_clicked, FVWM),
            "on_icewmRB_clicked" : (self.on_RB_clicked, ICEWM),
            "on_fluxboxRB_clicked" : (self.on_RB_clicked, FLUXBOX),
            "on_defaultRB_clicked" : (self.on_RB_clicked, SYSTEM),
            "on_CB_toggled" : self.on_CB_toggled,
            "on_cancelB_clicked" : self.on_cancelB_clicked,
            "on_okB_clicked" : self.on_okB_clicked,            
        }

        self.builder.connect_signals(self.handlers)
        self.window = self.builder.get_object("window")
        self.okB = self.builder.get_object("okB")
        self.localCB = self.builder.get_object("localCB")
        self.infoDialog = self.builder.get_object("infoDialog")
        self.infoDialog.set_transient_for(self.window)
        self.warnDialog = self.builder.get_object("warnDialog")
        self.warnDialog.set_transient_for(self.window)
        self.window.show()
        self.hydrate()
        self.okB.set_sensitive(False)
        Gtk.main()

    def hydrate(self):
        for w in self.wmlist:
           self.builder.get_object(WINDOWMANAGERS[w][WIDGET_NAME]).show()
           
        if self.cw in WINDOWMANAGERS.keys():
           self.builder.get_object(WINDOWMANAGERS[self.cw][WIDGET_NAME]).set_active(True)
           self.wm = WINDOWMANAGERS[self.cw][OPTION_NAME]
        else:
           self.builder.get_object(WINDOWMANAGERS[self.defaultw][WIDGET_NAME]).set_active(True)
           self.wm = WINDOWMANAGERS[self.defaultw][OPTION_NAME]
           
    def on_cancelB_clicked(self, button):
        Gtk.main_quit()

    def on_okB_clicked(self, button):
        self.window.hide()

        if self.localCB.get_active():
            self.wm = self.wm + ' local'

        if os.system(HELPER + ' ' + self.wm):
            self.warnDialog.run()
            self.warnDialog.destroy()
        else:
            self.infoDialog.run()
            self.infoDialog.destroy()

        Gtk.main_quit()

    def on_RB_clicked(self, button, w):
        self.wm = WINDOWMANAGERS[w][OPTION_NAME]
        self.okB.set_sensitive(True)

    def on_CB_toggled(self, *args):
        self.okB.set_sensitive(True)

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onDeleteDialog(self, button, w):
        if w == INFODIALOG:
            self.infoDialog.destroy()
        else:
            self.warnDialog.destroy()

# MAIN
signal.signal (signal.SIGINT, signal.SIG_DFL)
app = SwitchDesktop()
sys.exit(0)
