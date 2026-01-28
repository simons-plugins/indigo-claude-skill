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

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process. However, to avoid lots of error
# highlighting by many IDEs we added the import above which usually fixes it.

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug: bool = True

    ########################################
    def startup(self):
        self.logger.debug("startup called -- subscribing to variable changes")
        # Subscribe to all variable changes
        indigo.variables.subscribeToChanges()

    def shutdown(self):
        self.logger.debug("shutdown called")

    ########################################
    def variableCreated(self, var):
        '''
        This method is called whenever a new variable is created.

        :param self: Your plugin instance
        :param var: The variable that has been created
        :return: No return value required
        '''
        # You must call the superclass method
        super().variableCreated(var)
        self.logger.debug(f"variableCreated called for variable '{var.name}': value: {var.value}")
        # Do your stuff

    def variableUpdated(self, orig_var, new_var):
        '''
        This method is called every time a variable is changed in any way (name, value, etc). Your
        plugin will likely need to inspect the variable to see if it's one you're interested in. You
        can compare the previous value to the new value if you need to.

        :param self: Your plugin instance
        :param orig_var: An instance of the indigo.Variable object as it was before the change
        :param new_var: An instance of the indigo.Variable object as it is currently (after the change)
        :return: No return value required
        '''
        # You must call the superclass method
        super().variableUpdated(orig_var, new_var)
        self.logger.debug("variableUpdated called")
        self.logger.debug(f"old name: {orig_var.name}, old value: {orig_var.value}")
        self.logger.debug(f"new name: {new_var.name}, new value: {new_var.value}")
        # Do your stuff

    def variableDeleted(self, var):
        '''
        This method is called every time a variable is deleted. Since your plugin
        will likely depend on only specific variables, you'll want to make sure that
        you take the appropriate action when a variable that it depends on is deleted.

        :param self: Your plugin instance
        :param var: An instance of the indigo.Variable object that has been deleted
        :return: No return value required
        '''
        # You must call the superclass method
        super().variableDeleted(var)
        self.logger.debug(f"variableDeleted called for variable '{var.name}': value: {var.value}")
        # Do your stuff
