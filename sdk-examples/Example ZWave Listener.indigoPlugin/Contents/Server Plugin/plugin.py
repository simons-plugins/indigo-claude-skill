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

########################################
# Tiny function to convert a list of integers (bytes in this case) to a
# hexadecimal string for pretty logging.
def convert_list_to_hex_str(byte_list):
    return ' '.join([f"{byte:02X}" for byte in byte_list])

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug: bool = True

    ########################################
    def startup(self):
        self.logger.debug("startup called -- subscribing to all incoming and outgoing Z-Wave commands")
        indigo.zwave.subscribeToIncoming()
        indigo.zwave.subscribeToOutgoing()

    def shutdown(self):
        self.logger.debug("shutdown called")

    ########################################
    def zwaveCommandReceived(self, cmd):
        byte_list = cmd['bytes']         # List of the raw bytes just received.
        byte_list_str = convert_list_to_hex_str(byte_list)
        node_id = cmd['nodeId']          # Can be None!
        endpoint = cmd['endpoint']      # Often will be None!

        if node_id and endpoint:
            self.logger.debug(f"received: {byte_list_str} (node {node_id:03d}, endpoint {endpoint})")
        elif node_id:
            self.logger.debug(f"received: {byte_list_str} (node {node_id:03d})")
        else:
            self.logger.debug(f"received: {byte_list_str}")

    def zwaveCommandSent(self, cmd):
        byte_list = cmd['bytes']         # List of the raw bytes just sent.
        byte_list_str = convert_list_to_hex_str(byte_list)
        time_delta = cmd['timeDelta']    # The time duration it took to receive an Z-Wave ACK for the command.
        cmd_success = cmd['cmdSuccess']  # True if an ACK was received (or no ACK expected), false if NAK.
        node_id = cmd['nodeId']          # Can be None!
        # endpoint = cmd['endpoint']      # Often will be None!

        if cmd_success:
            if node_id:
                self.logger.debug(f"sent: {byte_list_str} (node {node_id:03d} ACK after {time_delta} milliseconds)")
            else:
                self.logger.debug(f"sent: {byte_list_str} (ACK after {time_delta} milliseconds)")
        else:
            self.logger.debug(f"sent: {byte_list_str} (failed)")
