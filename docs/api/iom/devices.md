# Device Classes Reference

## Device Class Hierarchy

```
indigo.Device (base)
├── indigo.DimmerDevice
├── indigo.RelayDevice
├── indigo.SensorDevice
├── indigo.ThermostatDevice
├── indigo.SprinklerDevice
├── indigo.SpeedControlDevice
└── indigo.MultiIODevice
```

## Common Device Properties

All device types share these properties:

```python
dev.id                  # Unique ID (int)
dev.name                # Device name (str)
dev.enabled             # Is enabled (bool)
dev.configured          # Is configured (bool)
dev.description         # Description (str)
dev.model               # Model name (str)
dev.address             # Device address (str)
dev.version             # Firmware version (str)
dev.subModel            # Sub-model identifier (str)
dev.protocol            # Protocol (indigo.kProtocol.*)
dev.deviceTypeId        # Plugin device type ID (str)
dev.pluginId            # Plugin bundle ID (str)
dev.folderId            # Parent folder ID (int)
dev.lastChanged         # Last state change (datetime)
dev.batteryLevel        # Battery level if applicable (int or None)
dev.buttonGroupCount    # Number of button groups (int)

# Plugin properties
dev.pluginProps         # indigo.Dict of user config
dev.globalProps         # indigo.Dict of global properties
dev.ownerProps          # Read-only plugin properties

# States
dev.states              # indigo.Dict of all states
dev.displayStateId      # Primary display state ID
dev.displayStateValue   # Primary display state value
dev.displayStateImageSel # Current state icon

# Remote UI
dev.remoteDisplay       # Text for remote display

# Capabilities
dev.supportsStatusRequest    # Can request status
dev.supportsAllOff           # Supports all-off
dev.supportsAllLightsOnOff   # Supports all-lights commands
```

## DimmerDevice

Dimmable lighting devices.

```python
dev.onState             # Is on (bool)
dev.brightness          # Brightness 0-100 (int)
dev.supportsRGB         # Supports color (bool)
dev.supportsWhite       # Supports white level (bool)
dev.supportsWhiteTemperature  # Supports color temp (bool)
```

### Color Properties (if supported)

```python
dev.redLevel            # Red 0-100
dev.greenLevel          # Green 0-100
dev.blueLevel           # Blue 0-100
dev.whiteLevel          # White 0-100
dev.whiteTemperature    # Color temp in Kelvin
```

## RelayDevice

On/off devices (switches, locks, outlets).

```python
dev.onState             # Is on (bool)
```

## SensorDevice

Sensors (motion, door/window, temperature).

```python
dev.onState             # Sensor triggered state (bool)
dev.sensorValue         # Numeric sensor value (float)

# For binary sensors
dev.onOffState          # "on" or "off" string
```

## ThermostatDevice

HVAC thermostats.

```python
dev.hvacMode            # Current mode (indigo.kHvacMode.*)
dev.fanMode             # Fan mode (indigo.kFanMode.*)
dev.coolSetpoint        # Cooling setpoint (float)
dev.heatSetpoint        # Heating setpoint (float)
dev.coolIsOn            # Cooling active (bool)
dev.heatIsOn            # Heating active (bool)
dev.fanIsOn             # Fan active (bool)

# Temperature sensors
dev.temperatureSensorCount  # Number of sensors
dev.temperatures        # List of temperatures

# Humidity sensors
dev.humiditySensorCount # Number of humidity sensors
dev.humidities          # List of humidity values
```

## SprinklerDevice

Irrigation controllers.

```python
dev.zoneCount           # Number of zones
dev.activeZone          # Currently active zone (0 = none)
dev.zoneNames           # List of zone names
dev.zoneEnableList      # List of enabled zones
dev.zoneDurations       # List of zone durations
dev.zoneScheduledDurations  # Scheduled durations
```

## SpeedControlDevice

Variable speed devices (fans, motors).

```python
dev.onState             # Is on (bool)
dev.speedLevel          # Speed 0-100 (int)
dev.speedIndex          # Discrete speed index (int)
dev.speedIndexCount     # Number of speed levels
dev.speedLabels         # List of speed labels
```

## MultiIODevice

Input/output devices.

```python
dev.binaryInputs        # List of binary input states
dev.binaryOutputs       # List of binary output states
dev.analogInputs        # List of analog input values
dev.sensorInputs        # List of sensor values
```

## Device Methods

### State Updates

```python
# Update single state
dev.updateStateOnServer('stateName', value=new_value)
dev.updateStateOnServer('stateName', value=new_value, uiValue="Display Text")

# Update multiple states (more efficient)
dev.updateStatesOnServer([
    {'key': 'state1', 'value': value1},
    {'key': 'state2', 'value': value2, 'uiValue': 'Display'}
])
```

### State Image

```python
dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
```

### Error State

```python
dev.setErrorStateOnServer("Connection failed")
dev.setErrorStateOnServer(None)  # Clear error
```

### Refresh Device Definition

```python
# Call if Devices.xml changed dynamically
dev.stateListOrDisplayStateIdChanged()
```

### Server Synchronization

```python
# Get fresh copy from server
dev.refreshFromServer()

# Push local changes to server
dev.replaceOnServer()

# Update plugin props
dev.replacePluginPropsOnServer(new_props_dict)
```

## HVAC Mode Constants

```python
indigo.kHvacMode.Off
indigo.kHvacMode.Heat
indigo.kHvacMode.Cool
indigo.kHvacMode.HeatCool  # Auto
indigo.kHvacMode.ProgramHeat
indigo.kHvacMode.ProgramCool
indigo.kHvacMode.ProgramHeatCool
```

## Fan Mode Constants

```python
indigo.kFanMode.Auto
indigo.kFanMode.AlwaysOn
```
