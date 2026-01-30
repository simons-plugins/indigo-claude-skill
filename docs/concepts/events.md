# Custom Plugin Events (Events.xml)

Define custom trigger events that users can respond to in Indigo.

## Overview

Events.xml defines plugin-specific events that appear in Indigo's trigger system alongside built-in events like Power Failure or Email Received.

Use cases:
- Update notifications
- Battery low alerts
- Button press events
- Connection status changes
- Custom sensor events

## Events.xml Structure

```xml
<?xml version="1.0"?>
<Events>
    <SupportURL>https://example.com/plugin/events.html</SupportURL>

    <Event id="updateAvailable">
        <Name>Plugin Update Available</Name>
        <ConfigUI>
            <Field id="notifyEmail" type="checkbox" defaultValue="true">
                <Label>Send email notification:</Label>
            </Field>
        </ConfigUI>
    </Event>

    <Event id="batteryLow">
        <Name>Battery Low</Name>
        <ConfigUI>
            <Field id="threshold" type="textfield" defaultValue="20">
                <Label>Threshold (%):</Label>
            </Field>
        </ConfigUI>
    </Event>

    <!-- Separator for visual grouping -->
    <Event id="sep1"/>

    <Event id="connectionLost">
        <Name>Connection Lost</Name>
    </Event>
</Events>
```

## Event Elements

| Element | Description |
|---------|-------------|
| `<Event id="...">` | Unique identifier for the event |
| `<Name>` | Display name in trigger UI |
| `<ConfigUI>` | Optional configuration fields |
| `<SupportURL>` | Help link for the event |

## Firing Events

Trigger events from your plugin code:

```python
def _check_for_updates(self):
    if self._update_available():
        # Fire event for all matching triggers
        for trigger in indigo.triggers.iter("self.updateAvailable"):
            if trigger.enabled:
                indigo.trigger.execute(trigger)

def _check_battery(self, dev, level):
    for trigger in indigo.triggers.iter("self.batteryLow"):
        if not trigger.enabled:
            continue

        threshold = int(trigger.pluginProps.get("threshold", 20))
        if level < threshold:
            indigo.trigger.execute(trigger)
```

## Event Callback Methods

### triggerStartProcessing

Called when a trigger using your event is enabled:

```python
def triggerStartProcessing(self, trigger):
    """Called when trigger is enabled."""
    self.logger.debug(f"Trigger started: {trigger.name}")

    # Track active triggers
    self.active_triggers[trigger.id] = trigger.pluginTypeId
```

### triggerStopProcessing

Called when a trigger is disabled:

```python
def triggerStopProcessing(self, trigger):
    """Called when trigger is disabled."""
    self.logger.debug(f"Trigger stopped: {trigger.name}")

    # Remove from tracking
    if trigger.id in self.active_triggers:
        del self.active_triggers[trigger.id]
```

### validateEventConfigUi

Validate event configuration:

```python
def validateEventConfigUi(self, valuesDict, typeId, triggerId):
    """Validate event configuration."""
    errorsDict = indigo.Dict()

    if typeId == "batteryLow":
        try:
            threshold = int(valuesDict.get("threshold", 20))
            if threshold < 1 or threshold > 100:
                errorsDict["threshold"] = "Must be between 1 and 100"
        except ValueError:
            errorsDict["threshold"] = "Must be a number"

    if errorsDict:
        return (False, valuesDict, errorsDict)

    return (True, valuesDict)
```

### getEventConfigUiValues

Provide initial/default values:

```python
def getEventConfigUiValues(self, pluginProps, typeId, triggerId):
    """Return initial values for event config UI."""
    valuesDict = pluginProps

    if typeId == "batteryLow":
        valuesDict.setdefault("threshold", "20")

    return valuesDict
```

### closedEventConfigUi

Called after event config is saved:

```python
def closedEventConfigUi(self, valuesDict, userCancelled, typeId, triggerId):
    """Called after event config dialog closes."""
    if userCancelled:
        return

    self.logger.debug(f"Event config saved: {typeId}")
```

## Complete Example

### Events.xml

```xml
<?xml version="1.0"?>
<Events>
    <Event id="motionDetected">
        <Name>Motion Detected</Name>
        <ConfigUI>
            <Field id="zone" type="menu">
                <Label>Zone:</Label>
                <List class="self" method="getZoneList"/>
            </Field>
            <Field id="sensitivity" type="menu" defaultValue="medium">
                <Label>Sensitivity:</Label>
                <List>
                    <Option value="low">Low</Option>
                    <Option value="medium">Medium</Option>
                    <Option value="high">High</Option>
                </List>
            </Field>
        </ConfigUI>
    </Event>
</Events>
```

### plugin.py

```python
def getZoneList(self, filter="", valuesDict=None, typeId="", targetId=0):
    """Return list of zones for event config."""
    zones = []
    for dev in indigo.devices.iter("self.motionSensor"):
        zone = dev.pluginProps.get("zone", "unknown")
        zones.append((zone, f"Zone: {zone}"))
    return zones

def triggerStartProcessing(self, trigger):
    self.logger.debug(f"Motion trigger started: {trigger.name}")
    self.motion_triggers.append(trigger.id)

def triggerStopProcessing(self, trigger):
    self.logger.debug(f"Motion trigger stopped: {trigger.name}")
    if trigger.id in self.motion_triggers:
        self.motion_triggers.remove(trigger.id)

def _on_motion_detected(self, zone):
    """Called when motion is detected."""
    for trigger_id in self.motion_triggers:
        try:
            trigger = indigo.triggers[trigger_id]
            if not trigger.enabled:
                continue

            # Check if zone matches
            trigger_zone = trigger.pluginProps.get("zone", "")
            if trigger_zone and trigger_zone != zone:
                continue

            # Fire the trigger
            indigo.trigger.execute(trigger)

        except KeyError:
            # Trigger was deleted
            self.motion_triggers.remove(trigger_id)
```

## Best Practices

- Use descriptive event IDs and names
- Provide sensible defaults in ConfigUI
- Validate all configuration input
- Track active triggers to avoid unnecessary iteration
- Handle deleted triggers gracefully
- Use separators to group related events

## See Also

- [Trigger Classes Reference](../api/iom/triggers.md) - Trigger object properties
- [Subscriptions](../api/iom/subscriptions.md) - Monitor trigger changes
- [Plugin Lifecycle](plugin-lifecycle.md) - When callbacks are called
