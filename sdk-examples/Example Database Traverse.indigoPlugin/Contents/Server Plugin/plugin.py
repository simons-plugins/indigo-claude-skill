####################
# Copyright (c) 2024, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

DIVIDER_WIDTH = 50  # used to determine the width of the section/element dividers in the event log
LABEL_WIDTH = 16  # used to right-justify element labels

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
    # IOM logging methods
    ####################
    def log_elem_divider(self: indigo.PluginBase, character: str = "-") -> None:
        """
        Clever way of generating a section divider, something like:
          --------------------------------------------------

        :param character: the character to use for the divider, default to dash.
        :return: None
        """
        self.logger.info("".join([character for x in range(DIVIDER_WIDTH)]))

    def log_list_divider(self: indigo.PluginBase, section_name: str) -> None:
        """
        This method writes out a header for a new section into the log file.

        :param section_name: name of the section to print
        :return: None
        """
        self.log_elem_divider("=")
        self.logger.info(section_name)
        self.log_elem_divider()

    def log_element(self: indigo.PluginBase, label: str, value: any) -> None:
        """
        Simple method to log a formatted value.

        :param label: the label to use for this log line
        :param value: the value to use for this log line
        :return: None
        """
        self.logger.info(f"{label.upper() : >{LABEL_WIDTH}}:  {value}")

    def log_base_elem(self: indigo.PluginBase, elem: any, folders: indigo.List) -> None:
        """
        Method to log a common parts of an element.

        :param elem: an Indigo object instance: device, trigger, action group, etc.
        :param folders: the list of folders available for instance type
        :return: Non e
        """
        self.log_element("instance", elem.__class__.__name__)
        if len(elem.description) > 0:
            self.log_element("description", elem.description)
        if folders and elem.folderId != 0:
            self.log_element("in folder", folders.getName(elem.folderId))
        self.log_element("remote display", elem.remoteDisplay)

    def log_base_folder(self: indigo.PluginBase, elem: any) -> None:
        """
        Log a folder's common parts.

        :param elem: a folder instance
        :return: None
        """
        if len(elem.description) > 0:
            self.log_element("description", elem.description)
        self.log_element("remote display", elem.remoteDisplay)

    ########################################
    def log_device_base(self: indigo.PluginBase, elem: any) -> None:
        """
        Log the common device bits for every device.

        :param elem: a device instance
        :return: None
        """
        self.log_base_elem(elem, indigo.devices.folders)
        self.log_element("protocol", elem.protocol)
        self.log_element("model name", elem.model)
        self.log_element("address", (elem.address or "--"))
        if elem.protocol == indigo.kProtocol.Insteon and elem.buttonGroupCount > 0:
            self.log_element("button count", elem.buttonGroupCount)
        self.log_element("last changed", elem.lastChanged)

        supported_props: list = []
        # This is just a subset of supports* properties that a device can have.
        property_list = ["supportsColor", "supportsOnState", "supportsEnergyMeter", "supportsPowerMeter", "supportsStatusRequest"]
        for property in property_list:
            supports_property = getattr(elem, property, False)
            if supports_property:
                supported_props.append(property)
        if len(supported_props) == 0:
            supports = "--"
        else:
            supports = ", ".join(supported_props)
        self.log_element("supports", supports)

    ####################
    def log_device_sensor(self: indigo.PluginBase, elem: any) -> None:
        """
        Log sensor states.

        :param elem: a sensor device
        :return: None
        """
        self.log_device_base(elem)
        if elem.supportsOnState:
            self.log_element("is on", elem.onState)
        if elem.supportsSensorValue:
            self.log_element("value", elem.sensorValue)

    ####################
    def log_device_relay(self: indigo.PluginBase, elem: any) -> None:
        """
        Log relay (on/off) device stuff

        :param elem: a relay device instance
        :return: None
        """
        self.log_device_base(elem)
        self.log_element("is on", elem.onState)

    ####################
    def log_device_dimmer(self: indigo.PluginBase, elem: any) -> None:
        """
        Log dimmer info

        :param elem: dimmer device
        :return: None
        """
        # All dimmer devices are also relay devices, so log that information first
        self.log_device_relay(elem)
        self.log_element("brightness", elem.brightness)

    ####################
    def log_device_multi_io(self: indigo.PluginBase, elem: any) -> None:
        """
        Log I/O device info

        :param elem: i/o device
        :return: None
        """
        self.log_device_base(elem)
        if elem.analogInputCount > 0:
            self.log_element("analog inputs", elem.analogInputs)
        if elem.binaryInputCount > 0:
            self.log_element("binary inputs", elem.binaryInputs)
        if elem.sensorInputCount > 0:
            self.log_element("sensor inputs", elem.sensorInputs)
        if elem.binaryOutputCount > 0:
            self.log_element("binary outputs", elem.binaryOutputs)

    ####################
    def log_device_sprinkler(self: indigo.PluginBase, elem: any) -> None:
        """
        Log sprinkler info

        :param elem: sprinkler device
        :return: None
        """
        self.log_device_base(elem)
        self.log_element("zone count", elem.zoneCount)
        self.log_element("zone names", elem.zoneNames)
        self.log_element("max durations", elem.zoneMaxDurations)
        if len(elem.zoneScheduledDurations) > 0:
            self.log_element("scheduled dura.", elem.zoneScheduledDurations)
        if elem.activeZone:
            self.log_element("active zone", elem.zoneNames[elem.activeZone])

    ####################
    def log_device_thermostat(self: indigo.PluginBase, elem: any) -> None:
        """
        Log thermostat info

        :param elem: thermostat device
        :return: None
        """
        self.log_device_base(elem)
        self.log_element("hvac mode", elem.hvacMode)
        self.log_element("fan mode", elem.fanMode)
        self.log_element("cool setpoint", elem.coolSetpoint)
        self.log_element("heat setpoint", elem.heatSetpoint)
        self.log_element("temp count", elem.temperatureSensorCount)
        self.log_element("temps", elem.temperatures)
        self.log_element("humidity count", elem.humiditySensorCount)
        self.log_element("humidities", elem.humidities)
        self.log_element("cool is on", elem.coolIsOn)
        self.log_element("heat is on", elem.heatIsOn)
        self.log_element("fan is on", elem.fanIsOn)

    ####################
    def log_device(self: indigo.PluginBase, elem: any) -> None:
        """
        Method to log device details based on the device type

        :param elem: indigo device instance
        :return: None
        """
        if isinstance(elem, indigo.DimmerDevice):
            self.log_device_dimmer(elem)
        elif isinstance(elem, indigo.RelayDevice):
            self.log_device_relay(elem)
        elif isinstance(elem, indigo.SensorDevice):
            self.log_device_sensor(elem)
        elif isinstance(elem, indigo.MultiIODevice):
            self.log_device_multi_io(elem)
        elif isinstance(elem, indigo.SprinklerDevice):
            self.log_device_sprinkler(elem)
        elif isinstance(elem, indigo.ThermostatDevice):
            self.log_device_thermostat(elem)
        else:
            self.log_device_base(elem)

    ########################################
    def log_event_base(self: indigo.PluginBase, elem: any, folders) -> None:
        self.log_base_elem(elem, folders)
        self.log_element("enabled", elem.enabled)
        self.log_element("upload", elem.upload)
        if elem.suppressLogging:
            self.log_element("suppress logging", "True")
        # TODO: Need to add conditional tree and action list traversal here.

    ####################
    def log_trigger(self: indigo.PluginBase, elem: any) -> None:
        self.log_event_base(elem, indigo.triggers.folders)

        if isinstance(elem, indigo.DeviceStateChangeTrigger):
            self.log_element("device", indigo.devices.getName(elem.deviceId))
            self.log_element("change type", elem.stateChangeType)
            self.log_element("selector key", elem.stateSelector)
            if elem.stateSelectorIndex > 0:
                self.log_element("selector index", elem.stateSelectorIndex)
            if len(elem.stateValue) > 0:
                self.log_element("state value", elem.stateValue)
        elif isinstance(elem, indigo.VariableValueChangeTrigger):
            self.log_element("variable", indigo.variables.getName(elem.variableId))
            self.log_element("change type", elem.variableChangeType)
            if len(elem.variableValue) > 0:
                self.log_element("variable value", elem.variableValue)
        elif isinstance(elem, indigo.InsteonCommandReceivedTrigger):
            self.log_element("insteon command", elem.command)
            self.log_element("source type", elem.commandSourceType)
            self.logger.info(f"     SOURCE TYPE:  {elem.commandSourceType}")
            if elem.commandSourceType == indigo.kDeviceSourceType.DeviceId:
                self.log_element("device", indigo.devices.getName(elem.deviceId))
                self.log_element("group num", elem.buttonOrGroup)
            self.logger.info(f"       GROUP NUM:  {elem.buttonOrGroup}")
        elif isinstance(elem, indigo.X10CommandReceivedTrigger):
            self.log_element("X10 command", elem.command)
            self.log_element("source type", elem.commandSourceType)
            if elem.commandSourceType == indigo.kDeviceSourceType.DeviceId:
                self.log_element("device", indigo.devices.getName(elem.deviceId))
            elif elem.commandSourceType == indigo.kDeviceSourceType.RawAddress:
                self.log_element("address", elem.address)
            elif elem.command == indigo.kX10Cmd.AvButtonPressed:
                self.log_element("a/v button", elem.avButton)
        elif isinstance(elem, indigo.EmailReceivedTrigger):
            self.log_element("email filter", elem.emailFilter)
            if elem.emailFilter == indigo.kEmailFilter.MatchEmailFields:
                self.log_element("from filter", elem.emailFrom)
                self.log_element("subject filter", elem.emailSubject)

    ####################
    def log_schedule(self: indigo.PluginBase, elem: any) -> None:
        self.log_event_base(elem, indigo.schedules.folders)
        self.log_element("date type", elem.dateType)
        self.log_element("time type", elem.timeType)
        if elem.dateType == indigo.kDateType.Absolute and elem.timeType == indigo.kTimeType.Absolute:
            self.log_element("date and time", elem.absoluteDateTime)
        elif elem.dateType == indigo.kDateType.Absolute:
            self.log_element("absolute date", elem.absoluteDate.date())
        elif elem.timeType == indigo.kTimeType.Absolute:
            self.log_element("absolute time", elem.absoluteTime.time())
        if elem.sunDelta > 0:
            self.log_element("sun delta", f"{elem.sunDelta} seconds")
        if elem.randomizeBy > 0:
            self.log_element("randomize by", f"{elem.randomizeBy} seconds")
        try:
            self.log_element("next execution", elem.nextExecution)
        except:
            self.log_element("next execution", "- none scheduled -")
        # TODO: Need to log additional properties after they are implemented here.

    ####################
    def log_action_group(self: indigo.PluginBase, elem: any):
        self.log_base_elem(elem, indigo.actionGroups.folders)
        # TODO: Need to add action list traversal here.

    ####################
    def log_control_page(self: indigo.PluginBase, elem: any) -> None:
        self.log_base_elem(elem, indigo.controlPages.folders)
        self.log_element("hide tab bar", elem.hideTabBar)
        if len(elem.backgroundImage) > 0:
            self.log_element("background image", elem.backgroundImage)
        # TODO: Need to log additional properties after they are implemented here.
        # TODO: Need to add control list traversal here.

    ####################
    def log_variable(self: indigo.PluginBase, elem: any) -> None:
        self.log_base_elem(elem, indigo.variables.folders)
        self.log_element("value", elem.value)
        if elem.readOnly:
            self.log_element("read only", "True")

    ########################################
    # Actions defined in MenuItems.xml:
    ####################
    def traverse_devices(self: indigo.PluginBase) -> None:
        """
        This is called when the Log Devices menu item is selected.

        :return: None
        """
        self.log_list_divider("DEVICES")
        for folder in indigo.devices.folders:
            self.log_element("folder", folder.name)
            self.log_base_folder(folder)
        for elem in indigo.devices:
            self.log_elem_divider()
            self.log_element("device", elem.name)
            self.log_device(elem)

    def traverse_triggers(self: indigo.PluginBase) -> None:
        """
        This is called when the Log Triggers menu item is selected.

        :return: None
        """
        self.log_list_divider("TRIGGERS")
        for folder in indigo.triggers.folders:
            self.log_element("folder", folder.name)
            self.log_base_folder(folder)
        for elem in indigo.triggers:
            self.log_elem_divider()
            self.log_element("trigger", elem.name)
            self.log_trigger(elem)

    def traverse_schedules(self: indigo.PluginBase) -> None:
        """
        This is called when the Log Schedules menu item is selected.

        :return: None
        """
        self.log_list_divider("SCHEDULES")
        for folder in indigo.schedules.folders:
            self.log_element("folder", folder.name)
            self.log_base_folder(folder)
        for elem in indigo.schedules:
            self.log_elem_divider()
            self.log_element("schedule", elem.name)
            self.log_schedule(elem)

    def traverse_action_groups(self: indigo.PluginBase) -> None:
        """
        This is called when the Log Action Groups menu item is selected.

        :return: None
        """
        self.log_list_divider("ACTION GROUPS")
        for folder in indigo.actionGroups.folders:
            self.log_element("folder", folder.name)
            self.log_base_folder(folder)
        for elem in indigo.actionGroups:
            self.log_elem_divider()
            self.log_element("action group", elem.name)
            self.log_action_group(elem)

    def traverse_control_pages(self: indigo.PluginBase) -> None:
        """
        This is called when the Log Control Pages menu item is selected.

        :return: None
        """
        self.log_list_divider("CONTROL PAGES")
        for folder in indigo.controlPages.folders:
            self.log_element("folder", folder.name)
            self.log_base_folder(folder)
        for elem in indigo.controlPages:
            self.log_elem_divider()
            self.log_element("control page", elem.name)
            self.log_control_page(elem)

    def traverse_variables(self: indigo.PluginBase) -> None:
        """
        This is called when the Log Variables menu item is selected.

        :return: None
        """
        self.log_list_divider("VARIABLES")
        for folder in indigo.variables.folders:
            self.log_element("folder", folder.name)
            self.log_base_folder(folder)
        for elem in indigo.variables:
            self.log_elem_divider()
            self.log_element("variable", elem.name)
            self.log_variable(elem)

    ####################
    def traverse_database(self: indigo.PluginBase) -> None:
        """
        This is called when the Log Entire Database menu item is selected.

        :return: None
        """
        self.traverse_devices()
        self.traverse_triggers()
        self.traverse_schedules()
        self.traverse_action_groups()
        self.traverse_control_pages()
        self.traverse_variables()
