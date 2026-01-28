#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2024, Perceptive Automation, LLC. All rights reserved.
# https://www.indigodomo.com

import random

try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(
            self: indigo.PluginBase,
            plugin_id: str,
            plugin_display_name: str,
            plugin_version: str,
            plugin_prefs: indigo.Dict,
            **kwargs: dict
    ) -> None:
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug: bool = True

    ########################################
    def startup(self: indigo.PluginBase) -> None:
        self.logger.debug("startup called")

    def shutdown(self: indigo.PluginBase) -> None:
        self.logger.debug("shutdown called")

    ########################################
    # Poll all of the states from the energy meter and pass new values to
    # Indigo Server.
    def _refresh_states_from_hardware(
            self: indigo.PluginBase,
            dev: indigo.Device,
            log_refresh: bool
    ) -> None:
        """
        As an example here we update the current power (Watts) to a random value, and we increase the kWh by a smidge.

        Note the states are automatically created based on the SupportsEnergyMeter and SupportsPowerMeter device
        properties.

        The plugin instance property is updated by updating the states.

        :param dev: the device to update
        :param log_refresh: should log to the event or not
        :return: None
        """
        key_value_list = []
        if "curEnergyLevel" in dev.states:
            simulate_watts = random.randint(0, 500)
            simulate_watts_str = f"{simulate_watts} W"
            if log_refresh:
                self.logger.info(f'received "{dev.name}" power load to {simulate_watts_str}')
            key_value_list.append({'key': 'curEnergyLevel', 'value': simulate_watts, 'uiValue': simulate_watts_str})
        if "accumEnergyTotal" in dev.states:
            simulate_kwh = dev.states.get("accumEnergyTotal", 0) + 0.001
            simulate_kwh_str = f"{simulate_kwh:.3f} kWh"
            if log_refresh:
                self.logger.info(f'received "{dev.name}" energy total to {simulate_kwh_str}')
            key_value_list.append({'key': 'accumEnergyTotal', 'value': simulate_kwh, 'uiValue': simulate_kwh_str})
        dev.updateStatesOnServer(key_value_list)

    ########################################
    def runConcurrentThread(self: indigo.PluginBase):
        try:
            while True:
                for dev in indigo.devices.iter("self"):
                    if not dev.enabled or not dev.configured:
                        continue
                    # Plugins that need to poll out the status from the meter
                    # could do so here, then broadcast back the new values to the
                    # Indigo Server.
                    self._refresh_states_from_hardware(dev, False)
                self.sleep(2)
        except self.StopThread:
            pass  # Optionally catch the StopThread exception and do any needed cleanup.

    ########################################
    def validateDeviceConfigUi(
            self: indigo.PluginBase,
            values_dict: indigo.Dict,
            type_id: str,
            dev_id: int
    ) -> tuple:
        """
        Validates the config UI for a device.

        :param values_dict: values for the dialog
        :param type_id: device type id
        :param dev_id: id of the device
        :return: tuple of the form (True, values_dict) or (False, dict_of_errors, values_dict)
        """
        return (True, values_dict)

    ########################################
    def deviceStartComm(self: indigo.PluginBase, dev: indigo.Device) -> None:
        """
        Called when communication with the hardware should be established.
        Here would be a good place to poll out the current states from the
        meter. If periodic polling of the meter is needed (that is, it
        doesn't broadcast changes back to the plugin somehow), then consider
        adding that to runConcurrentThread() above.

        :param dev: the device instance which should be started
        :return: None
        """
        self._refresh_states_from_hardware(dev, True)

    def deviceStopComm(self: indigo.PluginBase, dev: indigo.Device) -> None:
        """
        Called when communication with the hardware should be shutdown.

        :param dev: device instance to stop
        :return: None
        """
        pass

    ########################################
    # General Action callback
    ######################
    def actionControlUniversal(self: indigo.PluginBase, action: object, dev: indigo.Device) -> None:
        """
        This is the callback for the universal actions. For our purposes, we will inspect action.deviceAction to
        figure out what action is being called.

        :param action: an action instance
        :param dev:
        :return:
        """
        ###### BEEP ######
        if action.deviceAction == indigo.kUniversalAction.Beep:
            # Beep the hardware module (dev) here:
            # FIXME: add implementation here
            self.logger.info(f"sent '{dev.name}' beep request")
        ###### ENERGY UPDATE ######
        elif action.deviceAction == indigo.kUniversalAction.EnergyUpdate:
            # Request hardware module (dev) for its most recent meter data here:
            # FIXME: add implementation here
            self._refresh_states_from_hardware(dev, True)
        ###### ENERGY RESET ######
        elif action.deviceAction == indigo.kUniversalAction.EnergyReset:
            # Request that the hardware module (dev) reset its accumulative energy usage data here:
            # FIXME: add implementation here
            self.logger.info(f"sent '{dev.name}' energy usage reset")
            # And then tell Indigo to reset it by just setting the value to 0.
            # This will automatically reset Indigo's time stamp for the accumulation.
            dev.updateStateOnServer("accumEnergyTotal", 0.0)
        ###### STATUS REQUEST ######
        elif action.deviceAction == indigo.kUniversalAction.RequestStatus:
            # Query hardware module (dev) for its current status here:
            # FIXME: add implementation here
            self._refresh_states_from_hardware(dev, True)

    ########################################
    # Custom Plugin Action callbacks (defined in Actions.xml)
    ######################
    def set_backlight_brightness(self: indigo.PluginBase, plugin_action, dev):
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
