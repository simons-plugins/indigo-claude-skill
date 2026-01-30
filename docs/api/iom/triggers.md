# Trigger Classes Reference

## Trigger Class Hierarchy

```
indigo.Trigger (base)
├── indigo.DeviceStateChangeTrigger
├── indigo.VariableValueChangeTrigger
├── indigo.EmailReceivedTrigger
├── indigo.InsteonCommandReceivedTrigger
├── indigo.X10CommandReceivedTrigger
├── indigo.ServerStartupTrigger
├── indigo.PowerFailureTrigger
├── indigo.InterfaceFailureTrigger
├── indigo.InterfaceInitializedTrigger
└── indigo.PluginEventTrigger
```

## Common Trigger Properties

All trigger types share these properties:

```python
trigger.id              # Unique ID (int)
trigger.name            # Trigger name (str)
trigger.enabled         # Is enabled (bool)
trigger.folderId        # Parent folder ID
trigger.pluginId        # Plugin ID if plugin-defined
trigger.pluginTypeId    # Plugin's event type ID
```

## Trigger Types

### DeviceStateChangeTrigger

Fires when a device state changes.

```python
trigger = indigo.triggers[trigger_id]
trigger.deviceId        # Monitored device ID
trigger.stateSelector   # Which state to monitor
trigger.stateValue      # Value to match (if applicable)
```

### VariableValueChangeTrigger

Fires when a variable value changes.

```python
trigger.variableId      # Monitored variable ID
trigger.variableValue   # Value to match (if applicable)
```

### PluginEventTrigger

Fires when a plugin raises an event.

```python
trigger.pluginId        # Source plugin ID
trigger.pluginTypeId    # Event type from Events.xml
trigger.pluginProps     # Configuration properties
```

### EmailReceivedTrigger

Fires when email is received matching criteria.

### InsteonCommandReceivedTrigger

Fires when an INSTEON command is received.

```python
trigger.address         # INSTEON address to monitor
trigger.command         # Command type to match
```

### X10CommandReceivedTrigger

Fires when an X10 command is received.

### ServerStartupTrigger

Fires when Indigo server starts.

### PowerFailureTrigger

Fires on power failure detection.

### InterfaceFailureTrigger

Fires when a hardware interface fails.

### InterfaceInitializedTrigger

Fires when a hardware interface initializes.

## Plugin-Defined Triggers

Plugins define custom trigger types in `Events.xml`:

```xml
<Events>
    <Event id="motionDetected">
        <Name>Motion Detected</Name>
        <ConfigUI>
            <Field id="zone" type="menu">
                <Label>Zone:</Label>
            </Field>
        </ConfigUI>
    </Event>
</Events>
```

### Firing Plugin Events

```python
# In plugin code, fire the event
indigo.trigger.execute(trigger)

# Or trigger all matching plugin events
for trigger in indigo.triggers.iter("self.motionDetected"):
    if trigger.pluginProps.get("zone") == detected_zone:
        indigo.trigger.execute(trigger)
```

### triggerStartProcessing / triggerStopProcessing

```python
def triggerStartProcessing(self, trigger):
    """Called when trigger is enabled."""
    self.logger.debug(f"Trigger started: {trigger.name}")

def triggerStopProcessing(self, trigger):
    """Called when trigger is disabled."""
    self.logger.debug(f"Trigger stopped: {trigger.name}")
```

## Iterating Triggers

```python
# All triggers
for trigger in indigo.triggers:
    print(trigger.name)

# By type
for trigger in indigo.triggers.iter("indigo.devStateChange"):
    print(f"Device trigger: {trigger.name}")

# Plugin's own triggers
for trigger in indigo.triggers.iter("self"):
    print(f"My trigger: {trigger.name}")

# Specific plugin trigger type
for trigger in indigo.triggers.iter("self.motionDetected"):
    print(f"Motion trigger: {trigger.name}")
```

## Subscribing to Trigger Changes

```python
# In startup()
indigo.triggers.subscribeToChanges()

# Implement callbacks
def triggerCreated(self, trigger):
    pass

def triggerUpdated(self, origTrigger, newTrigger):
    pass

def triggerDeleted(self, trigger):
    pass
```
