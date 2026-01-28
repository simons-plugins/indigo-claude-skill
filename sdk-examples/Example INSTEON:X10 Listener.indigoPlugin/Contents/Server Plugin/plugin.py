#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2024, Perceptive Automation, LLC. All rights reserved.
# https://www.indigodomo.com

try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

import os
import sys

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug: bool = True

    ########################################
    def startup(self):
        self.logger.debug("startup called -- subscribing to all X10 and INSTEON commands")
        indigo.insteon.subscribeToIncoming()
        indigo.insteon.subscribeToOutgoing()
        indigo.x10.subscribeToIncoming()
        indigo.x10.subscribeToOutgoing()

    def shutdown(self):
        self.logger.debug("shutdown called")

    ########################################
    def insteonCommandReceived(self, cmd):
        self.logger.debug(f"insteonCommandReceived: \n{str(cmd)}")

    def insteonCommandSent(self, cmd):
        self.logger.debug(f"insteonCommandSent: \n{str(cmd)}")

    ########################################
    def x10CommandReceived(self, cmd):
        self.logger.debug(f"x10CommandReceived: \n{str(cmd)}")

        if cmd.cmdType == "sec":    # or "x10" for power line commands
            if cmd.secCodeId == 6:
                if cmd.secFunc == "sensor alert (max delay)":
                    self.logger.info("SENSOR OPEN")
                elif cmd.secFunc == "sensor normal (max delay)":
                    self.logger.info("SENSOR CLOSED")

    def x10CommandSent(self, cmd):
        self.logger.debug(f"x10CommandSent: \n{str(cmd)}")
