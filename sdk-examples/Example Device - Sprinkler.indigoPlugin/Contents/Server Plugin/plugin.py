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
        # self.logger.debug("startup called")
        pass

    def shutdown(self):
        # self.logger.debug("shutdown called")
        pass

    ########################################
    def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
        return (True, values_dict)

    ########################################
    # Sprinkler Control Action callback
    ######################
    def actionControlSprinkler(self, action, dev):
        ########################################
        # Required plugin sprinkler actions: These actions must be handled by the plugin.
        ########################################
        ###### ZONE ON ######
        if action.sprinklerAction == indigo.kSprinklerAction.ZoneOn:
            # Command hardware module (dev) to turn ON a specific zone here.
            # ** IMPLEMENT ME **
            zone_name = "no zone"
            if action.zoneIndex is not None:
                zone_name = dev.zoneNames[action.zoneIndex - 1]
            send_success = True     # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name} - {zone_name}\" on")

                # And then tell the Indigo Server to update the state.
                dev.updateStateOnServer("activeZone", action.zoneIndex)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name} - {zone_name}\" on failed")

        ###### ALL ZONES OFF ######
        elif action.sprinklerAction == indigo.kSprinklerAction.AllZonesOff:
            # Command hardware module (dev) to turn OFF here:
            # ** IMPLEMENT ME **
            send_success = True     # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" all zones off")

                # And then tell the Indigo Server to update the state.
                dev.updateStateOnServer("activeZone", 0)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" all zones off failed")

        ########################################
        # Optional plugin sprinkler actions: These actions are *only* dispatched to the plugin
        # if the device property "OverrideScheduleActions" is set to True. The default behavior
        # (False) is for the Indigo Server to handle these higher level commands and scheduling
        # automatically, which will dispatch the required lower-level indigo.kSprinklerAction.ZoneOn
        # and indigo.kSprinklerAction.AllZonesOff actions above at the appropriate times.
        #
        # Note if a plugin defines the higher level actions below then it must handle all zone
        # scheduling, pausing, resuming, and next/previous skipping. Given the complexity in
        # handling the individual zone scheduling, pausing, resuming, and next/previous zones
        # it is recommended to use the default value of OverrideScheduleActions False, so that
        # IndigoServer can handle this higher level scheduling and complexity.
        ########################################
        ###### RUN SCHEDULE OF ZONE DURATIONS ######
        elif action.sprinklerAction == indigo.kSprinklerAction.RunNewSchedule:
            # Plugin should handle its own scheduling here and tell the device
            # to turn on the first zone in the schedule, _or_ (if supported by
            # the device) send the entire schedule to the device.
            # ** IMPLEMENT ME **
            self.logger.info(f"scheduled \"{dev.name}\" zone durations: {action.zoneDurations}")

            # The ScheduledZoneDurations property is used by Indigo to show the
            # currently running schedule (in the client, Web, and Indigo Touch UI),
            # so set based on the durations requested in the action.
            props = dev.pluginProps
            # Plugin should use dev.zoneEnableList, dev.zoneMaxDurations and
            # dev.zoneCount to make sure action.zoneDurations are within the
            # range and bounds specified.
            zone_list_str = ', '.join(str(dur) for dur in action.zoneDurations)
            props["PreviousZoneDurations"] = zone_list_str
            props["ScheduledZoneDurations"] = zone_list_str
            dev.replacePluginPropsOnServer(props)

            # Plugin will then need to update the activeZone state appropriately.
            # As an example here we'll just turn on zone 1 (plugin should really
            # inspect action.zoneDurations for the first non-zero item).
            dev.updateStateOnServer("activeZone", 1)

        ###### RUN LAST USED SCHEDULE ######
        elif action.sprinklerAction == indigo.kSprinklerAction.RunPreviousSchedule:
            # Plugin should re-run the last schedule that was used here and tell
            # the device to turn on the first zone in the schedule, _or_ (if
            # supported by the device) send the device a run last schedule command.
            # ** IMPLEMENT ME **

            # Plugin will then need to update the ScheduledZoneDurations property
            # and the activeZone state appropriately.
            props = dev.pluginProps
            if "PreviousZoneDurations" in props:
                self.logger.info(f"running last used scheduled for \"{dev.name}\": {props['PreviousZoneDurations']}")

                props["ScheduledZoneDurations"] = props["PreviousZoneDurations"]
                dev.replacePluginPropsOnServer(props)
                dev.updateStateOnServer("activeZone", 1)

        ###### PAUSE SCHEDULE ######
        elif action.sprinklerAction == indigo.kSprinklerAction.PauseSchedule:
            # Plugin should pause its schedule here and tell the device to
            # turn off the active zone, _or_ (if supported by the device)
            # send the device a pause command.
            # ** IMPLEMENT ME **
            self.logger.info(f"pausing \"{dev.name}\" schedule")

            # Plugin will then need to update the ScheduledZoneDurations property
            # and the activeZone state appropriately.
            props = dev.pluginProps
            props["PauseScheduleZoneIndex"] = dev.activeZone
            props["PauseScheduleRemainingZoneDuration"] = 15        # plugin needs to calc and store remaining duration for active zone
            props["ScheduledZoneDurations"] = ''                    # empty so UI doesn't show active schedule
            dev.replacePluginPropsOnServer(props)
            dev.updateStateOnServer("activeZone", 0)

        ###### RESUME SCHEDULE ######
        elif action.sprinklerAction == indigo.kSprinklerAction.ResumeSchedule:
            # Plugin should resume the active schedule here and tell the device
            # to turn on the paused zone, _or_ (if supported by the device) send
            # the device a resume command.
            # ** IMPLEMENT ME **

            # Plugin will then need to update the ScheduledZoneDurations property
            # and the activeZone state appropriately.
            props = dev.pluginProps
            if "PreviousZoneDurations" in props and "PauseScheduleZoneIndex" in props and "PauseScheduleRemainingZoneDuration" in props:
                self.logger.info(f"resuming \"{dev.name}\" schedule zone durations: {props['PreviousZoneDurations']}")

                resume_zone = int(props["PauseScheduleZoneIndex"])
                resume_duration = int(props["PauseScheduleRemainingZoneDuration"])

                props["PauseScheduleZoneIndex"] = 0
                props["PauseScheduleRemainingZoneDuration"] = 0
                props["ScheduledZoneDurations"] = props["PreviousZoneDurations"]
                dev.replacePluginPropsOnServer(props)
                dev.updateStateOnServer("activeZone", resume_zone)

                # Plugin should now use resume_duration for its own internal timer of how long
                # the activeZone (resume_zone) should remain ON before advancing to next zone.

        ###### STOP SCHEDULE ######
        elif action.sprinklerAction == indigo.kSprinklerAction.StopSchedule:
            # Plugin should stop the active schedule here and tell the device
            # to turn off all zones, _or_ (if supported by the device) send
            # the device both a stop schedule and all zones off command.
            # ** IMPLEMENT ME **
            self.logger.info(f"stopping \"{dev.name}\" schedule")

            # Clear out ScheduledZoneDurations so the UI doesn't show an active schedule anymore.
            props = dev.pluginProps
            props["PauseScheduleZoneIndex"] = 0
            props["PauseScheduleRemainingZoneDuration"] = 0
            props["ScheduledZoneDurations"] = ''
            dev.replacePluginPropsOnServer(props)

            # Plugin will then need to update the activeZone state appropriately.
            dev.updateStateOnServer("activeZone", 0)

        ###### JUMP TO PREVIOUS ZONE ######
        elif action.sprinklerAction == indigo.kSprinklerAction.PreviousZone:
            # Plugin should jump to the previous zone in the current
            # schedule here and tell the device to turn that zone on, _or_
            # (if supported by the device) send the device a previous zone
            # command.
            # ** IMPLEMENT ME **
            self.logger.info(f"skipping \"{dev.name}\" to previous zone")

            # Plugin will then need to update the activeZone state appropriately.
            #   dev.updateStateOnServer("activeZone", current zone - 1)

        ###### SKIP TO NEXT ZONE ######
        elif action.sprinklerAction == indigo.kSprinklerAction.NextZone:
            # Plugin should jump to the next zone in the current schedule
            # here and tell the device to turn that zone on, _or_ (if
            # supported by the device) send the device a next zone command.
            # ** IMPLEMENT ME **
            self.logger.info(f"advancing \"{dev.name}\" to next zone")

            # Plugin will then need to update the activeZone state appropriately.
            #   dev.updateStateOnServer("activeZone", current zone + 1)

    ########################################
    # General Action callback
    ######################
    def actionControlUniversal(self, action, dev):
        ###### BEEP ######
        if action.deviceAction == indigo.kUniversalAction.Beep:
            # Beep the hardware module (dev) here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" beep request")

        ###### ENERGY UPDATE ######
        elif action.deviceAction == indigo.kUniversalAction.EnergyUpdate:
            # Request hardware module (dev) for its most recent meter data here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" energy update request")

        ###### ENERGY RESET ######
        elif action.deviceAction == indigo.kUniversalAction.EnergyReset:
            # Request that the hardware module (dev) reset its accumulative energy usage data here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" energy reset request")

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
