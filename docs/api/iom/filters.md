# Iteration Filters Reference

Use filters with `.iter()` to efficiently iterate subsets of objects.

## Device Filters

```python
for dev in indigo.devices.iter("filter"):
    pass
```

### Protocol Filters

| Filter | Description |
|--------|-------------|
| `indigo.insteon` | INSTEON devices |
| `indigo.zwave` | Z-Wave devices |
| `indigo.x10` | X10 devices |

### Device Type Filters

| Filter | Description |
|--------|-------------|
| `indigo.dimmer` | Dimmer devices |
| `indigo.relay` | Relay/switch/lock devices |
| `indigo.sensor` | Sensor devices |
| `indigo.thermostat` | Thermostat devices |
| `indigo.sprinkler` | Sprinkler devices |
| `indigo.speedcontrol` | Speed control devices |
| `indigo.iodevice` | Input/output devices |

### Capability Filters

| Filter | Description |
|--------|-------------|
| `indigo.responder` | Devices whose state can be changed |
| `indigo.controller` | Devices that can send commands |

### Plugin Filters

| Filter | Description |
|--------|-------------|
| `self` | Devices defined by calling plugin |
| `self.myDeviceType` | Specific device type from calling plugin |
| `com.company.plugin` | All devices from specific plugin |
| `com.company.plugin.deviceType` | Specific device type from plugin |

### Property Filters

| Filter | Description |
|--------|-------------|
| `props.SupportsOnState` | Devices supporting ON state |

### Combining Filters

Combine filters with commas:

```python
# INSTEON dimmers only
for dev in indigo.devices.iter("indigo.dimmer, indigo.insteon"):
    print(dev.name)

# Z-Wave sensors only
for dev in indigo.devices.iter("indigo.sensor, indigo.zwave"):
    print(dev.name)
```

## Trigger Filters

```python
for trigger in indigo.triggers.iter("filter"):
    pass
```

| Filter | Description |
|--------|-------------|
| `indigo.devStateChange` | Device state change triggers |
| `indigo.varValueChange` | Variable value change triggers |
| `indigo.emailRcvd` | Email received triggers |
| `indigo.insteonCmdRcvd` | INSTEON command received |
| `indigo.x10CmdRcvd` | X10 command received |
| `indigo.serverStartup` | Server startup triggers |
| `indigo.powerFail` | Power failure triggers |
| `indigo.interfaceFail` | Interface failure triggers |
| `indigo.interfaceInit` | Interface initialized triggers |
| `indigo.pluginEvent` | Plugin-defined event triggers |
| `self` | Triggers from calling plugin |
| `self.myTriggerType` | Specific trigger type from plugin |
| `com.company.plugin.triggerType` | Trigger type from other plugin |

**Note**: Unlike devices, only a single trigger filter can be used.

## Variable Filters

```python
for var in indigo.variables.iter("filter"):
    pass
```

| Filter | Description |
|--------|-------------|
| `indigo.readWrite` | Read/write variables only |

## Examples

### All Plugin Devices

```python
for dev in indigo.devices.iter("self"):
    self.logger.info(f"My device: {dev.name}")
```

### Specific Plugin Device Type

```python
for dev in indigo.devices.iter("self.myThermostat"):
    self.logger.info(f"My thermostat: {dev.name}")
```

### All Dimmers at Full Brightness

```python
for dev in indigo.devices.iter("indigo.dimmer"):
    if dev.brightness == 100:
        self.logger.info(f"Full bright: {dev.name}")
```

### Device State Change Triggers

```python
for trigger in indigo.triggers.iter("indigo.devStateChange"):
    self.logger.info(f"Monitoring device {trigger.deviceId}")
```

### Iterate IDs Only (More Efficient)

```python
# When you only need IDs, not full objects
for dev_id in indigo.devices.iterkeys():
    # Process without loading full device
    pass
```

## Iteration Behavior

When iteration begins, the list is fixed:
- Items added during iteration are NOT included
- Items deleted during iteration are gracefully skipped
- No exceptions are thrown for mid-iteration changes
