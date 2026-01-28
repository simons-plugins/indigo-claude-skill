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
import random

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
        self.logger.debug("startup called")

    def shutdown(self):
        self.logger.debug("shutdown called")

    ########################################
    def runConcurrentThread(self):
        try:
            while True:
                for dev in indigo.devices.iter("self"):
                    if not dev.enabled or not dev.configured:
                        continue

                    # Plugins that need to poll out the status from the sensor
                    # could do so here, then broadcast back the new values to the
                    # Indigo Server via updateStateOnServer. For this example, we
                    # could toggle the onOffState every 2 seconds. If the sensor
                    # always broadcasts out changes (or is just 1-way), then this
                    # entire runConcurrentThread() method can be deleted.
                    if dev.deviceTypeId == "myTempSensor":
                        if dev.sensorValue is not None:
                            example_temp_float = random.randint(560, 880) / 10.0      # random between 56.0 and 88.0 degrees F
                            example_temp_str = f"{example_temp_float:.1f} °F"

                            key_val_list = []
                            key_val_list.append({'key':'sensorValue', 'value':example_temp_float, 'uiValue':example_temp_str})
                            # Override the state icon shown (in Indigo Touch and client Main Window)
                            # for this device to be a temperature sensor:
                            if dev.onState is not None:
                                key_val_list.append({'key':'onOffState', 'value':not dev.onState})
                                dev.updateStatesOnServer(key_val_list)
                                if dev.onState:
                                    dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensorOn)
                                else:
                                    dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)
                            else:
                                dev.updateStatesOnServer(key_val_list)
                                dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)
                        elif dev.onState is not None:
                            dev.updateStateOnServer("onOffState", not dev.onState)
                            dev.updateStateImageOnServer(indigo.kStateImageSel.Auto)
                        else:
                            dev.updateStateImageOnServer(indigo.kStateImageSel.Auto)
                self.sleep(2)
        except self.StopThread:
            pass    # Optionally catch the StopThread exception and do any needed cleanup.

    ########################################
    def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
        return (True, values_dict)

    ########################################
    def deviceStartComm(self, dev):
        # Called when communication with the hardware should be started.
        pass

    def deviceStopComm(self, dev):
        # Called when communication with the hardware should be shutdown.
        pass

    ########################################
    # Sensor Action callback
    ######################
    def actionControlSensor(self, action, dev):
        ###### TURN ON ######
        # Ignore turn on/off/toggle requests from clients since this is a read-only sensor.
        if action.sensorAction == indigo.kSensorAction.TurnOn:
            self.logger.info(f"ignored \"{dev.name}\" on request (sensor is read-only)")
            # But we could request a sensor state update if we wanted like this:
            # dev.updateStateOnServer("onOffState", True)

        ###### TURN OFF ######
        # Ignore turn on/off/toggle requests from clients since this is a read-only sensor.
        elif action.sensorAction == indigo.kSensorAction.TurnOff:
            self.logger.info(f"ignored \"{dev.name}\" off request (sensor is read-only)")
            # But we could request a sensor state update if we wanted like this:
            # dev.updateStateOnServer("onOffState", False)

        ###### TOGGLE ######
        # Ignore turn on/off/toggle requests from clients since this is a read-only sensor.
        elif action.sensorAction == indigo.kSensorAction.Toggle:
            self.logger.info(f"ignored \"{dev.name}\" toggle request (sensor is read-only)")
            # But we could request a sensor state update if we wanted like this:
            # dev.updateStateOnServer("onOffState", not dev.onState)

    ########################################
    # General Action callback
    ######################
    def actionControlUniversal(self, action, dev):
        ###### BEEP ######
        if action.deviceAction == indigo.kUniversalAction.Beep:
            # Beep the hardware module (dev) here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" beep request")

        ###### STATUS REQUEST ######
        elif action.deviceAction == indigo.kUniversalAction.RequestStatus:
            # Query hardware module (dev) for its current status here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" status request")

    ########################################
    # Custom Plugin Action callbacks (defined in Actions.xml)
    ######################
    def set_backlight_brightness(self, plugin_action, dev):
        try:
            new_brightness = int(plugin_action.props.get("brightness", 100))
        except ValueError:
            # The int() cast above might fail if the user didn't enter a number:
            self.logger.error(f"set backlight brightness action to device \"{dev.name}\" -- invalid brightness value")
            return
        # Command hardware module (dev) to set backlight brightness here:
        # FIXME: add implementation here
        send_success = True     # Set to False if it failed.
        if send_success:
            # If success then log that the command was successfully sent.
            self.logger.info(f"sent \"{dev.name}\" set backlight brightness to {new_brightness}")
            # And then tell the Indigo Server to update the state:
            dev.updateStateOnServer("backlightBrightness", new_brightness)
        else:
            # Else log failure but do NOT update state on Indigo Server.
            self.logger.error(f"send \"{dev.name}\" set backlight brightness to {new_brightness} failed")
