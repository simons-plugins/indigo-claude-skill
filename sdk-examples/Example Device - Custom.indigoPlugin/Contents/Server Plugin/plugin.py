####################
# Copyright (c) 2024, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

import time

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
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug: bool = True
        self.time_warp_on: bool = False
        self.time_warp_count: int = 0
        self.state_updater_dev: indigo.Device = None
        self.server_time_dev: indigo.Device = None

    ########################################
    def startup(self: indigo.PluginBase):
        self.logger.debug("startup called")
        # Most plugins that expose new device types will depend on the user
        # creating the new device from the Indigo UI (just like a native device).
        #
        # However, it is also possible for the plugin to create the devices
        # automatically at runtime:
        if "Example Server Time" in indigo.devices:
            self.server_time_dev = indigo.devices["Example Server Time"]
        else:
            self.logger.info("creating test device: Example Server Time")
            self.server_time_dev = indigo.device.create(
                indigo.kProtocol.Plugin,
                "Example Server Time",
                "test device created by example plugin",
                deviceTypeId="serverTimeDevice"
            )
        # Override the state icon shown (in Indigo Touch and client Main Window)
        # for this device to be the timer image icon:
        self.server_time_dev.updateStateImageOnServer(indigo.kStateImageSel.TimerOn)
        if "Example State Updater" in indigo.devices:
            self.state_updater_dev = indigo.devices["Example State Updater"]
        else:
            self.logger.info("creating test device: Example State Updater")
            self.state_updater_dev = indigo.device.create(
                indigo.kProtocol.Plugin,
                "Example State Updater",
                "test state value updating device created by example plugin device",
                deviceTypeId="stateUpdater"
            )
        # Override the state icon shown (in Indigo Touch and client Main Window)
        # for this device to be the timer image icon:
        self.state_updater_dev.updateStateImageOnServer(indigo.kStateImageSel.TimerOn)

    def shutdown(self: indigo.PluginBase):
        self.logger.debug("shutdown called")
        key_value_list = [
            {'key': 'serverTimeSeconds', 'value': 0},
            {'key': 'serverSecondsEven', 'value': False},
            {'key': 'serverDateTime', 'value': "--"},
        ]
        self.server_time_dev.updateStatesOnServer(key_value_list)

    ########################################
    def runConcurrentThread(self: indigo.PluginBase) -> None:
        """
        If runConcurrentThread() is defined, then a new thread is automatically created
        and runConcurrentThread() is called in that thread after startup() has been called.

        runConcurrentThread() should loop forever and only return after self.stopThread
        becomes True. If this function returns prematurely then the plugin host process
        will log an error and attempt to call runConcurrentThread() again after several seconds.

        :return: None
        """
        try:
            while True:
                server_time = indigo.server.getTime()
                server_time_second = server_time.second
                if self.time_warp_on:
                    self.time_warp_count += 1
                    server_time_second = self.time_warp_count

                key_value_list = [
                    {'key': 'serverTimeSeconds', 'value': server_time_second},
                    {'key': 'serverSecondsEven', 'value': not bool(server_time_second % 2)},
                    {'key': 'serverDateTime', 'value': str(server_time)}
                ]
                self.server_time_dev.updateStatesOnServer(key_value_list)

                key_value_list = []
                if server_time_second % 2:
                    key_value_list.append({'key': 'alwaysInteger', 'value': 0})
                    key_value_list.append({'key': 'alwaysFloat', 'value': 0.01})
                    key_value_list.append({'key': 'stringToggleFloats', 'value': "0.0"})
                    key_value_list.append({'key': 'stringToggleStrings', 'value': "abc"})
                    key_value_list.append({'key': 'integerToFloat', 'value': 0})
                    key_value_list.append({'key': 'integerToString', 'value': 0})
                    key_value_list.append({'key': 'floatToString', 'value': 0.1})
                else:
                    key_value_list.append({'key': 'alwaysInteger', 'value': 1})
                    key_value_list.append({'key': 'alwaysFloat', 'value': 0.123456, 'decimalPlaced': 4})
                    key_value_list.append({'key': 'stringToggleFloats', 'value': "0.0000"})
                    key_value_list.append({'key': 'stringToggleStrings', 'value': "def"})
                    key_value_list.append({'key': 'integerToFloat', 'value': 0.1})
                    key_value_list.append({'key': 'integerToString', 'value': "abc"})
                    key_value_list.append({'key': 'floatToString', 'value': "abc"})
                key_value_list.append({'key': 'timeStamp', 'value': str(time.time()).split(".")[0]})
                try:
                    self.state_updater_dev.updateStatesOnServer(key_value_list)
                except Exception as exc:
                    self.logger.exception(exc)
                if self.time_warp_on:
                    self.sleep(0.12)
                else:
                    self.sleep(1)
        except self.StopThread:
            pass  # Optionally catch the StopThread exception and do any needed cleanup.

    ########################################
    # Actions defined in MenuItems.xml:
    ####################
    def time_warp(self: indigo.PluginBase):
        if not self.time_warp_on:
            self.logger.info("starting mega time warp")
            self.time_warp_on = True
        else:
            self.logger.info("stopping mega time warp")
            self.time_warp_on = False

    ########################################
    """
    Buttons and dynamic list methods defined for the scenes custom device

    Overview of scene devices:
        Scene devices are custom devices that will contain multiple devices.
        We implement this custom device by storing a comma-delimited list of
        device IDs which is manipulated by clicking Add and Delete buttons
        in the device config dialog. There are two dynamic list controls in
        the dialog:
            1) one popup button control on which the user selects a device
               to add then clicks the Add Device button.
            2) one list control which shows all the devices that have already
               been added to the scene and in which the user can select devices
               and click the Delete Devices button
        There is a hidden field "memberDevices" that stores a comma-delimited
        list of device ids for each member of the scene. The add_device and
        delete_devices methods will take the selections from the respective
        dynamic lists and do the right thing with the list.
        Finally, there are the two methods that build the dynamic lists.
        The method that builds the source list will inspect the "memberDevices"
        field and won't include those devices in the source list (so the user
        won't be confused by seeing a device that's already in the member list
        in the source list). The method that builds the member list of course
        uses "memberDevices" to build the list.

        One other thing that should be done probably - in the deviceStartComm
        method (or the appropriate CRUD methods if you're using them instead)
        you should check the IDs to make sure they're still around and if not
        remove them from the device id list.

        The device id list property ("memberDevices") could, of course, be
        formatted in some other way besides a comma-delimited list of ids
        if you need to store more information. You could, for instance, store
        some kind of formatted text like JSON or XML that had much more
        information.
    """

    def add_device(
            self: indigo.PluginBase,
            values_dict: indigo.Dict,
            type_id: str,
            dev_id: int
    ) -> indigo.Dict:
        """
        This is the method that's called by the Add Device button in the scene device config UI.

        :param values_dict: the values dict from the dialog
        :param type_id: the device type
        :param dev_id: the device id
        :return: an indigo.Dict that replaces the values dict
        """
        self.logger.debug("add_device called")
        # just making sure that they have selected a device in the source
        # list - it shouldn't be possible not to but it's safer
        if "sourceDeviceMenu" in values_dict:
            # Get the device ID of the selected device
            device_id = values_dict["sourceDeviceMenu"]
            if device_id == "":
                return None
            # Get the list of devices that have already been added to the "scene"
            # If the key doesn't exist then return an empty string indicating
            # no devices have yet been added. "memberDevices" is a hidden text
            # field in the dialog that holds a comma-delimited list of device
            # ids, one for each of the devices in the scene.
            dev_list_str = values_dict.get("memberDevices", "")
            self.logger.debug(f"adding device: {device_id} to {dev_list_str}")
            # If no devices have been added then just set the selected device string to
            # the device id of the device they selected in the popup
            if dev_list_str == "":
                dev_list_str = device_id
            # Otherwise append it to the end separated by a comma
            else:
                dev_list_str += f",{device_id}"
            # Set the device string back to the hidden text field that contains the
            # list of device ids that are in the scene
            values_dict["memberDevices"] = dev_list_str
            self.logger.debug(f"values_dict: {values_dict}")
            # Delete the selections on both dynamic lists since we don't
            # want to preserve those across dialog runs
            if "memberDeviceList" in values_dict:
                del values_dict["memberDeviceList"]
            if "sourceDeviceMenu" in values_dict:
                del values_dict["sourceDeviceMenu"]
            # return the new dict
            return values_dict

    def delete_devices(
            self: indigo.PluginBase,
            values_dict: indigo.Dict,
            type_id: str,
            dev_id: int
    ) -> indigo.Dict:
        """
        This is the method that's called by the Delete Device button in the scene device config UI.

        :param values_dict: the values dict from the dialog
        :param type_id: the device type
        :param dev_id: the device id
        :return: an indigo.Dict that replaces the values dict
        """
        self.logger.debug("delete_devices called")
        if "memberDevices" in values_dict:
            # Get the list of devices that are already in the scene
            devs_in_scene = []
            dev_list_str = values_dict.get("memberDevices", "")
            if dev_list_str:
                devs_in_scene = dev_list_str.split(",")
            # Get the devices they've selected in the list that they want
            # to remove
            sel_devs = values_dict.get("memberDeviceList", [])
            # Loop through the devices to be deleted list and remove them
            for device_id in sel_devs:
                self.logger.debug(f"remove device_id: {device_id}")
                if device_id in devs_in_scene:
                    devs_in_scene.remove(device_id)
            # Set the "memberDevices" field back to the new list which
            # has the devices deleted from it.
            values_dict["memberDevices"] = ",".join(devs_in_scene)
            # Delete the selections on both dynamic lists since we don't
            # want to preserve those across dialog runs
            if "memberDeviceList" in values_dict:
                del values_dict["memberDeviceList"]
            if "sourceDeviceMenu" in values_dict:
                del values_dict["sourceDeviceMenu"]
            return values_dict

    def source_devices(
            self: indigo.PluginBase,
            filter_str: str = "",
            values_dict: indigo.Dict = None,
            type_id: str = "",
            target_id: int = 0
    ) -> list:
        """
        This is the method that's called to build the source device list. Note that values_dict is read-only so any
        changes you make to it will be discarded.

        :param filter_str: unused string to filter device types
        :param values_dict: values from the dialog
        :param type_id: unused type of device
        :param target_id: unused ID of the target object
        :return: a list of device tuples in the form of (device.id, device.name)
        """
        self.logger.debug(f"source_devices called with filter: {filter_str}  type_id: {type_id}  target_id: {target_id}")
        return_list = []
        # if values_dict doesn't exist yet - if this is a brand new device
        # then we just create an empty dict so the rest of the logic will
        # work correctly. Many other ways to skin that particular cat.
        if not values_dict:
            values_dict = {}
        # Get the member device id list, loop over all devices, and if the device
        # id isn't in the member list then include it in the source list.
        device_list = []
        dev_list_str = values_dict.get("memberDevices", "")
        if dev_list_str:
            device_list = dev_list_str.split(",")
        for dev_id in indigo.devices.keys():
            if str(dev_id) not in device_list:
                return_list.append((str(dev_id), indigo.devices.get(dev_id).name))
        return return_list

    def member_devices(
            self: indigo.PluginBase,
            filter_str: str = "",
            values_dict: indigo.Dict = None,
            type_id: str = "",
            target_id: int = 0
    ) -> list:
        """
        This is the method that's called to build the member device list. Note that values_dict is read-only so any
        changes you make to it will be discarded.

        :param filter_str:
        :param values_dict:
        :param type_id:
        :param target_id:
        :return:
        """
        self.logger.debug(
            f"member_devices called with filter: {filter_str}  type_id: {type_id}  target_id: {target_id}"
        )
        return_list = []
        # values_dict may be empty or None if it's a brand new device
        if values_dict and "memberDevices" in values_dict:
            # Get the list of devices
            dev_list_str = values_dict["memberDevices"]
            self.logger.debug(f"memberDeviceString: {dev_list_str}")
            if dev_list_str:
                device_list = dev_list_str.split(",")
                # Iterate over the list and if the device exists (it could have been
                # deleted) then add it to the list.
                for dev_id in device_list:
                    if int(dev_id) in indigo.devices:
                        return_list.append((dev_id, indigo.devices[int(dev_id)].name))
        return return_list

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
        # If the type_id is "scene", we want to clear the selections on both
        # dynamic lists so that they're not stored since we really don't
        # care about those.
        self.logger.debug(f"validateDeviceConfigUi: type_id: {type_id}  dev_id: {dev_id}")
        if type_id == "scene":
            if "memberDeviceList" in values_dict:
                values_dict["memberDeviceList"] = ""
            if "sourceDeviceMenu" in values_dict:
                values_dict["sourceDeviceMenu"] = ""
        return (True, values_dict)

    ########################################
    # Plugin Actions object callbacks (action is an Indigo plugin action instance)
    ######################
    def reset_hardware(self: indigo.PluginBase, action: object) -> None:
        self.logger.debug(f"reset_hardware action called:\n {action}")

    def update_hardware_firmware(self: indigo.PluginBase, action: object) -> None:
        self.logger.debug(f"update_hardware_firmware action called:\n {action}")
