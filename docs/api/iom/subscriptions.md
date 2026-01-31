# Subscriptions and Event Callbacks

Subscribe to object changes to receive real-time notifications.

## Object Change Subscriptions

### Available Subscriptions

| Collection | Method |
|------------|--------|
| `indigo.devices` | `subscribeToChanges()` |
| `indigo.variables` | `subscribeToChanges()` |
| `indigo.triggers` | `subscribeToChanges()` |
| `indigo.schedules` | `subscribeToChanges()` |
| `indigo.actionGroups` | `subscribeToChanges()` |
| `indigo.controlPages` | `subscribeToChanges()` |

### Subscribing

Call in `__init__()` or `startup()`:

```python
def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
    super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

    indigo.devices.subscribeToChanges()
    indigo.variables.subscribeToChanges()
    indigo.triggers.subscribeToChanges()
    indigo.actionGroups.subscribeToChanges()
```

**Note**: Use sparingly - subscriptions generate significant traffic between IndigoServer and your plugin.

## Device Callbacks

```python
def deviceCreated(self, dev):
    """Called when any device is created."""
    self.logger.debug(f"{dev.name} created")

def deviceUpdated(self, origDev, newDev):
    """Called when device state or properties change."""
    # Always call super first
    indigo.PluginBase.deviceUpdated(self, origDev, newDev)

    # Check what changed
    if origDev.onState != newDev.onState:
        self.logger.info(f"{newDev.name} turned {'on' if newDev.onState else 'off'}")

def deviceDeleted(self, dev):
    """Called when any device is deleted."""
    self.logger.debug(f"{dev.name} deleted")
```

### Finding What Changed

```python
def deviceUpdated(self, origDev, newDev):
    indigo.PluginBase.deviceUpdated(self, origDev, newDev)

    # Convert to dicts for comparison
    orig_dict = dict(origDev)
    new_dict = dict(newDev)

    # Find changed attributes
    diff = {k: new_dict[k] for k in orig_dict
            if k in new_dict and orig_dict[k] != new_dict[k]}

    if diff:
        self.logger.debug(f"Changed: {diff}")
```

## Variable Callbacks

```python
def variableCreated(self, var):
    """Called when any variable is created."""
    self.logger.debug(f"Variable created: {var.name}")

def variableUpdated(self, origVar, newVar):
    """Called when variable value changes."""
    indigo.PluginBase.variableUpdated(self, origVar, newVar)

    if origVar.value != newVar.value:
        self.logger.info(f"{newVar.name}: {origVar.value} -> {newVar.value}")

def variableDeleted(self, var):
    """Called when any variable is deleted."""
    self.logger.debug(f"Variable deleted: {var.name}")
```

## Trigger Callbacks

```python
def triggerCreated(self, trigger):
    self.logger.debug(f"Trigger created: {trigger.name}")

def triggerUpdated(self, origTrigger, newTrigger):
    indigo.PluginBase.triggerUpdated(self, origTrigger, newTrigger)

def triggerDeleted(self, trigger):
    self.logger.debug(f"Trigger deleted: {trigger.name}")
```

## Schedule Callbacks

```python
def scheduleCreated(self, schedule):
    self.logger.debug(f"Schedule created: {schedule.name}")

def scheduleUpdated(self, origSchedule, newSchedule):
    indigo.PluginBase.scheduleUpdated(self, origSchedule, newSchedule)

def scheduleDeleted(self, schedule):
    self.logger.debug(f"Schedule deleted: {schedule.name}")
```

## Action Group Callbacks

```python
def actionGroupCreated(self, actionGroup):
    self.logger.debug(f"Action group created: {actionGroup.name}")

def actionGroupUpdated(self, origActionGroup, newActionGroup):
    indigo.PluginBase.actionGroupUpdated(self, origActionGroup, newActionGroup)

def actionGroupDeleted(self, actionGroup):
    self.logger.debug(f"Action group deleted: {actionGroup.name}")
```

## Control Page Callbacks

```python
def controlPageCreated(self, controlPage):
    self.logger.debug(f"Control page created: {controlPage.name}")

def controlPageUpdated(self, origControlPage, newControlPage):
    indigo.PluginBase.controlPageUpdated(self, origControlPage, newControlPage)

def controlPageDeleted(self, controlPage):
    self.logger.debug(f"Control page deleted: {controlPage.name}")
```

## Low-Level Protocol Subscriptions

Monitor raw INSTEON or X10 commands (regardless of effect on device state).

### INSTEON

```python
def startup(self):
    indigo.insteon.subscribeToIncoming()
    indigo.insteon.subscribeToOutgoing()

def insteonCommandReceived(self, cmd):
    """Called for incoming INSTEON commands."""
    self.logger.debug(f"INSTEON received: {cmd}")

def insteonCommandSent(self, cmd):
    """Called for outgoing INSTEON commands."""
    self.logger.debug(f"INSTEON sent: {cmd}")
```

### X10

```python
def startup(self):
    indigo.x10.subscribeToIncoming()
    indigo.x10.subscribeToOutgoing()

def x10CommandReceived(self, cmd):
    """Called for incoming X10 commands."""
    self.logger.debug(f"X10 received: {cmd}")

    if cmd.cmdType == "sec":  # Security command
        if cmd.secCodeId == 6:
            if cmd.secFunc == "sensor alert (max delay)":
                self.logger.info("SENSOR OPEN")
            elif cmd.secFunc == "sensor normal (max delay)":
                self.logger.info("SENSOR CLOSED")

def x10CommandSent(self, cmd):
    """Called for outgoing X10 commands."""
    self.logger.debug(f"X10 sent: {cmd}")
```

## Best Practices

### Use Sparingly

Subscriptions create significant traffic. Good use cases:

- Logging plugins (SQL Logger)
- Scene management (track device states)
- Integration bridges (sync with external systems)
- Fan controllers (monitor related devices)

### Filter in Callbacks

Check if the change is relevant before processing:

```python
def deviceUpdated(self, origDev, newDev):
    indigo.PluginBase.deviceUpdated(self, origDev, newDev)

    # Only process our plugin's devices
    if newDev.pluginId != self.pluginId:
        return

    # Only process if state actually changed
    if origDev.states == newDev.states:
        return

    # Now do work
    self.processDeviceChange(newDev)
```

### Subscription Scope

Note that `subscribeToChanges()` reports **actual changes only**:

- Light turns ON → notification
- Light commanded ON when already ON → no notification (no change)

### Plugin Device Subscriptions

For your own plugin's devices, prefer the device lifecycle methods:

```python
def deviceStartComm(self, dev):
    """Called when your device starts."""
    pass

def deviceStopComm(self, dev):
    """Called when your device stops."""
    pass
```

## Example: Multi-Device Sync

Sync multiple fans to act as one:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    indigo.devices.subscribeToChanges()
    self.syncing = False  # Prevent loops

def deviceUpdated(self, origDev, newDev):
    indigo.PluginBase.deviceUpdated(self, origDev, newDev)

    # Avoid recursive updates
    if self.syncing:
        return

    # Only handle our grouped fans
    if newDev.pluginId != self.pluginId:
        return
    if newDev.deviceTypeId != "groupedFan":
        return

    # Check if speed changed
    if origDev.speedLevel == newDev.speedLevel:
        return

    # Sync all fans in group
    self.syncing = True
    try:
        group_id = newDev.pluginProps.get("groupId")
        for dev in indigo.devices.iter("self.groupedFan"):
            if dev.id != newDev.id:
                if dev.pluginProps.get("groupId") == group_id:
                    indigo.speedcontrol.setSpeedLevel(dev, value=newDev.speedLevel)
    finally:
        self.syncing = False
```
