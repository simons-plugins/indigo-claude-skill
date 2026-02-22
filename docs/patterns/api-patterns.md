# Indigo API Patterns

Common patterns for working with the Indigo Object Model.

For core concepts like client-server architecture, object modification, and `replaceOnServer()` patterns, see [IOM Architecture](../api/iom/architecture.md).

## Device State Updates

### Single State

```python
dev.updateStateOnServer('temperature', value=72.5)

# With UI display value
dev.updateStateOnServer('temperature', value=72.5, uiValue="72.5°F")
```

### Batch Updates (Preferred)

More efficient than multiple single updates:

```python
states = [
    {'key': 'temperature', 'value': 72.5, 'uiValue': '72.5°F'},
    {'key': 'humidity', 'value': 45},
    {'key': 'status', 'value': 'online'},
    {'key': 'lastUpdate', 'value': str(datetime.now())}
]
dev.updateStatesOnServer(states)
```

### With Decimal Places

```python
states = [
    {'key': 'temperature', 'value': 72.5, 'decimalPlaces': 1},
    {'key': 'humidity', 'value': 45.234, 'decimalPlaces': 2}
]
dev.updateStatesOnServer(states)
```

### Error States

```python
# Set error (displays in UI)
dev.setErrorStateOnServer("Connection failed")

# Clear error
dev.setErrorStateOnServer(None)
```

### State Icons

```python
# Update icon based on state
if dev.onState:
    dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
else:
    dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)

# Error icon
dev.updateStateImageOnServer(indigo.kStateImageSel.Error)
```

## Object Access Patterns

### By ID (Preferred)

```python
dev = indigo.devices[123456]
var = indigo.variables[789012]
```

### By Name (Not Recommended for Storage)

```python
dev = indigo.devices["Living Room Lamp"]
```

### Safe Access with Existence Check

```python
if 123456 in indigo.devices:
    dev = indigo.devices[123456]
else:
    self.logger.error("Device not found")
```

### Using get() for Variables

```python
# Returns None if not found
var = indigo.variables.get("MyVariable")
if var:
    value = var.value
```

## Iteration Patterns

### All Objects

```python
for dev in indigo.devices:
    self.logger.info(dev.name)
```

### Plugin's Own Devices

```python
for dev in indigo.devices.iter("self"):
    self.update_device(dev)
```

### Specific Device Type

```python
for dev in indigo.devices.iter("self.myThermostat"):
    self.poll_thermostat(dev)
```

### By Protocol

```python
for dev in indigo.devices.iter("indigo.insteon"):
    self.logger.info(f"INSTEON: {dev.address}")
```

### IDs Only (More Efficient)

```python
for dev_id in indigo.devices.iterkeys():
    # Process without loading full device
    name = indigo.devices.getName(dev_id)
```

## Variable Patterns

### Create Variable

```python
try:
    var = indigo.variable.create("MyPluginStatus", value="initialized")
except:
    # Variable already exists
    var = indigo.variables["MyPluginStatus"]
```

### Update Variable

```python
indigo.variable.updateValue(var.id, value="running")
# or
indigo.variable.updateValue("MyPluginStatus", value="running")
```

### Safe Variable Access

```python
def get_variable_value(self, name, default=""):
    """Safely get variable value with default"""
    try:
        return indigo.variables[name].value
    except KeyError:
        return default
```

## Action Group Patterns

### Execute

```python
# By ID
indigo.actionGroup.execute(123456)

# By name
ag = indigo.actionGroups["Morning Routine"]
indigo.actionGroup.execute(ag.id)

# With event data (passed to actions in the group)
event_data = indigo.Dict()
event_data["scene"] = "evening"
indigo.actionGroup.execute(ag.id, event_data=event_data)
```

### Dependencies and Management

```python
# Check what depends on an action group before deleting
deps = indigo.actionGroup.getDependencies(ag.id)
if deps:
    indigo.server.log(f"Action group has dependencies: {deps}")

# Duplicate an action group
new_ag = indigo.actionGroup.duplicate(ag.id, duplicateName="Morning Routine v2")

# Move to a folder
indigo.actionGroup.moveToFolder(ag.id, value=folder_id)
```

## Schedule Patterns

### Execute and Control

```python
# Execute a schedule immediately
indigo.schedule.execute(sched.id)

# Execute ignoring conditions
indigo.schedule.execute(sched.id, ignoreConditions=True)

# Execute with metadata
sched_data = indigo.Dict()
sched_data["reason"] = "manual override"
indigo.schedule.execute(sched.id, schedule_data=sched_data)

# Enable with delay (seconds before activation) and duration (auto-disable after)
indigo.schedule.enable(sched.id, value=True, delay=30, duration=3600)

# Cancel pending delayed actions
indigo.schedule.removeDelayedActions(sched.id)
```

### Dependencies and Management

```python
# Check dependencies before deletion
deps = indigo.schedule.getDependencies(sched.id)

# Duplicate a schedule
new_sched = indigo.schedule.duplicate(sched.id, duplicateName="Weekday Backup")

# Move to a folder
indigo.schedule.moveToFolder(sched.id, value=folder_id)
```

## Logging Patterns

### Standard Logging

```python
self.logger.debug("Detailed info for debugging")
self.logger.info("Normal operational info")
self.logger.warning("Something unexpected but recoverable")
self.logger.error("Error that needs attention")
```

### Server Log (Visible in Event Log)

```python
indigo.server.log("Message visible in Event Log")
indigo.server.log("Error message", isError=True)
```

## JSON Serialization

```python
import json

# Serialize device with proper date handling
dev_dict = dict(dev)
json_str = json.dumps(dev_dict, indent=2, cls=indigo.utils.IndigoJSONEncoder)
```

## Common Anti-Patterns

### Don't Store Names

```python
# BAD - name can change
self.device_name = "Living Room Lamp"

# GOOD - ID is permanent
self.device_id = 123456
```

### Don't Modify Cached Objects

```python
# BAD - changes lost
dev = indigo.devices[123456]
dev.name = "New Name"
# forgot replaceOnServer()

# GOOD
dev = indigo.devices[123456]
dev.name = "New Name"
dev.replaceOnServer()
```

### Don't Update States Unnecessarily

```python
# BAD - updates even when unchanged
def poll(self):
    temp = self.read_temperature()
    dev.updateStateOnServer('temperature', value=temp)

# GOOD - only update on change
def poll(self):
    temp = self.read_temperature()
    if dev.states['temperature'] != temp:
        dev.updateStateOnServer('temperature', value=temp)
```

## See Also

- [IOM Architecture](../api/iom/architecture.md) - Core concepts, replaceOnServer, pluginProps
- [Device Classes](../api/iom/devices.md) - Device properties and methods
- [Filters](../api/iom/filters.md) - Iteration patterns
