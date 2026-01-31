# Command Namespaces Reference

Commands are organized into namespaces matching their target class type.

## Device Commands

| Class | Namespace | Description |
|-------|-----------|-------------|
| `indigo.Device` | `indigo.device.*` | All device subclasses |
| `indigo.DimmerDevice` | `indigo.dimmer.*` | Dimmer devices |
| `indigo.RelayDevice` | `indigo.relay.*` | Relay, lock, 2-state devices |
| `indigo.SensorDevice` | `indigo.sensor.*` | Sensor devices |
| `indigo.SpeedControlDevice` | `indigo.speedcontrol.*` | Speed control/motor devices |
| `indigo.SprinklerDevice` | `indigo.sprinkler.*` | Sprinkler devices |
| `indigo.ThermostatDevice` | `indigo.thermostat.*` | Thermostat devices |
| `indigo.MultiIODevice` | `indigo.iodevice.*` | Input/output devices |

### Common Device Commands

```python
# Create device (factory method for all types)
indigo.device.create(protocol, deviceTypeId=..., props=...)

# Duplicate device
indigo.device.duplicate(dev_or_id, duplicateName="Copy")

# Delete device
indigo.device.delete(dev_or_id)

# Move to folder
indigo.device.moveToFolder(dev_or_id, folder_id)

# Enable/disable
indigo.device.enable(dev_or_id, value=True)

# Display in remote UI
indigo.device.displayInRemoteUI(dev_or_id, value=True)
```

### Dimmer Commands

```python
indigo.dimmer.turnOn(dev)
indigo.dimmer.turnOff(dev)
indigo.dimmer.toggle(dev)
indigo.dimmer.setBrightness(dev, value=75)
indigo.dimmer.brightenBy(dev, value=10)
indigo.dimmer.dimBy(dev, value=10)
indigo.dimmer.statusRequest(dev)
```

### Relay Commands

```python
indigo.relay.turnOn(dev)
indigo.relay.turnOff(dev)
indigo.relay.toggle(dev)
indigo.relay.statusRequest(dev)
```

### Sensor Commands

```python
indigo.sensor.turnOn(dev)   # For virtual sensors
indigo.sensor.turnOff(dev)
indigo.sensor.statusRequest(dev)
```

### Thermostat Commands

```python
indigo.thermostat.setHeatSetpoint(dev, value=68)
indigo.thermostat.setCoolSetpoint(dev, value=76)
indigo.thermostat.setHvacMode(dev, value=indigo.kHvacMode.Auto)
indigo.thermostat.setFanMode(dev, value=indigo.kFanMode.Auto)
indigo.thermostat.statusRequest(dev)
```

### Sprinkler Commands

```python
indigo.sprinkler.setActiveZone(dev, index=1)
indigo.sprinkler.run(dev)
indigo.sprinkler.stop(dev)
indigo.sprinkler.pause(dev)
indigo.sprinkler.resume(dev)
indigo.sprinkler.previousZone(dev)
indigo.sprinkler.nextZone(dev)
```

### Speed Control Commands

```python
indigo.speedcontrol.turnOn(dev)
indigo.speedcontrol.turnOff(dev)
indigo.speedcontrol.toggle(dev)
indigo.speedcontrol.setSpeedLevel(dev, value=50)
indigo.speedcontrol.setSpeedIndex(dev, value=2)
indigo.speedcontrol.increaseSpeedIndex(dev)
indigo.speedcontrol.decreaseSpeedIndex(dev)
indigo.speedcontrol.statusRequest(dev)
```

## Trigger Commands

| Class | Namespace |
|-------|-----------|
| `indigo.Trigger` | `indigo.trigger.*` |
| `indigo.DeviceStateChangeTrigger` | `indigo.devStateChange.*` |
| `indigo.VariableValueChangeTrigger` | `indigo.varValueChange.*` |
| `indigo.EmailReceivedTrigger` | `indigo.emailRcvd.*` |
| `indigo.InsteonCommandReceivedTrigger` | `indigo.insteonCmdRcvd.*` |
| `indigo.X10CommandReceivedTrigger` | `indigo.x10CmdRcvd.*` |
| `indigo.ServerStartupTrigger` | `indigo.serverStartup.*` |
| `indigo.PowerFailureTrigger` | `indigo.powerFail.*` |
| `indigo.InterfaceFailureTrigger` | `indigo.interfaceFail.*` |
| `indigo.InterfaceInitializedTrigger` | `indigo.interfaceInit.*` |
| `indigo.PluginEventTrigger` | `indigo.pluginEvent.*` |

```python
# Common trigger commands
indigo.trigger.enable(trigger_or_id, value=True)
indigo.trigger.execute(trigger_or_id)
indigo.trigger.delete(trigger_or_id)
indigo.trigger.moveToFolder(trigger_or_id, folder_id)
```

## Variable Commands

| Class | Namespace |
|-------|-----------|
| `indigo.Variable` | `indigo.variable.*` |

```python
# Create variable
indigo.variable.create("VarName", value="initial", folder=folder_id)

# Update value
indigo.variable.updateValue(var_or_id, value="new value")

# Delete
indigo.variable.delete(var_or_id)

# Move to folder
indigo.variable.moveToFolder(var_or_id, folder_id)
```

## Action Group Commands

| Class | Namespace |
|-------|-----------|
| `indigo.ActionGroup` | `indigo.actionGroup.*` |

```python
# Execute action group
indigo.actionGroup.execute(ag_or_id)

# Enable/disable
indigo.actionGroup.enable(ag_or_id, value=True)

# Delete
indigo.actionGroup.delete(ag_or_id)
```

## Schedule Commands

| Class | Namespace |
|-------|-----------|
| `indigo.Schedule` | `indigo.schedule.*` |

```python
# Enable/disable
indigo.schedule.enable(sched_or_id, value=True)

# Delete
indigo.schedule.delete(sched_or_id)
```

## Protocol-Specific Commands

### INSTEON

```python
indigo.insteon.sendRawInsteon(address, cmd, cmd2=0, waitUntilAck=True)
indigo.insteon.sendRawExtended(address, cmd, cmd2, data)
indigo.insteon.subscribeToIncoming()  # Low-level monitoring
indigo.insteon.subscribeToOutgoing()
```

### X10

```python
indigo.x10.sendRawX10(address, cmd)
indigo.x10.subscribeToIncoming()
indigo.x10.subscribeToOutgoing()
```

## Server Commands

```python
indigo.server.log("message")
indigo.server.error("error message")
indigo.server.speak("text to speak", waitUntilDone=False)
indigo.server.getTime()
indigo.server.apiVersion   # Property, e.g., "3.6"
indigo.server.version      # Property, e.g., "2025.1"
```

## Common Command Patterns

All namespaces support these methods for their object type:

| Method | Description |
|--------|-------------|
| `create()` | Create new object |
| `duplicate()` | Duplicate existing object |
| `delete()` | Delete object |
| `enable()` | Enable/disable object |
| `moveToFolder()` | Move to folder |
