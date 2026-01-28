# Indigo Object Model (IOM) Reference

**Official Documentation**: https://www.indigodomo.com/docs/object_model_reference

## Overview

The Indigo Object Model provides Python access to all Indigo objects (devices, variables, triggers, actions, etc.). All objects are accessed through the `indigo` module which is automatically imported when your plugin runs.

## Core Collections

### Devices

```python
# Access by ID
dev = indigo.devices[123456]

# Access by name
dev = indigo.devices["Living Room Lamp"]

# Check existence
if "Living Room Lamp" in indigo.devices:
    dev = indigo.devices["Living Room Lamp"]

# Iterate all devices
for dev in indigo.devices:
    print(dev.name)

# Iterate only this plugin's devices
for dev in indigo.devices.iter("self"):
    print(dev.name)

# Iterate devices by plugin ID
for dev in indigo.devices.iter(pluginId="com.example.plugin"):
    print(dev.name)

# Iterate by filter
for dev in indigo.devices.iter(filter="indigo.dimmer"):
    print(f"Dimmer: {dev.name}, brightness: {dev.brightness}")
```

### Variables

```python
# Access by ID
var = indigo.variables[123456]

# Access by name
var = indigo.variables["MyVariable"]

# Get/set value
value = var.value
var.value = "new value"  # Updates in Indigo

# Create variable
new_var = indigo.variable.create("MyNewVariable", value="initial")

# Update via ID
indigo.variable.updateValue(var_id, "new value")

# Iterate all variables
for var in indigo.variables:
    print(f"{var.name} = {var.value}")
```

### Triggers

```python
# Access trigger
trigger = indigo.triggers[trigger_id]

# Check if enabled
if trigger.enabled:
    print("Trigger is active")

# Iterate triggers
for trigger in indigo.triggers:
    if trigger.pluginId == "self":
        print(f"My trigger: {trigger.name}")
```

### Action Groups

```python
# Access action group
ag = indigo.actionGroups[ag_id]

# Execute action group
indigo.actionGroup.execute(ag_id)

# Iterate
for ag in indigo.actionGroups:
    print(ag.name)
```

### Schedules

```python
# Access schedule
sched = indigo.schedules[sched_id]

# Check if enabled
if sched.enabled:
    print("Schedule active")
```

## Device Object

**Reference**: https://www.indigodomo.com/docs/object_model_reference#device

### Common Properties

```python
dev.id                  # Unique device ID (int)
dev.name                # Device name (str)
dev.deviceTypeId        # Type from Devices.xml (str)
dev.pluginId            # Plugin bundle ID (str)
dev.enabled             # Is enabled? (bool)
dev.configured          # Is configured? (bool)
dev.description         # Description text (str)
dev.model               # Model name (str)
dev.protocol            # Protocol type (indigo.kProtocol)
dev.address             # Device address (str)
dev.version             # Firmware version (str)
dev.subModel            # Sub-model identifier (str)

# Plugin properties
dev.pluginProps         # indigo.Dict of ConfigUI values
dev.ownerProps          # Read-only plugin properties

# States
dev.states              # indigo.Dict of all states
dev.states['stateName'] # Access specific state
dev.displayStateId      # ID of primary display state
dev.displayStateValue   # Value of primary display state
dev.displayStateImageSel # Current state icon

# Remote display
dev.remoteDisplay       # Text shown on remote control
```

### Device Type Specific Properties

#### Relays/Dimmers
```python
dev.onState             # Is device on? (bool)
dev.brightness          # Brightness 0-100 (int) - dimmers only
```

#### Sensors
```python
dev.onState             # Sensor tripped state
dev.onOffState          # ON or OFF
dev.sensorValue         # Numeric sensor value
```

#### Thermostats
```python
dev.heatSetpoint        # Heat setpoint
dev.coolSetpoint        # Cool setpoint
dev.hvacMode            # Current mode
dev.fanMode             # Fan mode
dev.temperatureInput1   # Current temperature
```

### Device Methods

```python
# Update states
dev.updateStateOnServer('stateName', value=new_value)
dev.updateStatesOnServer(key_value_list)

# Update icon
dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)

# Set error state
dev.setErrorStateOnServer("Error message")
dev.setErrorStateOnServer(None)  # Clear error

# Refresh state list (call if Devices.xml changed)
dev.stateListOrDisplayStateIdChanged()

# Get as dict
dev_dict = dict(dev)
```

## Variable Object

**Reference**: https://www.indigodomo.com/docs/object_model_reference#variable

```python
var.id              # Unique variable ID
var.name            # Variable name
var.value           # Current value (str)
var.readOnly        # Is read-only? (bool)

# Modify variable
var.value = "new value"
indigo.variable.updateValue(var.id, "new value")

# Create variable
new_var = indigo.variable.create("VarName", value="initial", folder=folder_id)

# Folder
var.folderId        # Parent folder ID
var.displayInRemoteUI  # Show in remote UI?
```

## Server Object

```python
# Get server time
server_time = indigo.server.getTime()

# Get API version
api_version = indigo.server.apiVersion  # e.g., "3.6"

# Get Indigo version
indigo_version = indigo.server.version  # e.g., "2023.2.0"

# Log to Event Log
indigo.server.log("message")
indigo.server.error("error message")

# Speak text
indigo.server.speak("Hello world")
```

## Trigger Object

```python
trigger.id              # Trigger ID
trigger.name            # Trigger name
trigger.enabled         # Is enabled?
trigger.pluginId        # Plugin ID if plugin trigger
trigger.pluginTypeId    # Event type ID
```

## Action Group Object

```python
ag.id                   # Action group ID
ag.name                 # Action group name
ag.enabled              # Is enabled?

# Execute
indigo.actionGroup.execute(ag.id)
```

## Constants

### State Icons

```python
indigo.kStateImageSel.Auto
indigo.kStateImageSel.AvPaused
indigo.kStateImageSel.AvPlaying
indigo.kStateImageSel.AvStopped
indigo.kStateImageSel.DimmerOff
indigo.kStateImageSel.DimmerOn
indigo.kStateImageSel.Error
indigo.kStateImageSel.FanHigh
indigo.kStateImageSel.FanLow
indigo.kStateImageSel.FanMedium
indigo.kStateImageSel.FanOff
indigo.kStateImageSel.HvacAutoMode
indigo.kStateImageSel.HvacCoolMode
indigo.kStateImageSel.HvacFanMode
indigo.kStateImageSel.HvacHeatMode
indigo.kStateImageSel.HvacOff
indigo.kStateImageSel.LightSensor
indigo.kStateImageSel.LightSensorOn
indigo.kStateImageSel.Locked
indigo.kStateImageSel.MotionSensor
indigo.kStateImageSel.MotionSensorTripped
indigo.kStateImageSel.NoImage
indigo.kStateImageSel.PowerOff
indigo.kStateImageSel.PowerOn
indigo.kStateImageSel.SensorOff
indigo.kStateImageSel.SensorOn
indigo.kStateImageSel.SensorTripped
indigo.kStateImageSel.SprinklerOff
indigo.kStateImageSel.SprinklerOn
indigo.kStateImageSel.TimerOff
indigo.kStateImageSel.TimerOn
indigo.kStateImageSel.Unlocked
```

### Device Actions

```python
# Relay/Dimmer
indigo.kDeviceAction.TurnOn
indigo.kDeviceAction.TurnOff
indigo.kDeviceAction.Toggle
indigo.kDeviceAction.SetBrightness
indigo.kDeviceAction.BrightenBy
indigo.kDeviceAction.DimBy
indigo.kDeviceAction.RequestStatus

# Thermostat
indigo.kThermostatAction.SetHeatSetpoint
indigo.kThermostatAction.SetCoolSetpoint
indigo.kThermostatAction.SetHvacMode
indigo.kThermostatAction.SetFanMode

# Sensor
indigo.kSensorAction.TurnOn
indigo.kSensorAction.TurnOff

# Sprinkler
indigo.kSprinklerAction.ZoneOn
indigo.kSprinklerAction.ZoneOff
indigo.kSprinklerAction.AllZonesOff
```

### Protocols

```python
indigo.kProtocol.Plugin
indigo.kProtocol.Insteon
indigo.kProtocol.X10
indigo.kProtocol.ZWave
```

## indigo.Dict

Special dictionary class used throughout Indigo:

```python
# Create
d = indigo.Dict()

# Access with dot notation or brackets
d.key = "value"
d['key'] = "value"
value = d.key
value = d['key']

# Get with default
value = d.get('key', 'default')

# Check existence
if 'key' in d:
    pass

# Convert to regular dict
regular_dict = dict(d)
```

## Subscriptions

Subscribe to object changes:

```python
# Variables
indigo.variables.subscribeToChanges()

# Devices
indigo.devices.subscribeToChanges()
indigo.devices.subscribeToChanges(pluginId="com.example.plugin")

# Implement callbacks
def variableUpdated(self, orig_var, new_var):
    super().variableUpdated(orig_var, new_var)
    # Handle change

def deviceUpdated(self, orig_dev, new_dev):
    super().deviceUpdated(orig_dev, new_dev)
    # Handle change
```

## JSON Encoding

Use Indigo's JSON encoder for proper date handling:

```python
import json

# Serialize device with proper date encoding
json_str = json.dumps(dict(dev), indent=4, cls=indigo.utils.JSONDateEncoder)
```

## Official References

- [Complete Object Model Reference](https://www.indigodomo.com/docs/object_model_reference)
- [Device Object](https://www.indigodomo.com/docs/object_model_reference#device)
- [Variable Object](https://www.indigodomo.com/docs/object_model_reference#variable)
- [Server Object](https://www.indigodomo.com/docs/object_model_reference#server)
- [Constants Reference](https://www.indigodomo.com/docs/object_model_reference#constants)
