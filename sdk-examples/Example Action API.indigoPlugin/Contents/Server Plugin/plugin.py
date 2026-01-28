####################
# Copyright (c) 2024, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

import json
import yaml
import dicttoxml

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

        :return:
        """
        self.logger.debug("shutdown called")

    @staticmethod
    def validate_device_info_action(dev_id: int, props: indigo.Dict) -> tuple:
        """
        This static method will validate the device information in the specified props dictionary.

        :param dev_id: ID of the device to check
        :param props: dictionary of props to validate against
        :return: a tuple: (False, errors) or (True, empty_dict)
        """
        errors: indigo.Dict = indigo.Dict()
        if dev_id not in indigo.devices:
            errors["device"] = "'deviceId' must be included and must represent an existing device"
        if "format" not in props:
            errors["format"] = "'format' parameter is missing"
        elif props["format"] not in ["json", "xml", "yaml"]:
            errors["format"] = f"{props['format']} must be one of: 'json', 'xml', 'yaml'"
        return (len(errors) == 0, errors)

    ########################################
    def get_device_info(
            self: indigo.PluginBase,
            action: any,
            dev: indigo.Device = None,
            caller_waiting_for_result: bool = None
    ) -> indigo.Dict:
        """
        This handler is used to generate a simple api that returns device details for the specified device id. We lifted
        this example from the HTTP Responder plugin, but rather than return an HTML page, we'll just return an
        indigo.Dict to the caller for the device.

        We will also illustrate a pattern you can use for validating actions, both actions called as an API and actions
        configured and called through the UI. Historically, all validation has been done in the validate*ConfigUI
        methods, but for actions which can also be called from scripts or other plugins, that will not suffice since
        they construct their own properties to pass to the action and those aren't passed through the validate methods.
        It is also possible that the conditions will change at runtime from when the user configured the action - the
        most obvious scenario is if the user specifies substitution patterns in the action config. Since those values
        will most often change between the time the action was configured and the time the action runs, it's usually
        prudent to validate just before the action runs.

        The first part is the ID of a device and the extension as the type of content to return. We only do XML and JSON
        in this example. There is an optional arg to return JSON that doesn't have indents, which means it would be
        smaller. condense-json can be any value at all and it will skip the formatting with indents.

        :param action: action.props contains all the information passed from the action config or executeAction call
        :param dev: device whose details to return in the appropriate format
        :param caller_waiting_for_result: this will be true if it's an API call or false if it's called via the server
        :return: a reply dict with the content value being JSON or XML representation of a device instance.
        """
        # This will hold the status and errors or device details in the appropriate format
        reply_dict: indigo.Dict = indigo.Dict()
        # Get a copy of the props dictionary as a Python dict.
        props: dict = dict(action.props)
        is_valid: bool
        errors: indigo.Dict
        # Validate the device information in the action props
        is_valid, errors = self.validate_device_info_action(dev.id, action.props)
        # Add the validation status to the reply dict
        reply_dict["status"] = is_valid
        if not is_valid:
            # If it's not valid, we're going to log and add the errors to the reply dict
            if caller_waiting_for_result:
                self.logger.error(
                    f"Couldn't complete 'get_device_info' scripting action because of errors:\n{dict(errors)}")
            else:
                self.logger.error(f"Couldn't complete 'Get Device Info' action because of errors:\n{dict(errors)}")
            reply_dict["errors"] = errors
        else:
            # If the validation passes, we generate a dict from the device, convert it to the requested format, and
            # add it to the reply.
            device_dict: dict = dict(dev)
            if props["format"] == "yaml":
                reply_dict["deviceInfo"] = yaml.dump(device_dict)
            elif props["format"] == "xml":
                reply_dict["deviceInfo"] = dicttoxml.dicttoxml(device_dict)
            else:
                reply_dict["deviceInfo"] = json.dumps(device_dict, indent=2, cls=indigo.utils.JSONDateEncoder)
            if not caller_waiting_for_result:
                # We're only going to write to the log if it's called from the UI action
                self.logger.info(f"Device details for device '{dev.name}':\n{reply_dict['deviceInfo']}")
        return reply_dict

    ########################################
    def validateActionConfigUi(self: indigo.PluginBase, values_dict: indigo.Dict, type_id: str, dev_id: int) -> tuple:
        """
        If the type_id is "scene", we want to clear the selections on both
        dynamic lists so that they're not stored since we really don't
        care about those.

        :param values_dict: an indigo.Dict instance with the values from the config UI
        :param type_id: a type id for the action
        :param dev_id: a device id
        :return: a tuple with a bool, the values dict, and an optional errors dict.
        """
        self.logger.debug(f"validateDeviceConfigUi: type_id: {type_id}  dev_id: {dev_id}")
        if type_id == "get_device_info":
            # Here we validate the configuration for the "get_device_info" action (the only one currently).
            is_valid: bool
            errors: indigo.Dict
            # Validate the device information
            is_valid, errors = self.validate_device_info_action(dev_id, values_dict)
            return (is_valid, values_dict, errors)
        else:
            # If we had other actions in Actions.xml, we would do a different validation here.
            return (True, values_dict)
