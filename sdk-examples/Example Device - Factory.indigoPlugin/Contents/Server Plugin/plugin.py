####################
# Copyright (c) 2024, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
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
        """
        The init method that is called when a plugin is first instantiated.

        :param plugin_id: the ID string of the plugin from Info.plist
        :param plugin_display_name: the name string of the plugin from Info.plist
        :param plugin_version: the version string from Info.plist
        :param plugin_prefs: an indigo.Dict containing the prefs for the plugin
        :param kwargs: passthrough for any other keyword args
        :return: None
        """
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs)
        self.debug: bool = True

    ########################################
    def startup(self: indigo.PluginBase) -> None:
        """
        Any logic needed at startup, but after __init__ is called.

        :return:
        """
        self.logger.debug("startup called")

    def shutdown(self: indigo.PluginBase) -> None:
        """
        Any cleanup logic needed before the plugin is completely shut down.

        :return: None
        """
        self.logger.debug("shutdown called")

    ########################################
    # DeviceFactory methods (specified in Devices.xml):
    #
    # All device factory methods are passed a dev_id_list argument, which is
    # a list of device IDs in the current group being edited. Plugins add
    # and remove devices to/from the group by making indigo.device.create()
    # and indigo.device.delete(). On subsequent factory method calls the
    # dev_id_list will automatically be updated to reflect any changes.
    #
    # Plugins should set the main model type using dev.model, and the sub-
    # type using dev.subType, which is used for the tabbed UI. Be sure
    # and call dev.replaceOnServer() after modifying the .model and .subType
    # attributes to push those changes to the server.
    ####################
    def getDeviceFactoryUiValues(self: indigo.PluginBase, dev_id_list: indigo.List) -> tuple:
        """
        You can implement this method to "prime" values that will be inserted into the device factory dialog. This
        allows you to do calculated values beyond just the ability to specify a static default in the XML.

        :param dev_id_list: list of device IDs that are in the group
        :return: a tuple with the values_dict and error_msg_dict for the dialog
        """
        values_dict: indigo.Dict = indigo.Dict()
        error_msg_dict: indigo.Dict = indigo.Dict()
        return (values_dict, error_msg_dict)

    def validateDeviceFactoryUi(self: indigo.PluginBase, values_dict: indigo.Dict, dev_id_list: indigo.List) -> tuple:
        """
        Called when a device factory dialog needs to be validated.

        :param values_dict: the dict of values from the dialog
        :param dev_id_list: the list of grouped device IDs
        :return: a tuple with the validation success (boolean), the values_dict and error_msg_dict for the dialog
        """
        errors_dict: indigo.Dict = indigo.Dict()
        return (True, values_dict, errors_dict)

    def closedDeviceFactoryUi(self: indigo.PluginBase, values_dict: indigo.Dict, user_cancelled: bool, dev_id_list: indigo.List) -> None:
        """
        Called when the device factory dialog has closed (after validation return success or is canceled).

        :param values_dict: the dict of values from the dialog
        :param user_cancelled: boolean that will be true if the user canceled the dialog
        :param dev_id_list: the list of grouped device IDs
        :return: None
        """
        return

    ####################
    def _get_device_group_list(self: indigo.PluginBase, filter: str, values_dict: indigo.Dict, dev_id_list: indigo.List) -> list:
        """
        Generates a list of device names tuples from the dev_id_list, suitable for use when populating a UI popup menu
        control.

        :param filter: an optional filter string
        :param values_dict: the dict of values from the dialog
        :param dev_id_list: the list of grouped device IDs
        :return: list of tuples, defined as (DEVICEID, DEVICENAME), to be used in a dialog popup menu control
        """
        menu_items = []
        for dev_id in dev_id_list:
            if dev_id in indigo.devices:
                dev = indigo.devices[dev_id]
                dev_name = dev.name
            else:
                dev_name = "- device not found -"
            menu_items.append((dev_id, dev_name))
        return menu_items

    def _add_relay(self: indigo.PluginBase, values_dict: indigo.Dict, dev_id_list: indigo.List) -> indigo.Dict:
        newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="myRelayType")
        newdev.model = "Example Multi-Device"
        newdev.subType = "Relay"        # Manually need to set the model and subType names (for UI only)
        newdev.replaceOnServer()
        return values_dict

    def _add_dimmer(self: indigo.PluginBase, values_dict: indigo.Dict, dev_id_list: indigo.List) -> indigo.Dict:
        newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="myDimmerType")
        newdev.model = "Example Multi-Device"
        newdev.subType = "Dimmer"       # Manually need to set the model and subType names (for UI only)
        newdev.replaceOnServer()
        return values_dict

    def _add_x10_motion_sensor(
            self: indigo.PluginBase,
            values_dict: indigo.Dict,
            dev_id_list: indigo.List
    ) -> indigo.Dict:
        # Not fully supported -- device groups currently should only contain
        # devices defined by the plugin. The UI doesn't properly handle showing
        # and editing X10 / INSTEON / etc. devices as part of the group.
        #
        # newdev = indigo.device.create(indigo.kProtocol.X10, deviceTypeId="Motion Detector")
        # newdev.model = "Example Multi-Device"
        # newdev.subType = "Motion" # Manually need to set the model and subType names (for UI only)
        # newdev.replaceOnServer()
        return values_dict

    def _add_x10_sprinkler_device(
            self: indigo.PluginBase,
            values_dict: indigo.Dict,
            dev_id_list: indigo.List
    ) -> indigo.Dict:
        # Not fully supported -- device groups currently should only contain
        # devices defined by the plugin. The UI doesn't properly handle showing
        # and editing X10 / INSTEON / etc. devices as part of the group.
        #
        # newdev = indigo.device.create(indigo.kProtocol.X10, deviceTypeId="Rain8 (8 zone)")
        # newdev.model = "Example Multi-Device"
        # newdev.subType = "Sprinkler"  # Manually need to set the model and subType names (for UI only)
        # newdev.replaceOnServer()
        return values_dict

    def _remove_dimmer_devices(
            self: indigo.PluginBase,
            values_dict: indigo.Dict,
            dev_id_list: indigo.List
    ) -> indigo.Dict:
        for dev_id in dev_id_list:
            try:
                dev = indigo.devices[dev_id]
                if dev.deviceTypeId == "myDimmerType":
                    indigo.device.delete(dev)
            except:
                pass    # delete doesn't allow (throws) on root elem
        return values_dict

    def _remove_relay_devices(
            self: indigo.PluginBase,
            values_dict: indigo.Dict,
            dev_id_list: indigo.List
    ) -> indigo.Dict:
        for dev_id in dev_id_list:
            try:
                dev = indigo.devices[dev_id]
                if dev.deviceTypeId == "myRelayType":
                    indigo.device.delete(dev)
            except:
                pass    # delete doesn't allow (throws) on root elem
        return values_dict

    def _remove_all_devices(
            self: indigo.PluginBase,
            values_dict: indigo.Dict,
            dev_id_list: indigo.List
    ) -> indigo.Dict:
        for dev_id in dev_id_list:
            try:
                indigo.device.delete(dev_id)
            except:
                pass    # delete doesn't allow (throws) on root elem
        return values_dict

    ########################################
    def validateDeviceConfigUi(self: indigo.PluginBase, values_dict: indigo.Dict, type_id: str, dev_id: int) -> tuple:
        return (True, values_dict)

    ########################################
    # Relay / Dimmer Action callback
    ######################
    def actionControlDevice(self, action, dev):
        ###### TURN ON ######
        if action.deviceAction == indigo.kDeviceAction.TurnOn:
            # Command hardware module (dev) to turn ON here:
            # ** IMPLEMENT ME **
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" on")

                # And then tell the Indigo Server to update the state.
                dev.updateStateOnServer("onOffState", True)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" on failed")

        ###### TURN OFF ######
        elif action.deviceAction == indigo.kDeviceAction.TurnOff:
            # Command hardware module (dev) to turn OFF here:
            # ** IMPLEMENT ME **
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" off")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("onOffState", False)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" off failed")

        ###### TOGGLE ######
        elif action.deviceAction == indigo.kDeviceAction.Toggle:
            # Command hardware module (dev) to toggle here:
            # ** IMPLEMENT ME **
            new_on_state = not dev.onState
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" toggle")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("onOffState", new_on_state)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" toggle failed")

        ###### SET BRIGHTNESS ######
        elif action.deviceAction == indigo.kDeviceAction.SetBrightness:
            # Command hardware module (dev) to set brightness here:
            # ** IMPLEMENT ME **
            new_brightness = action.actionValue
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" set brightness to {new_brightness}")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("brightnessLevel", new_brightness)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" set brightness to {new_brightness} failed")

        ###### BRIGHTEN BY ######
        elif action.deviceAction == indigo.kDeviceAction.BrightenBy:
            # Command hardware module (dev) to do a relative brighten here:
            # ** IMPLEMENT ME **
            new_brightness = min(dev.brightness + action.actionValue, 100)
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" brighten to {new_brightness}")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("brightnessLevel", new_brightness)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" brighten to {new_brightness} failed")

        ###### DIM BY ######
        elif action.deviceAction == indigo.kDeviceAction.DimBy:
            # Command hardware module (dev) to do a relative dim here:
            # ** IMPLEMENT ME **
            new_brightness = max(dev.brightness - action.actionValue, 0)
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" dim to {new_brightness}")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("brightnessLevel", new_brightness)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" dim to {new_brightness} failed")


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
