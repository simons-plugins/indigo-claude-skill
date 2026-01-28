# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Indigo SDK** - a Python-based framework for creating plugins that integrate 3rd party hardware, applications, and services into the Indigo home automation server. The SDK contains example plugins demonstrating various integration patterns.

**Current API Version**: 3.0+ (Python 3)
**Documentation**: https://www.indigodomo.com/docs/documents#technical_documents
**Developer Forum**: https://forums.indigodomo.com/viewforum.php?f=18

## Plugin Bundle Structure

Indigo plugins are packaged as `.indigoPlugin` bundles with this structure:

```
PluginName.indigoPlugin/
├── Contents/
│   ├── Info.plist                    # Plugin metadata and versioning
│   ├── Server Plugin/
│   │   ├── plugin.py                 # Main plugin class (required)
│   │   ├── Devices.xml               # Device type definitions
│   │   ├── Actions.xml               # Action definitions
│   │   ├── Events.xml                # Event/trigger definitions
│   │   ├── MenuItems.xml             # Plugin menu items
│   │   ├── PluginConfig.xml          # Plugin configuration UI
│   │   └── [additional .py modules]  # Supporting code
│   ├── Resources/                     # Static web content (auto-served)
│   │   ├── templates/                # HTML templates (Jinja2)
│   │   └── static/                   # CSS, JS, images
│   └── Packages/                      # Bundled Python libraries
```

### Critical Files

**Info.plist** ([Example Device - Custom.indigoPlugin/Contents/Info.plist](Example%20Device%20-%20Custom.indigoPlugin/Contents/Info.plist)):
- `CFBundleIdentifier`: **MUST be unique** (e.g., `com.yourcompany.indigoplugin.name`)
- `CFBundleDisplayName`: Display name shown in Indigo UI
- `ServerApiVersion`: Indigo API version (use `"3.6"` or later for Python 3)
- `PluginVersion`: Your plugin version

**plugin.py**: Must contain a `Plugin` class inheriting from `indigo.PluginBase`

## Plugin Architecture

### Core Plugin Class Pattern

All plugins implement `Plugin(indigo.PluginBase)` with these lifecycle methods:

```python
class Plugin(indigo.PluginBase):
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        # Initialize plugin-level attributes

    def startup(self):
        # Called when plugin starts
        # Subscribe to events, initialize resources

    def shutdown(self):
        # Called when plugin stops
        # Clean up resources

    def runConcurrentThread(self):
        # Optional: Runs in separate thread for polling/periodic tasks
        # Must loop forever checking self.stopThread
        try:
            while True:
                # Do periodic work
                self.sleep(interval)
        except self.StopThread:
            pass
```

### Device Types

Plugins can define devices of these types ([Devices.xml](Example%20Device%20-%20Custom.indigoPlugin/Contents/Server%20Plugin/Devices.xml)):

1. **Native types** (inherit states/actions from Indigo):
   - `relay`: ON/OFF/STATUS
   - `dimmer`: ON/OFF/DIM/BRIGHTEN/SET BRIGHTNESS/STATUS
   - `speedcontrol`: ON/OFF/SET SPEED LEVEL/INCREASE/DECREASE/STATUS
   - `sensor`: ON/OFF/STATUS
   - `thermostat`: Full HVAC control
   - `sprinkler`: Zone control

2. **custom**: Define your own states and actions completely

### Device Lifecycle Callbacks

```python
def deviceStartComm(self, dev):
    # Device is starting - initialize hardware connection

def deviceStopComm(self, dev):
    # Device is stopping - clean up connection

def deviceCreated(self, dev):
    # New device created

def deviceUpdated(self, orig_dev, new_dev):
    # Device configuration changed

def deviceDeleted(self, dev):
    # Device deleted
```

### Action Handlers

Actions defined in Actions.xml map to callback methods:

```python
def actionControlDevice(self, action, dev):
    # Handle native device actions (ON/OFF/DIM etc.)
    if action.deviceAction == indigo.kDeviceAction.TurnOn:
        # Handle turn on

def actionControlDimmerRelay(self, action, dev):
    # Handle relay/dimmer specific actions

def actionControlSensor(self, action, dev):
    # Handle sensor actions (usually read-only)

def custom_action_name(self, action, dev):
    # Handle custom actions defined in Actions.xml
```

### State Management

Update device states using:

```python
# Single state update
dev.updateStateOnServer('state_name', value=new_value)

# Multiple states (more efficient)
key_value_list = [
    {'key': 'state1', 'value': value1},
    {'key': 'state2', 'value': value2, 'decimalPlaces': 2},
]
dev.updateStatesOnServer(key_value_list)

# Update state icon
dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
```

### Event Subscription Patterns

**Variable Changes** ([Example Variable Change Subscriber.indigoPlugin/Contents/Server Plugin/plugin.py](Example%20Variable%20Change%20Subscriber.indigoPlugin/Contents/Server%20Plugin/plugin.py)):
```python
def startup(self):
    indigo.variables.subscribeToChanges()

def variableCreated(self, var):
    super().variableCreated(var)  # Always call superclass
    # Handle new variable

def variableUpdated(self, orig_var, new_var):
    super().variableUpdated(orig_var, new_var)
    # Handle variable change

def variableDeleted(self, var):
    super().variableDeleted(var)
    # Handle variable deletion
```

**Device Changes**:
```python
def startup(self):
    indigo.devices.subscribeToChanges()
    # Or subscribe to specific plugin:
    indigo.devices.subscribeToChanges(pluginId="com.some.plugin")
```

### HTTP Responder Pattern

Plugins can respond to HTTP requests ([Example HTTP Responder.indigoPlugin/Contents/Server Plugin/plugin.py](Example%20HTTP%20Responder.indigoPlugin/Contents/Server%20Plugin/plugin.py)):

**URL Format**: `http://localhost:8176/message/{plugin_id}/{method_name}/...`

**Handler Method**:
```python
def api(self, action, dev=None, caller_waiting_for_result=None):
    props_dict = dict(action.props)
    # props_dict["file_path"] - URL path components
    # props_dict["url_query_args"] - Query string args

    reply = indigo.Dict()
    reply["status"] = 200  # HTTP status code
    reply["content"] = "response content"
    reply["headers"] = {"Content-Type": "application/json"}
    return reply
```

**Auto-served Static Content**: Files in `Resources/static/` and `Resources/templates/` are automatically served by Indigo's web server.

### Configuration UI Patterns

**Dynamic Lists** - Lists populated by plugin methods:
```xml
<Field id="deviceMenu" type="menu">
    <List class="self" method="get_device_list" dynamicReload="true"/>
</Field>
```

```python
def get_device_list(self, filter="", values_dict=None, type_id="", target_id=0):
    return [(dev.id, dev.name) for dev in indigo.devices]
```

**Validation**:
```python
def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
    errors_dict = indigo.Dict()
    if some_validation_fails:
        errors_dict["fieldId"] = "Error message"
        return (False, values_dict, errors_dict)
    return (True, values_dict)
```

## Python 3 Migration Notes

Key changes from Python 2 ([Updating to API version 3.0 (Python 3).md](Updating%20to%20API%20version%203.0%20(Python%203).md)):

1. **Print statements**: `print("message")` (not `print "message"`)
2. **Exception handling**: `except Exception as e:` (not `except Exception, e:`)
3. **No unicode type**: All strings are unicode by default
4. **JSON import**: Use `import json` (not `simplejson`)
5. **State image constant**: Use `indigo.kStateImageSel.NoImage` (not `.None`)
6. **Socket operations**: Use `bytes` type, encode/decode strings:
   ```python
   s = "string"
   b = s.encode("utf8")  # str -> bytes for socket
   s = b.decode("utf8")  # bytes -> str from socket
   ```
7. **Dictionary iteration**: `dict.items()` returns views; use `.copy()` if deleting during iteration
8. **Division**: `2/3` returns float; use `2//3` for integer division
9. **File operations**: Use `open()` (not `file()`), specify encoding: `open("file.txt", encoding="utf-8")`

## Development Workflow

### Creating a New Plugin

1. **Copy an example plugin** as starting template
2. **Edit Info.plist**: Change `CFBundleIdentifier` to unique value
3. **Modify plugin.py**: Implement your device/action logic
4. **Define XML files**: Create Devices.xml, Actions.xml, etc.
5. **Install in Indigo**: Copy `.indigoPlugin` to plugins folder or reload via Indigo UI
6. **Test**: Enable/disable plugin, create devices, check logs

### Debugging

- **Enable debug logging**: Set `self.debug = True` in `__init__`
- **Logging methods**:
  ```python
  self.logger.debug("debug message")
  self.logger.info("info message")
  self.logger.warning("warning message")
  self.logger.error("error message")
  self.logger.exception(exc)  # Logs exception with traceback
  ```
- **View logs**: Indigo Event Log window shows all plugin output
- **Breakpoints**: Can't use traditional debuggers; rely on logging

### Package Management

- **Bundled libraries**: Place 3rd party packages in `Contents/Packages/` directory
- **System packages**: Install to Indigo's Python environment (usually not recommended)
- **Import order**: Packages folder takes precedence over system packages

### Reloading During Development

- Indigo must reload the plugin for code changes to take effect
- Use "Reload Plugin" from Plugins menu in Indigo
- Or disable/re-enable the plugin
- Changes to XML files require plugin reload
- Changes to Resources/ files may require clearing browser cache

## Example Plugins Guide

Each example demonstrates specific patterns:

- **Example Device - Custom**: Custom states, dynamic UI, scene management
- **Example Device - Relay and Dimmer**: Overriding native device types
- **Example Device - Thermostat**: HVAC control implementation
- **Example Device - Energy Meter**: Accumulating energy usage tracking
- **Example Device - Sensor**: Read-only sensor device pattern
- **Example Device - Sprinkler**: Zone scheduling and control
- **Example HTTP Responder**: Web API, Jinja2 templates, static content serving
- **Example Action API**: Complex action configurations, YAML processing
- **Example Database Traverse**: Iterating through Indigo's device/variable database
- **Example Custom Broadcaster**: Publishing custom broadcasts to other plugins
- **Example Custom Subscriber**: Receiving broadcasts from other plugins
- **Example Variable Change Subscriber**: Monitoring variable changes
- **Example INSTEON/X10 Listener**: Hardware protocol event monitoring
- **Example ZWave Listener**: Z-Wave protocol event monitoring

## Common Patterns

### Polling Hardware

```python
def runConcurrentThread(self):
    try:
        while True:
            for dev in indigo.devices.iter("self"):
                if dev.enabled:
                    self.update_device_from_hardware(dev)
            self.sleep(polling_interval)
    except self.StopThread:
        pass
```

### Error Handling

```python
try:
    # Hardware communication
    result = hardware.send_command()
    dev.updateStateOnServer('status', value='success')
except Exception as exc:
    self.logger.exception(exc)
    dev.updateStateOnServer('status', value='error')
    dev.updateStateImageOnServer(indigo.kStateImageSel.Error)
```

### Plugin Preferences

```python
# Access in plugin code:
api_key = self.pluginPrefs.get('apiKey', 'default_value')

# Validate in:
def validatePrefsConfigUi(self, values_dict):
    errors_dict = indigo.Dict()
    if not values_dict.get('apiKey'):
        errors_dict['apiKey'] = "API key is required"
        return (False, values_dict, errors_dict)
    return (True, values_dict)
```

### Thread Safety

- `self.sleep()` instead of `time.sleep()` - allows clean plugin shutdown
- Device state updates are thread-safe
- Use locks if sharing mutable data between threads

## Indigo Object Model

Access Indigo's database through these collections:

```python
indigo.devices[id]           # Device by ID
indigo.devices["name"]       # Device by name
indigo.devices.iter("self")  # Iterate devices from this plugin

indigo.variables[id]         # Variable by ID
indigo.variables["name"]     # Variable by name

indigo.triggers[id]          # Trigger by ID
indigo.schedules[id]         # Schedule by ID
indigo.actionGroups[id]      # Action group by ID
```

All return `indigo.Dict` objects with dot notation access: `dev.states["temp"]` or `dev.states.temp`
