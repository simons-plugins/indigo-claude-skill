####################
# Copyright (c) 2024, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

import random

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

        :return: None
        """
        self.logger.debug("startup called -- broadcasting startup to all subscribers")
        # Broadcast to all listeners that we have started using the "broadcasterStarted"
        # broadcast key. Note the key is arbitrary and will just be used by the
        # subscribers in their subscribeToBroadcast() call.
        indigo.server.broadcastToSubscribers("broadcasterStarted")

    def shutdown(self: indigo.PluginBase) -> None:
        """
        Any cleanup logic needed before the plugin is completely shut down.

        :return: None
        """
        self.logger.debug("shutdown called -- broadcasting shutdown to all subscribers")
        # Broadcast to all listeners that we have shutdown using the "broadcasterShutdown"
        # broadcast key.
        indigo.server.broadcastToSubscribers("broadcasterShutdown")

    ########################################
    def runConcurrentThread(self: indigo.PluginBase) -> None:
        """
        This method, if defined, will be started up in a separate thread, so that it runs in parallel with the main
        plugin thread which processes all the other method calls. Note that it should be called with an infinite
        loop wrapped in a try block which catches self.StopThread, which is your signal that the plugin is about to
        shut down.

        :return: None
        """
        try:
            # Every 3 seconds broadcast to subscribers a new random color from our list:
            color_list = ["red", "green", "blue", "indigo", "orange", "black", "white", "magento", "silver", "gold"]
            while True:
                color = color_list[random.randint(0, len(color_list)-1)]
                # broadcastToSubscribers can take an additional argument to be passed to
                # the subscribers. Allowed types include basic python objects: string, number,
                # boolean, dict, or list. For server performance please keep the data size
                # sent small (a few kilobytes at most), and try not to broadcast more frequently
                # than once per second. Bursts of higher data rates should be fine.
                indigo.server.broadcastToSubscribers("colorChanged", color)
                self.sleep(3)
        except self.StopThread:
            pass  # Optionally catch the StopThread exception and do any needed cleanup.
