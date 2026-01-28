"""
Indigo Plugin Base Template

A complete starter template for an Indigo plugin with best practices.

Usage:
    1. Copy this file as plugin.py in your plugin's Server Plugin folder
    2. Rename the class if desired
    3. Update __init__ with your plugin-specific preferences
    4. Implement your plugin logic in the appropriate methods

Requirements:
    - Indigo 2023.2+ (Python 3.10+)
    - ServerApiVersion 3.0 in Info.plist
"""

import indigo
import logging


class Plugin(indigo.PluginBase):
    """Main plugin class.

    Inherits from indigo.PluginBase and provides the basic structure
    for an Indigo plugin with logging, configuration, and lifecycle management.
    """

    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        """Initialize the plugin.

        This method should ONLY initialize instance variables. No Indigo API
        calls, no network requests, no device communication.

        Args:
            pluginId: Unique identifier for the plugin
            pluginDisplayName: Display name from Info.plist
            pluginVersion: Version from Info.plist
            pluginPrefs: Plugin preferences dict
        """
        super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

        # Configure logging level from preferences
        self.debug = pluginPrefs.get("showDebugInfo", False)
        if self.debug:
            self.logger.debug("Debug logging enabled")

        # Initialize plugin-specific preferences
        self.update_frequency = int(pluginPrefs.get("updateFrequency", 60))

        # Initialize data structures
        self.devices_dict = {}

    ########################################
    # Plugin lifecycle methods
    ########################################

    def startup(self):
        """Start the plugin.

        Called after __init__() when the plugin is enabled. Use this to:
        - Initialize API clients
        - Subscribe to Indigo events
        - Load persistent data
        - Validate configuration

        Note: startup() is a pure callback - do NOT call super().startup()
        """
        self.logger.info(f"{self.pluginDisplayName} {self.pluginVersion} starting")

        # Example: Initialize API client
        # self.api_client = MyAPIClient(self.pluginPrefs.get("apiKey"))

        # Example: Subscribe to device changes
        # indigo.devices.subscribeToChanges()

    def shutdown(self):
        """Shutdown the plugin.

        Called when the plugin is disabled or Indigo quits. Use this to:
        - Close connections
        - Save persistent data
        - Clean up resources

        Note: shutdown() is a pure callback - do NOT call super().shutdown()
        """
        self.logger.info(f"{self.pluginDisplayName} shutting down")

        # Example: Clean up resources
        # if hasattr(self, 'api_client'):
        #     self.api_client.close()

    def runConcurrentThread(self):
        """Background thread for periodic tasks.

        This method runs continuously while the plugin is enabled. Use it for:
        - Polling APIs
        - Periodic device updates
        - Background monitoring

        IMPORTANT: Use self.sleep() instead of time.sleep() to allow clean shutdown.
        """
        self.logger.debug("Starting concurrent thread")

        try:
            while True:
                try:
                    # Your periodic task here
                    # Example: self._update_all_devices()
                    pass

                except Exception as exc:
                    # Catch exceptions to prevent thread from exiting
                    self.logger.exception("Error in concurrent thread")

                # Use self.sleep() for interruptible wait
                self.sleep(self.update_frequency)

        except self.StopThread:
            # Raised when plugin is being disabled
            self.logger.debug("Concurrent thread stopping")
            pass

    ########################################
    # Configuration callbacks
    ########################################

    def validatePrefsConfigUi(self, valuesDict):
        """Validate plugin configuration.

        Called when user saves plugin config. Validate all settings and
        return errors for invalid inputs.

        Args:
            valuesDict: Dictionary of configuration values

        Returns:
            Tuple of (valid, valuesDict, errorsDict)
        """
        errorsDict = indigo.Dict()

        # Example validation: Required field
        # if not valuesDict.get("apiKey"):
        #     errorsDict["apiKey"] = "API key is required"

        # Example validation: Numeric range
        # try:
        #     freq = int(valuesDict.get("updateFrequency", 60))
        #     if freq < 10:
        #         errorsDict["updateFrequency"] = "Update frequency must be at least 10 seconds"
        # except ValueError:
        #     errorsDict["updateFrequency"] = "Must be a valid number"

        if len(errorsDict):
            return False, valuesDict, errorsDict
        return True, valuesDict

    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        """Called when user closes plugin config dialog.

        Use this to apply configuration changes without requiring a restart.

        Args:
            valuesDict: Configuration values from UI
            userCancelled: True if user cancelled, False if they saved
        """
        if not userCancelled:
            self.debug = valuesDict.get("showDebugInfo", False)
            self.update_frequency = int(valuesDict.get("updateFrequency", 60))

            self.logger.info("Configuration updated")

    ########################################
    # Device callbacks
    ########################################

    def deviceStartComm(self, dev):
        """Start communication with a device.

        Called when a device is enabled or when the plugin starts with
        the device already enabled.

        Args:
            dev: The Indigo device object
        """
        super().deviceStartComm(dev)

        self.logger.info(f"Starting device: {dev.name}")

        # Initialize device-specific data
        self.devices_dict[dev.id] = {
            'last_update': None,
        }

        # Set initial state
        # dev.updateStateOnServer("onOffState", False)

    def deviceStopComm(self, dev):
        """Stop communication with a device.

        Called when a device is disabled or when the plugin is shutting down.

        Args:
            dev: The Indigo device object
        """
        super().deviceStopComm(dev)

        self.logger.info(f"Stopping device: {dev.name}")

        # Clean up device-specific data
        if dev.id in self.devices_dict:
            del self.devices_dict[dev.id]

    def validateDeviceConfigUi(self, valuesDict, typeId, devId):
        """Validate device configuration.

        Called when user saves device config.

        Args:
            valuesDict: Device configuration values
            typeId: Device type ID
            devId: Device ID

        Returns:
            Tuple of (valid, valuesDict, errorsDict)
        """
        errorsDict = indigo.Dict()

        # Example validation
        # if not valuesDict.get("address"):
        #     errorsDict["address"] = "Device address is required"

        if len(errorsDict):
            return False, valuesDict, errorsDict
        return True, valuesDict

    ########################################
    # Action callbacks
    ########################################

    def actionControlDevice(self, action, dev):
        """Handle device action requests.

        Called when user triggers a device action (turn on, turn off, etc).

        Args:
            action: The action object
            dev: The device object
        """
        # Turn On
        if action.deviceAction == indigo.kDeviceAction.TurnOn:
            self.logger.info(f"Turn on device: {dev.name}")
            # Implement turn on logic
            # dev.updateStateOnServer("onOffState", True)

        # Turn Off
        elif action.deviceAction == indigo.kDeviceAction.TurnOff:
            self.logger.info(f"Turn off device: {dev.name}")
            # Implement turn off logic
            # dev.updateStateOnServer("onOffState", False)

        # Toggle
        elif action.deviceAction == indigo.kDeviceAction.Toggle:
            self.logger.info(f"Toggle device: {dev.name}")
            # new_state = not dev.onState
            # dev.updateStateOnServer("onOffState", new_state)

    ########################################
    # Custom methods
    ########################################

    def _update_all_devices(self):
        """Update all devices.

        Private method to update all plugin devices. Called from
        concurrent thread or on-demand.
        """
        for dev_id in self.devices_dict:
            try:
                dev = indigo.devices[dev_id]
                self._update_device(dev)
            except Exception as exc:
                self.logger.exception(f"Error updating device {dev_id}")

    def _update_device(self, dev):
        """Update a single device.

        Args:
            dev: The Indigo device to update
        """
        # Implement device update logic
        pass
