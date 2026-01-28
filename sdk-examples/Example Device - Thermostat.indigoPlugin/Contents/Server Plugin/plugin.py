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
HVAC_MODE_ENUM_TO_STR_MAP = {
    indigo.kHvacMode.Cool               : "cool",
    indigo.kHvacMode.Heat               : "heat",
    indigo.kHvacMode.HeatCool           : "auto",
    indigo.kHvacMode.Off                : "off",
    indigo.kHvacMode.ProgramHeat        : "program heat",
    indigo.kHvacMode.ProgramCool        : "program cool",
    indigo.kHvacMode.ProgramHeatCool    : "program auto"
}

FAN_MODE_ENUM_TO_STR_MAP = {
    indigo.kFanMode.AlwaysOn            : "always on",
    indigo.kFanMode.Auto                : "auto"
}

def _lookup_action_str_from_hvac_mode(hvac_mode):
    return HVAC_MODE_ENUM_TO_STR_MAP.get(hvac_mode, "unknown")

def _lookup_action_str_from_fan_mode(fan_mode):
    return FAN_MODE_ENUM_TO_STR_MAP.get(fan_mode, "unknown")

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug: bool = True
        self.simulate_temp_changes = True     # Every few seconds update to random temperature values
        self.simulate_humidity_changes = True # Every few seconds update to random humidity values
        self.refresh_delay = 2               # Simulate new temperature values every 2 seconds

    ########################################
    # Internal utility methods. Some of these are useful to provide
    # a higher-level abstraction for accessing/changing thermostat
    # properties or states.
    ######################
    def _change_temp_sensor_count(self, dev, count):
        new_props = dev.pluginProps
        new_props["NumTemperatureInputs"] = count
        dev.replacePluginPropsOnServer(new_props)

    def _change_humidity_sensor_count(self, dev, count):
        new_props = dev.pluginProps
        new_props["NumHumidityInputs"] = count
        dev.replacePluginPropsOnServer(new_props)

    def _change_all_temp_sensor_counts(self, count):
        for dev in indigo.devices.iter("self"):
            self._change_temp_sensor_count(dev, count)

    def _change_all_humidity_sensor_counts(self, count):
        for dev in indigo.devices.iter("self"):
            self._change_humidity_sensor_count(dev, count)

    ######################
    def _change_temp_sensor_value(self, dev, index, value, key_val_list):
        # Update the temperature value at index. If index is greater than the "NumTemperatureInputs"
        # an error will be displayed in the Event Log "temperature index out-of-range"
        state_key = "temperatureInput" + str(index)
        key_val_list.append({'key':state_key, 'value':value, 'uiValue':f"{value} °F"})
        self.logger.debug(f"\"{dev.name}\" updating {state_key} {value}")

    def _change_humidity_sensor_value(self, dev, index, value, key_val_list):
        # Update the humidity value at index. If index is greater than the "NumHumidityInputs"
        # an error will be displayed in the Event Log "humidity index out-of-range"
        state_key = "humidityInput" + str(index)
        key_val_list.append({'key':state_key, 'value':value, 'uiValue':f"{value}%"})
        self.logger.debug(f"\"{dev.name}\" updating {state_key} {value}")

    ######################
    # Poll all of the states from the thermostat and pass new values to
    # Indigo Server.
    def _refresh_states_from_hardware(self, dev, log_refresh, comm_just_started):
        # As an example here we update the temperature and humidity
        # sensor states to random values.
        key_val_list = []
        if self.simulate_temp_changes:
            # Simulate changing temperature values coming in from the
            # hardware by updating all temp values randomly:
            num_temps = dev.temperatureSensorCount
            for index in range(1, num_temps + 1):
                example_temp = random.randint(62, 88)
                self._change_temp_sensor_value(dev, index, example_temp, key_val_list)
                if log_refresh:
                    self.logger.info(f"received \"{dev.name}\" temperature{index} update to {example_temp:.1f}°")
                if dev.pluginProps.get("ShowCoolHeatEquipmentStateUI", False) and "hvacOperationMode" in dev.states and "setpointCool" in dev.states and "setpointHeat" in dev.states:
                    if dev.states["hvacOperationMode"] in [indigo.kHvacMode.Cool, indigo.kHvacMode.HeatCool, indigo.kHvacMode.ProgramCool, indigo.kHvacMode.ProgramHeatCool]:
                        key_val_list.append({'key':'hvacCoolerIsOn', 'value':example_temp > dev.states["setpointCool"]})
                    if dev.states["hvacOperationMode"] in [indigo.kHvacMode.Heat, indigo.kHvacMode.HeatCool, indigo.kHvacMode.ProgramHeat, indigo.kHvacMode.ProgramHeatCool]:
                        key_val_list.append({'key':'hvacHeaterIsOn', 'value':example_temp < dev.states["setpointHeat"]})
        if self.simulate_humidity_changes:
            # Simulate changing humidity values coming in from the
            # hardware by updating all humidity values randomly:
            num_sensors = dev.humiditySensorCount
            for index in range(1, num_sensors + 1):
                example_humidity = random.randint(15, 90)
                self._change_humidity_sensor_value(dev, index, example_humidity, key_val_list)
                if log_refresh:
                    self.logger.info(f"received \"{dev.name}\" humidity{index} update to {example_humidity:.0f}%")

        #   Other states that should also be updated:
        # ** IMPLEMENT ME **
        # key_val_list.append({'key':'setpointHeat', 'value':floating number here})
        # key_val_list.append({'key':'setpointCool', 'value':floating number here})
        # key_val_list.append({'key':'hvacOperationMode', 'value':some indigo.kHvacMode.* value here})
        # key_val_list.append({'key':'hvacFanMode', 'value':some indigo.kFanMode.* value here})
        # key_val_list.append({'key':'hvacCoolerIsOn', 'value':True or False here})
        # key_val_list.append({'key':'hvacHeaterIsOn', 'value':True or False here})
        # key_val_list.append({'key':'hvacFanIsOn', 'value':True or False here})
        if comm_just_started:
            # As an example, we force these thermostat states to specific values.
            if "setpointHeat" in dev.states:
                key_val_list.append({'key':'setpointHeat', 'value':66.5, 'uiValue':"66.5 °F"})
            if "setpointCool" in dev.states:
                key_val_list.append({'key':'setpointCool', 'value':77.5, 'uiValue':"77.5 °F"})
            if "hvacOperationMode" in dev.states:
                key_val_list.append({'key':'hvacOperationMode', 'value':indigo.kHvacMode.HeatCool})
            if "hvacFanMode" in dev.states:
                key_val_list.append({'key':'hvacFanMode', 'value':indigo.kFanMode.Auto})
            key_val_list.append({'key':'backlightBrightness', 'value':85, 'uiValue':"85%"})

        if len(key_val_list) > 0:
            dev.updateStatesOnServer(key_val_list)

        if log_refresh:
            if "setpointHeat" in dev.states:
                self.logger.info(f"received \"{dev.name}\" cool setpoint update to {dev.states['setpointHeat']:.1f}°")
            if "setpointCool" in dev.states:
                self.logger.info(f"received \"{dev.name}\" heat setpoint update to {dev.states['setpointCool']:.1f}°")
            if "hvacOperationMode" in dev.states:
                action_str = _lookup_action_str_from_hvac_mode(dev.states["hvacOperationMode"])
                self.logger.info(f"received \"{dev.name}\" main mode update to {action_str}")
            if "hvacFanMode" in dev.states:
                action_str = _lookup_action_str_from_fan_mode(dev.states["hvacFanMode"])
                self.logger.info(f"received \"{dev.name}\" fan mode update to {action_str}")
            self.logger.info(f"received \"{dev.name}\" backlight brightness update to {dev.states['backlightBrightness']}%")

    ######################
    # Process action request from Indigo Server to change main thermostat's main mode.
    def _handle_change_hvac_mode_action(self, dev, new_hvac_mode):
        # Command hardware module (dev) to change the thermostat mode here:
        # ** IMPLEMENT ME **
        send_success = True     # Set to False if it failed.

        action_str = _lookup_action_str_from_hvac_mode(new_hvac_mode)
        if send_success:
            # If success then log that the command was successfully sent.
            self.logger.info(f"sent \"{dev.name}\" mode change to {action_str}")

            # And then tell the Indigo Server to update the state.
            if "hvacOperationMode" in dev.states:
                dev.updateStateOnServer("hvacOperationMode", new_hvac_mode)
        else:
            # Else log failure but do NOT update state on Indigo Server.
            self.logger.error(f"send \"{dev.name}\" mode change to {action_str} failed")

    ######################
    # Process action request from Indigo Server to change thermostat's fan mode.
    def _handle_change_fan_mode_action(self, dev, new_fan_mode):
        # Command hardware module (dev) to change the fan mode here:
        # ** IMPLEMENT ME **
        send_success = True     # Set to False if it failed.

        action_str = _lookup_action_str_from_fan_mode(new_fan_mode)
        if send_success:
            # If success then log that the command was successfully sent.
            self.logger.info(f"sent \"{dev.name}\" fan mode change to {action_str}")

            # And then tell the Indigo Server to update the state.
            if "hvacFanMode" in dev.states:
                dev.updateStateOnServer("hvacFanMode", new_fan_mode)
        else:
            # Else log failure but do NOT update state on Indigo Server.
            self.logger.error(f"send \"{dev.name}\" fan mode change to {action_str} failed")

    ######################
    # Process action request from Indigo Server to change a cool/heat setpoint.
    def _handle_change_setpoint_action(self, dev, new_setpoint, log_action_name, state_key):
        if new_setpoint < 40.0:
            new_setpoint = 40.0      # Arbitrary -- set to whatever hardware minimum setpoint value is.
        elif new_setpoint > 95.0:
            new_setpoint = 95.0      # Arbitrary -- set to whatever hardware maximum setpoint value is.

        send_success = False

        if state_key == "setpointCool":
            # Command hardware module (dev) to change the cool setpoint to new_setpoint here:
            # ** IMPLEMENT ME **
            send_success = True         # Set to False if it failed.
        elif state_key == "setpointHeat":
            # Command hardware module (dev) to change the heat setpoint to new_setpoint here:
            # ** IMPLEMENT ME **
            send_success = True         # Set to False if it failed.

        if send_success:
            # If success then log that the command was successfully sent.
            self.logger.info(f"sent \"{dev.name}\" {log_action_name} to {new_setpoint:.1f}°")

            # And then tell the Indigo Server to update the state.
            if state_key in dev.states:
                dev.updateStateOnServer(state_key, new_setpoint, uiValue=f"{new_setpoint:.1f} °F")
        else:
            # Else log failure but do NOT update state on Indigo Server.
            self.logger.error(f"send \"{dev.name}\" {log_action_name} to {new_setpoint:.1f}° failed")

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

                    # Plugins that need to poll out the status from the thermostat
                    # could do so here, then broadcast back the new values to the
                    # Indigo Server.
                    self._refresh_states_from_hardware(dev, False, False)

                self.sleep(self.refresh_delay)
        except self.StopThread:
            pass    # Optionally catch the StopThread exception and do any needed cleanup.

    ########################################
    def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
        return (True, values_dict)

    ########################################
    def deviceStartComm(self, dev):
        # Called when communication with the hardware should be established.
        # Here would be a good place to poll out the current states from the
        # thermostat. If periodic polling of the thermostat is needed (that
        # is, it doesn't broadcast changes back to the plugin somehow), then
        # consider adding that to runConcurrentThread() above.
        self._refresh_states_from_hardware(dev, True, True)

    def deviceStopComm(self, dev):
        # Called when communication with the hardware should be shutdown.
        pass

    ########################################
    # Thermostat Action callback
    ######################
    # Main thermostat action bottleneck called by Indigo Server.
    def actionControlThermostat(self, action, dev):
        ###### SET HVAC MODE ######
        if action.thermostatAction == indigo.kThermostatAction.SetHvacMode:
            self._handle_change_hvac_mode_action(dev, action.actionMode)

        ###### SET FAN MODE ######
        elif action.thermostatAction == indigo.kThermostatAction.SetFanMode:
            self._handle_change_fan_mode_action(dev, action.actionMode)

        ###### SET COOL SETPOINT ######
        elif action.thermostatAction == indigo.kThermostatAction.SetCoolSetpoint:
            new_setpoint = action.actionValue
            self._handle_change_setpoint_action(dev, new_setpoint, "change cool setpoint", "setpointCool")

        ###### SET HEAT SETPOINT ######
        elif action.thermostatAction == indigo.kThermostatAction.SetHeatSetpoint:
            new_setpoint = action.actionValue
            self._handle_change_setpoint_action(dev, new_setpoint, "change heat setpoint", "setpointHeat")

        ###### DECREASE/INCREASE COOL SETPOINT ######
        elif action.thermostatAction == indigo.kThermostatAction.DecreaseCoolSetpoint:
            new_setpoint = dev.coolSetpoint - action.actionValue
            self._handle_change_setpoint_action(dev, new_setpoint, "decrease cool setpoint", "setpointCool")

        elif action.thermostatAction == indigo.kThermostatAction.IncreaseCoolSetpoint:
            new_setpoint = dev.coolSetpoint + action.actionValue
            self._handle_change_setpoint_action(dev, new_setpoint, "increase cool setpoint", "setpointCool")

        ###### DECREASE/INCREASE HEAT SETPOINT ######
        elif action.thermostatAction == indigo.kThermostatAction.DecreaseHeatSetpoint:
            new_setpoint = dev.heatSetpoint - action.actionValue
            self._handle_change_setpoint_action(dev, new_setpoint, "decrease heat setpoint", "setpointHeat")

        elif action.thermostatAction == indigo.kThermostatAction.IncreaseHeatSetpoint:
            new_setpoint = dev.heatSetpoint + action.actionValue
            self._handle_change_setpoint_action(dev, new_setpoint, "increase heat setpoint", "setpointHeat")

        ###### REQUEST STATE UPDATES ######
        elif action.thermostatAction in [indigo.kThermostatAction.RequestStatusAll, indigo.kThermostatAction.RequestMode,
        indigo.kThermostatAction.RequestEquipmentState, indigo.kThermostatAction.RequestTemperatures, indigo.kThermostatAction.RequestHumidities,
        indigo.kThermostatAction.RequestDeadbands, indigo.kThermostatAction.RequestSetpoints]:
            self._refresh_states_from_hardware(dev, True, False)

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
            # Query hardware module (dev) for its current status here. This differs from the
            # indigo.kThermostatAction.RequestStatusAll action - for instance, if your thermo
            # is battery powered you might only want to update it only when the user uses
            # this status request (and not from the RequestStatusAll). This action would
            # get all possible information from the thermostat and the other call
            # would only get thermostat-specific information:
            # ** GET BATTERY INFO **
            # and call the common function to update the thermo-specific data
            self._refresh_states_from_hardware(dev, True, False)
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

    ########################################
    # Actions defined in MenuItems.xml. In this case we just use these menu actions to
    # simulate different thermostat configurations (how many temperature and humidity
    # sensors they have).
    ####################
    def change_temp_sensor_count_to_1(self):
        self._change_all_temp_sensor_counts(1)

    def change_temp_sensor_count_to_2(self):
        self._change_all_temp_sensor_counts(2)

    def change_temp_sensor_count_to_3(self):
        self._change_all_temp_sensor_counts(3)

    def change_humidity_sensor_count_to_0(self):
        self._change_all_humidity_sensor_counts(0)

    def change_humidity_sensor_count_to_1(self):
        self._change_all_humidity_sensor_counts(1)

    def change_humidity_sensor_count_to_2(self):
        self._change_all_humidity_sensor_counts(2)

    def change_humidity_sensor_count_to_3(self):
        self._change_all_humidity_sensor_counts(3)


