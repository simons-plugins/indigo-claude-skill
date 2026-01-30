# Indigo Object Model (IOM) Reference

The IOM provides Python access to Indigo objects. See [official documentation](https://wiki.indigodomo.com/doku.php?id=indigo_2025.1_documentation:object_model_reference).

## Detailed Documentation

| Topic | File |
|-------|------|
| Architecture & Core Concepts | [iom/architecture.md](iom/architecture.md) |
| Command Namespaces | [iom/command-namespaces.md](iom/command-namespaces.md) |
| Device Classes | [iom/devices.md](iom/devices.md) |
| Trigger Classes | [iom/triggers.md](iom/triggers.md) |
| indigo.Dict & indigo.List | [iom/containers.md](iom/containers.md) |
| Iteration Filters | [iom/filters.md](iom/filters.md) |
| Subscriptions & Callbacks | [iom/subscriptions.md](iom/subscriptions.md) |
| Constants | [iom/constants.md](iom/constants.md) |
| Utility Functions | [iom/utilities.md](iom/utilities.md) |

## Quick Reference

### Access Objects

```python
dev = indigo.devices[123456]          # By ID
dev = indigo.devices["Device Name"]   # By name
var = indigo.variables["VarName"]
trigger = indigo.triggers[trigger_id]
ag = indigo.actionGroups[ag_id]
```

### Iterate Objects

```python
for dev in indigo.devices:                    # All devices
for dev in indigo.devices.iter("self"):       # Plugin's devices
for dev in indigo.devices.iter("indigo.dimmer"):  # All dimmers
```

### Modify Objects

```python
# Get copy, modify, push back
dev = indigo.devices[123456]
dev.name = "New Name"
dev.replaceOnServer()

# Update state
dev.updateStateOnServer('myState', value=42)

# Update plugin props
dev.replacePluginPropsOnServer(new_props)
```

### Send Commands

```python
indigo.dimmer.turnOn(dev)
indigo.dimmer.setBrightness(dev, value=75)
indigo.relay.toggle(dev)
indigo.thermostat.setHeatSetpoint(dev, value=68)
indigo.variable.updateValue(var, value="new")
indigo.actionGroup.execute(ag)
```

### Server Commands

```python
indigo.server.log("message")
indigo.server.speak("Hello")
time = indigo.server.getTime()
```

### Subscribe to Changes

```python
# In startup()
indigo.devices.subscribeToChanges()

# Callback
def deviceUpdated(self, origDev, newDev):
    indigo.PluginBase.deviceUpdated(self, origDev, newDev)
    # Handle change
```

## Key Concepts

1. **Objects are copies** - When you get an object, you get a copy, not the real object
2. **Use command namespaces** - `indigo.dimmer.turnOn(dev)` not `dev.turnOn()`
3. **replaceOnServer()** - Push local changes to server
4. **Store IDs, not names** - Names can change, IDs are permanent

## Common Tasks

| Task | Solution |
|------|----------|
| Turn on a device | `indigo.dimmer.turnOn(dev)` |
| Update device state | `dev.updateStateOnServer('key', value=val)` |
| Create variable | `indigo.variable.create("Name", value="val")` |
| Execute action group | `indigo.actionGroup.execute(ag_id)` |
| Get device name efficiently | `indigo.devices.getName(dev_id)` |
| Log message | `indigo.server.log("message")` |
| Convert to dict | `dict(dev)` |
| Serialize to JSON | `json.dumps(dict(dev), cls=indigo.utils.IndigoJSONEncoder)` |
