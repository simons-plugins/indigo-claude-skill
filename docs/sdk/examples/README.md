# SDK Example Plugins Guide

This guide explains what each example plugin in the SDK demonstrates and when to use it as a reference.

## Quick Reference

| Example | Use When You Need | Key Features |
|---------|-------------------|--------------|
| [Device - Custom](#example-device---custom) | Custom device types with unique states | State management, dynamic UI, scene devices |
| [Device - Relay and Dimmer](#example-device---relay-and-dimmer) | Control switches or lights | Overriding native types, dimmer control |
| [Device - Thermostat](#example-device---thermostat) | Climate control | HVAC modes, temperature control |
| [Device - Sensor](#example-device---sensor) | Read-only sensors | Sensor patterns, state updates |
| [Device - Energy Meter](#example-device---energy-meter) | Track accumulating values | Energy tracking, accumulation |
| [Device - Sprinkler](#example-device---sprinkler) | Zone-based control | Multi-zone scheduling |
| [Device - Speed Control](#example-device---speed-control) | Variable speed devices | Fan control, speed levels |
| [HTTP Responder](#example-http-responder) | Web API or web interface | HTTP handlers, Jinja2 templates, JSON/XML |
| [Action API](#example-action-api) | Complex plugin actions | Action configuration, YAML processing |
| [Database Traverse](#example-database-traverse) | Inspect Indigo database | Iterating devices/variables |
| [Custom Broadcaster](#example-custom-broadcaster) | Send events to other plugins | Inter-plugin communication |
| [Custom Subscriber](#example-custom-subscriber) | Receive events from other plugins | Event listening |
| [Variable Change Subscriber](#example-variable-change-subscriber) | Monitor variable changes | Variable subscriptions |
| [INSTEON/X10 Listener](#example-insteonx10-listener) | Monitor INSTEON/X10 traffic | Protocol monitoring |
| [ZWave Listener](#example-zwave-listener) | Monitor Z-Wave traffic | Protocol monitoring |

## Detailed Examples

### Example Device - Custom

**Path**: `../IndigoSDK-2025.1/Example Device - Custom.indigoPlugin`

**What It Demonstrates**:
- Custom device type with user-defined states
- Dynamic state updates in `runConcurrentThread()`
- Complex configuration UI with dynamic lists
- Scene device pattern (managing multiple devices)
- Button callbacks in device config

**Use This When**:
- Creating a device that doesn't fit standard types (relay, dimmer, etc.)
- Need custom states like temperature, status, counters
- Building composite devices that manage other devices
- Implementing dynamic configuration UIs

**Key Code Sections**:
- `serverTimeDevice` - Simple custom device with periodic state updates
- `stateUpdater` - Demonstrates different state value types
- `sceneExample` - Managing list of member devices
- `add_device()`, `delete_devices()` - UI button callbacks
- `source_devices()`, `member_devices()` - Dynamic list builders

**States Pattern**:
```xml
<States>
    <State id="serverTimeSeconds">
        <ValueType>Integer</ValueType>
        <TriggerLabel>Current Server Seconds</TriggerLabel>
        <ControlPageLabel>Current Server Seconds</ControlPageLabel>
    </State>
</States>
```

### Example Device - Relay and Dimmer

**Path**: `../IndigoSDK-2025.1/Example Device - Relay and Dimmer.indigoPlugin`

**What It Demonstrates**:
- Overriding native relay and dimmer device types
- Implementing standard ON/OFF/DIM actions
- Simulating hardware communication
- Status request handling

**Use This When**:
- Integrating with relay or dimmer hardware
- Need standard light switch behavior
- Want Indigo's native actions to work

**Key Methods**:
- `actionControlDimmerRelay()` - Handle ON/OFF/DIM commands
- `actionControlDevice()` - Handle generic device actions

### Example Device - Thermostat

**Path**: `../IndigoSDK-2025.1/Example Device - Thermostat.indigoPlugin`

**What It Demonstrates**:
- Full thermostat implementation
- HVAC mode control (Heat/Cool/Auto/Off)
- Fan mode control
- Temperature setpoint management
- Status updates

**Use This When**:
- Integrating smart thermostats
- Building climate control systems
- Need HVAC control

**Key Methods**:
- `actionControlThermostat()` - Handle thermostat actions
- Setpoint validation and range checking

### Example Device - Sensor

**Path**: `../IndigoSDK-2025.1/Example Device - Sensor.indigoPlugin`

**What It Demonstrates**:
- Read-only sensor device pattern
- ON/OFF sensor states
- Tripped state management
- Rejecting write actions (sensors are read-only)

**Use This When**:
- Motion sensors, door/window sensors
- Any read-only monitoring device
- Environmental sensors

**Key Pattern**:
```python
def actionControlSensor(self, action, dev):
    # Reject actions - sensors are read-only
    self.logger.info(f"ignored \"{dev.name}\" {action} (sensor is read-only)")
```

### Example Device - Energy Meter

**Path**: `../IndigoSDK-2025.1/Example Device - Energy Meter.indigoPlugin`

**What It Demonstrates**:
- Accumulating energy usage tracking
- Energy meter device type
- Power consumption monitoring
- Reset and update operations

**Use This When**:
- Tracking electricity usage
- Power monitoring devices
- Accumulating usage over time

### Example HTTP Responder

**Path**: `../IndigoSDK-2025.1/Example HTTP Responder.indigoPlugin`

**What It Demonstrates**:
- HTTP request handling
- RESTful API implementation
- JSON and XML responses
- Jinja2 template rendering
- Static file serving
- Custom 404 pages
- Query string parameter handling

**Use This When**:
- Building web API for your plugin
- Creating web-based control interfaces
- Returning device data as JSON/XML
- Serving web dashboards

**URL Pattern**:
```
http://localhost:8176/message/{bundle_id}/{method_name}/path...?args
```

**Handler Pattern**:
```python
def api(self, action, dev=None, caller_waiting_for_result=None):
    props_dict = dict(action.props)
    file_path = props_dict["file_path"]  # URL path components
    query_args = props_dict.get("url_query_args", {})  # Query params

    reply = indigo.Dict()
    reply["status"] = 200
    reply["content"] = json.dumps(data)
    reply["headers"] = {"Content-Type": "application/json"}
    return reply
```

**Auto-Served Content**:
- `Resources/static/` - CSS, JavaScript, images
- `Resources/templates/` - Jinja2 HTML templates

### Example Action API

**Path**: `../IndigoSDK-2025.1/Example Action API.indigoPlugin`

**What It Demonstrates**:
- Complex action configuration UIs
- YAML file processing
- XML to dict conversion
- Multiple action examples
- Dynamic action parameters

**Use This When**:
- Creating plugin actions with rich configuration
- Processing YAML or XML data
- Actions need user input parameters

### Example Database Traverse

**Path**: `../IndigoSDK-2025.1/Example Database Traverse.indigoPlugin`

**What It Demonstrates**:
- Iterating all devices in Indigo
- Iterating all variables
- Filtering by device type
- Inspecting object properties

**Use This When**:
- Need to scan entire Indigo database
- Building device/variable selection lists
- Auditing or reporting on Indigo configuration

**Pattern**:
```python
# All devices
for dev in indigo.devices:
    self.logger.info(f"Device: {dev.name}")

# Only dimmers
for dev in indigo.devices.iter(filter="indigo.dimmer"):
    self.logger.info(f"Dimmer: {dev.name}, brightness: {dev.brightness}")

# Only this plugin's devices
for dev in indigo.devices.iter("self"):
    self.logger.info(f"My device: {dev.name}")
```

### Example Custom Broadcaster

**Path**: `../IndigoSDK-2025.1/Example Custom Broadcaster.indigoPlugin`

**What It Demonstrates**:
- Broadcasting custom events to other plugins
- Inter-plugin communication
- Event payload structure

**Use This When**:
- Your plugin needs to notify other plugins of events
- Building plugin ecosystems
- Creating extensible plugin architecture

**Broadcast Pattern**:
```python
indigo.activePlugin.broadcast(
    msgType="customMessage",
    msgDict={"key": "value"}
)
```

### Example Custom Subscriber

**Path**: `../IndigoSDK-2025.1/Example Custom Subscriber.indigoPlugin`

**What It Demonstrates**:
- Receiving broadcasts from other plugins
- Filtering broadcast messages
- Processing broadcast payloads

**Use This When**:
- Your plugin needs to react to other plugins' events
- Building plugin integrations

**Subscribe Pattern**:
```python
def customBroadcastReceived(self, msg_dict):
    # Handle broadcast from another plugin
    msg_type = msg_dict.get("msgType", "")
    if msg_type == "customMessage":
        # Process message
        pass
```

### Example Variable Change Subscriber

**Path**: `../IndigoSDK-2025.1/Example Variable Change Subscriber.indigoPlugin`

**What It Demonstrates**:
- Subscribing to all variable changes
- Detecting variable creation
- Detecting variable updates
- Detecting variable deletion

**Use This When**:
- Plugin behavior depends on Indigo variables
- Need to react to variable changes
- Synchronizing with variable state

**Pattern**:
```python
def startup(self):
    indigo.variables.subscribeToChanges()

def variableCreated(self, var):
    super().variableCreated(var)
    # React to new variable

def variableUpdated(self, orig_var, new_var):
    super().variableUpdated(orig_var, new_var)
    # React to variable change

def variableDeleted(self, var):
    super().variableDeleted(var)
    # React to variable deletion
```

### Example INSTEON/X10 Listener

**Path**: `../IndigoSDK-2025.1/Example INSTEON:X10 Listener.indigoPlugin`

**What It Demonstrates**:
- Monitoring INSTEON protocol traffic
- Monitoring X10 protocol traffic
- Decoding raw protocol messages

**Use This When**:
- Building INSTEON device support
- Need to react to INSTEON/X10 commands
- Debugging INSTEON communication

### Example ZWave Listener

**Path**: `../IndigoSDK-2025.1/Example ZWave Listener.indigoPlugin`

**What It Demonstrates**:
- Monitoring Z-Wave protocol traffic
- Decoding Z-Wave messages
- Reacting to Z-Wave events

**Use This When**:
- Building Z-Wave device support
- Need to react to Z-Wave commands
- Debugging Z-Wave communication

## How to Use These Examples

1. **Browse the Code**: Right-click plugin bundle → Show Package Contents
2. **Copy as Template**: Duplicate entire plugin folder as starting point
3. **Modify Info.plist**: Change bundle ID and display name
4. **Adapt Code**: Replace example logic with your hardware/service integration
5. **Test**: Enable in Indigo and verify functionality

## Common Patterns Across Examples

### Plugin Structure
All examples follow same structure:
```
PluginName.indigoPlugin/
├── Contents/
│   ├── Info.plist
│   ├── Server Plugin/
│   │   ├── plugin.py
│   │   ├── Devices.xml
│   │   ├── Actions.xml
│   │   └── MenuItems.xml
```

### Plugin Class
All inherit from `indigo.PluginBase`:
```python
class Plugin(indigo.PluginBase):
    def __init__(self, ...):
        super().__init__(...)

    def startup(self):
        pass

    def shutdown(self):
        pass
```

### Error Handling
Consistent logging pattern:
```python
try:
    risky_operation()
except Exception as e:
    self.logger.exception(e)
```

## Finding the Right Example

**Start with**:
1. What type of device? → Choose device example
2. Need web interface? → HTTP Responder
3. React to changes? → Subscriber examples
4. Need actions? → Action API
5. Inspect database? → Database Traverse

**Most Common Starting Points**:
- Generic integration: **Device - Custom**
- Lights/switches: **Device - Relay and Dimmer**
- Sensors: **Device - Sensor**
- Web API: **HTTP Responder**

## Next Steps

After reviewing examples:
1. Copy relevant example as starting point
2. Review [../plugin-development/](../plugin-development/) documentation
3. Consult [../api-reference/](../api-reference/) for API details
4. Post questions on [Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)
