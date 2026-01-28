#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2024, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

from datetime import datetime
import json
import jinja2
import dicttoxml
import mimetypes

NO_FILE_SPECIFIED = "No File Specified"

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs)
        self.debug: bool = True
        # Set up the environment for Jinja templates. The most important thing to configure is the file system loader
        # so that it points to our Resources/templates directory. Then we can just load the template via name (or name
        # and relative path within that folder if we choose).
        self.templates = jinja2.Environment(
            loader=jinja2.FileSystemLoader("../Resources/templates"),
            autoescape=True,
            auto_reload=self.debug, # this makes the templates load from disk every time you use them - good for debugging
        )
        # Next, we add some global variables that will be available to all templates automatically.
        self.templates.globals = {
            "plugin": self, # used primarily here to construct paths to the static/css directory
            "year_string": datetime.now().strftime("%Y"), # used for the copyright
        }

    ########################################
    def startup(self):
        self.logger.debug("startup called")

    def shutdown(self):
        self.logger.debug("shutdown called")

    ########################################
    def api(self, action, dev=None, caller_waiting_for_result=None):
        '''
        This handler is used to generate a simple api that returns device details for the specified device id.
        Example url:

            http://localhost:8176/message/com.indigodomo.indigoplugin.example-http-responder/api/123456.json
            http://localhost:8176/message/com.indigodomo.indigoplugin.example-http-responder/api/123456.json?condense-json=true

        The first part is the ID of a device and the extension as the type of content to return. We only do XML and JSON
        in this example. There is an optional arg to return JSON that doesn't have indents, which means it would be
        smaller. condense-json can be any value at all and it will skip the formatting with indents.

        :param action: action.props contains all the information passed from the web server
        :param dev: unused
        :param caller_waiting_for_result: always True
        :return: a reply dict with the content value being JSON or XML representation of a device instance.
        '''
        self.logger.debug("Handling API request")
        props_dict = dict(action.props)
        file_path = list(props_dict["file_path"])
        reply = indigo.Dict()
        try:
            file_name = file_path[-1]
            id_string, frmt = file_name.split(".")
            dev_id = int(id_string)
            frmt = frmt.lower()
        except:
            self.logger.error("no file was specified in the request or the file name was incorrect")
            reply["content"] = "no file was specified in the request or the file name was incorrect"
            reply["status"] = 500
            return reply
        try:
            device = indigo.devices[dev_id]
            self.logger.debug(f"...for device {device.name}")
            reply["status"] = 200
            if frmt == "xml":
                reply["content"] = dicttoxml.dicttoxml(dict(device), custom_root="Device")
            elif frmt == "json":
                try:
                    condense = props_dict.get("url_query_args", {}).get("condense-json", False)
                    if condense:
                        reply["content"] = json.dumps(dict(device), separators=(',', ':'), cls=indigo.utils.JSONDateEncoder)
                    else:
                        reply["content"] = json.dumps(dict(device), indent=4, cls=indigo.utils.JSONDateEncoder)
                except Exception as exc:
                    self.logger.exception(exc)
            else:
                self.logger.error("specified format isn't supported")
                reply["content"] = "specified format isn't supported"
                reply["status"] = 500
                return reply
            reply["headers"] = {"Content-Type": f"application/{frmt}"}
            return reply
        except KeyError:
            self.logger.error("device id doesn't exist in database")
            # Here, we illustrate how to return a custom dynamic 404 page
            template = self.templates.get_template("device_missing.html")
            reply["status"] = 404
            reply["headers"] = indigo.Dict({"Content-Type": "text/html"})
            reply["content"] = template.render({"device_id": dev_id})
            return reply

    ########################################
    def handle_static_file_request(self, action, dev=None, caller_waiting_for_result=None):
        '''
        This handler just opens the file specified in the query string's "file-name" argument on the URL and returns
        the content. We just assume here it's some kind of text file. We'll look for the file in the Resources folder
        in this plugin. If it's not there, we'll return a 401.

        ** IMPORTANT **
        This example is here to illustrate one way to return a file from a plugin without putting it into one of the
        directories that are automatically served within the Resources folder (see the README.txt file in the Server
        Plugin folder for details on how the Indigo Web Server can automatically serve up content from your plugin.)

            http://localhost:8176/message/com.indigodomo.indigoplugin.example-http-responder/handle_static_file_request/?file-name=test.csv

        :param action: action.props contains all the information passed from the web server
        :param dev: unused
        :param caller_waiting_for_result: always True
        :return: a dict that contains the status, the Content-Type header, and the contents of the specified file.
        '''
        self.logger.debug("Handling HTTP request")
        props_dict = dict(action.props)
        reply = indigo.Dict()
        #######################
        # reply["content"] = "a 200 return from the plugin"
        # reply["status"] = 200
        # return reply
        #######################
        try:
            file_name = props_dict["url_query_args"]["file-name"]
            file_path = f"../Resources/{file_name}"
            self.logger.debug(f"...looking for file: {file_path}")
        except:
            # file name wasn't specified, set a flag
            file_name = ""
            file_path = NO_FILE_SPECIFIED
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                file_contents = file.read()
            content_type = mimetypes.guess_type(file_name)[0] or "text/plain"
            reply["status"] = 200
            reply["headers"] = indigo.Dict({ "Content-Type":f"{content_type}" })
            reply["content"] = file_contents
        except:
            # file wasn't found
            if file_path == NO_FILE_SPECIFIED:
                self.logger.error("no file was specified in the request query arguments")
                reply["content"] = "no file was specified in the request query arguments"
                reply["status"] = 400
            else:
                # Here, we illustrate how to return a custom static 404 HTML page
                file_name = props_dict["url_query_args"]["file-name"]
                self.logger.error(f"requested file was not found: {file_name}")
                return indigo.utils.return_static_file(
                    f"{self.pluginFolderPath}/Contents/Resources/static/html/static_404.html",
                    status=404,
                    path_is_relative=False,
                )
        return reply

    ########################################
    def sample_config(self, action, dev=None, caller_waiting_for_result=None):
        '''
        This handler represents a simple plugin configuration example. It will have the following URLs:

            http://localhost:8176/message/com.indigodomo.indigoplugin.example-http-responder/config

        It uses the config.html Jinja template in the templates directory. That template extends the base.html template
        file, which includes the static/css/config.css file using the built-in static file serving process for plugins.

        :param action: action.props contains all the information passed from the web server
        :param dev: unused
        :param caller_waiting_for_result: always True
        :return: a dict that contains the status, the Content-Type header, and the contents of the specified file.
        '''
        self.logger.debug("Handling config request")
        props_dict = dict(action.props)
        reply = indigo.Dict()
        context = {
            "date_string": str(datetime.now()),  # Used in the config.html template
            "prefs": self.pluginPrefs,
        }
        if props_dict.get('incoming_request_method', "GET") == "POST":
            post_params = dict(props_dict["body_params"])
            if "operation" in post_params:
                if post_params["operation"] == "add":
                    key = post_params.get("key", None)
                    val = post_params.get("value", None)
                    if not key or not val:
                        context["error"] = "the key and value must not be empty to add them to the plugin config"
                    else:
                        self.pluginPrefs[key] = val
                else:
                    context["error"] = "'add' is the only valid operation for this form"
            else:
                for key, val in post_params.items():
                    if val == "delete":
                        try:
                            del self.pluginPrefs[key]
                        except:
                            # probably a stale browser trying to delete a key that's already gone, just ignore it
                            pass
            indigo.server.savePluginPrefs()
        try:
            template = self.templates.get_template("config.html")
            reply["status"] = 200
            reply["headers"] = indigo.Dict({"Content-Type": "text/html"})
            reply["content"] = template.render(context)
        except Exception as exc:
            # some error happened
            self.logger.error(f"some error occurred: {exc}")
            reply["status"] = 500
        return reply

    ########################################
    def do_nothing(self, values_dict, type_id):
        pass
