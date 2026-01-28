####################
# Copyright (c) 2024, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

# Plugin ID of the Example Custom Broadcaster plugin (taken from its Info.plist file):
BROADCASTER_PLUGINID = "com.perceptiveautomation.indigoplugin.custom-broadcaster"

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
        self.debug: bool = True

    ########################################
    def startup(self: indigo.PluginBase) -> None:
        """
        Any logic needed at startup, but after __init__ is called.

        :return: None
        """
        self.logger.debug("startup called -- subscribing to messages from Example Custom Broadcaster plugin")
        # The Example Custom Broadcaster plugin defines three broadcast keys: broadcasterStarted,
        # broadcasterShutdown, and colorChanged. We subscribe to notifications of all three. The
        # second argument is the broadcast key used by the broadcasting plugin, the third argument
        # is the name of our callback method. In this case they are the same, but they don't have
        # to be.
        indigo.server.subscribeToBroadcast(BROADCASTER_PLUGINID, "broadcasterStarted", "broadcasterStarted")
        indigo.server.subscribeToBroadcast(BROADCASTER_PLUGINID, "broadcasterShutdown", "broadcasterShutdown")
        indigo.server.subscribeToBroadcast(BROADCASTER_PLUGINID, "colorChanged", "colorChanged")

    def shutdown(self: indigo.PluginBase) -> None:
        """
        Any cleanup logic needed before the plugin is completely shut down.

        :return: None
        """
        self.logger.debug("shutdown called")

    ########################################
    def broadcasterStarted(self: indigo.PluginBase) -> None:
        """
        This method will be called when we receive the "broadcasterStarted" message from the Example Custom Broadcaster
        plugin.

        :return: None
        """
        self.logger.info("received broadcasterStarted message")

    def broadcasterShutdown(self: indigo.PluginBase) -> None:
        """
        This method will be called when we receive the "broadcasterShutdown" message from the Example Custom Broadcaster
        plugin.

        :return: None
        """
        self.logger.info("received broadcasterShutdown message")

    def colorChanged(self: indigo.PluginBase, arg: any) -> None:
        """
        This method will be called when we receive the "colorChanged" message from the Example Custom Broadcaster
        plugin. For this example, 'arg' will be a color string, like "blue" or "black".

        :return: None
        """
        self.logger.info(f"received colorChanged message: {arg}")
