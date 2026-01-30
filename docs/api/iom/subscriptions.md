# Subscriptions and Event Callbacks

Subscribe to object changes to receive real-time notifications.

## Object Change Subscriptions

### Available Subscriptions

| Collection | Method |
|------------|--------|
| `indigo.devices` | `subscribeToChanges()` |
| `indigo.variables` | `subscribeToChanges()` |
| `indigo.triggers` | `subscribeToChanges()` |
| `indigo.actionGroups` | `subscribeToChanges()` |

### Subscribing

Call in `startup()`:

```python
def startup(self):
    indigo.devices.subscribeToChanges()
    indigo.variables.subscribeToChanges()
```

### Device Callbacks

```python
def deviceCreated(self, dev):
    """Called when any device is created."""
    pass

def deviceUpdated(self, origDev, newDev):
    """Called when device state or properties change."""
    # Always call super first
    indigo.PluginBase.deviceUpdated(self, origDev, newDev)

    # Check what changed
    if origDev.onState != newDev.onState:
        self.logger.info(f"{newDev.name} turned {'on' if newDev.onState else 'off'}")

def deviceDeleted(self, dev):
    """Called when any device is deleted."""
    pass
```

### Variable Callbacks

```python
def variableCreated(self, var):
    """Called when any variable is created."""
    pass

def variableUpdated(self, origVar, newVar):
    """Called when variable value changes."""
    indigo.PluginBase.variableUpdated(self, origVar, newVar)

    if origVar.value != newVar.value:
        self.logger.info(f"{newVar.name}: {origVar.value} -> {newVar.value}")

def variableDeleted(self, var):
    """Called when any variable is deleted."""
    pass
```

### Trigger Callbacks

```python
def triggerCreated(self, trigger):
    pass

def triggerUpdated(self, origTrigger, newTrigger):
    indigo.PluginBase.triggerUpdated(self, origTrigger, newTrigger)

def triggerDeleted(self, trigger):
    pass
```

### Action Group Callbacks

```python
def actionGroupCreated(self, actionGroup):
    pass

def actionGroupUpdated(self, origActionGroup, newActionGroup):
    indigo.PluginBase.actionGroupUpdated(self, origActionGroup, newActionGroup)

def actionGroupDeleted(self, actionGroup):
    pass
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

Subscriptions create significant traffic between IndigoServer and your plugin. Good use cases:

- Logging plugins (SQL Logger)
- Scene management (track device states)
- Integration bridges (sync with external systems)

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

def deviceUpdated(self, origDev, newDev):
    """Called when your device is updated (after subscribeToChanges)."""
    pass
```
