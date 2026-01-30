# Device Development

**Official Documentation**: https://wiki.indigodomo.com/doku.php?id=indigo_2025.1_documentation:plugin_guide#devices

## Device Types

Plugins can create devices of various types defined in `Devices.xml`:

### Native Device Types

These inherit states and actions from Indigo:

| Type | Actions | Use Case | Example |
|------|---------|----------|---------|
| `relay` | ON/OFF/TOGGLE/STATUS | Binary switches, outlets | Smart plugs |
| `dimmer` | ON/OFF/DIM/BRIGHTEN/SET BRIGHTNESS | Dimmable lights | LED bulbs |
| `speedcontrol` | ON/OFF/SET SPEED LEVEL/INCREASE/DECREASE | Fan control | Ceiling fans |
| `sensor` | ON/OFF/STATUS (read-only) | Sensors, monitors | Motion sensors |
| `thermostat` | Full HVAC control | Climate control | Smart thermostats |
| `sprinkler` | Zone control | Irrigation | Sprinkler systems |

### Custom Device Type

Complete control over states and actions:

```xml
<Device type="custom" id="myCustomDevice">
    <Name>My Custom Device</Name>
    <ConfigUI>
        <!-- Configuration fields -->
    </ConfigUI>
    <States>
        <!-- Custom states -->
    </States>
</Device>
```

## Device Definition (Devices.xml)

### Basic Structure

```xml
<?xml version="1.0"?>
<Devices>
    <Device type="custom" id="deviceTypeId">
        <Name>Display Name</Name>
        <ConfigUI>
            <!-- User configuration fields -->
        </ConfigUI>
        <States>
            <!-- Device states -->
        </States>
        <UiDisplayStateId>primaryStateId</UiDisplayStateId>
    </Device>
</Devices>
```

### State Definitions

States store device data and can trigger events:

```xml
<States>
    <State id="temperature">
        <ValueType>Number</ValueType>
        <TriggerLabel>Temperature</TriggerLabel>
        <ControlPageLabel>Temp</ControlPageLabel>
    </State>
    <State id="isOnline">
        <ValueType>Boolean</ValueType>
        <TriggerLabel>Device Online Status</TriggerLabel>
        <ControlPageLabel>Online</ControlPageLabel>
    </State>
    <State id="status">
        <ValueType>String</ValueType>
        <TriggerLabel>Status Message</TriggerLabel>
        <ControlPageLabel>Status</ControlPageLabel>
    </State>
</States>
```

**Value Types**: `Integer`, `Number`, `String`, `Boolean`, `Separator`

### Configuration UI (ConfigUI)

```xml
<ConfigUI>
    <Field id="address" type="textfield">
        <Label>Device Address:</Label>
    </Field>
    <Field id="pollingInterval" type="textfield" defaultValue="60">
        <Label>Polling Interval (seconds):</Label>
    </Field>
    <Field id="enableLogging" type="checkbox" defaultValue="false">
        <Label>Enable Detailed Logging:</Label>
    </Field>
    <Field id="deviceType" type="menu" defaultValue="sensor">
        <Label>Device Type:</Label>
        <List>
            <Option value="sensor">Sensor</Option>
            <Option value="switch">Switch</Option>
        </List>
    </Field>
</ConfigUI>
```

**Field Types**: `textfield`, `textarea`, `checkbox`, `menu`, `list`, `button`, `label`, `separator`

## Device Lifecycle

Device lifecycle callbacks are documented in [Plugin Lifecycle → Device Callbacks](plugin-lifecycle.md#device-lifecycle-callbacks).

Key callbacks:
- `deviceStartComm(dev)` - Initialize device communication
- `deviceStopComm(dev)` - Clean up device resources
- `deviceUpdated(origDev, newDev)` - Handle configuration changes

## Configuration Validation

```python
def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
    """
    Validate device configuration before saving

    :return: (is_valid, values_dict, errors_dict)
    """
    errors_dict = indigo.Dict()

    # Validate address
    address = values_dict.get('address', '').strip()
    if not address:
        errors_dict['address'] = "Address is required"

    # Validate polling interval
    try:
        interval = int(values_dict.get('pollingInterval', 60))
        if interval < 10:
            errors_dict['pollingInterval'] = "Minimum interval is 10 seconds"
    except ValueError:
        errors_dict['pollingInterval'] = "Must be a number"

    if len(errors_dict) > 0:
        return (False, values_dict, errors_dict)

    return (True, values_dict)
```

## Dynamic Lists

Populate configuration fields dynamically:

```python
def get_device_list(self, filter="", values_dict=None, type_id="", target_id=0):
    """Return list of available devices for dropdown"""
    device_list = []
    for dev in indigo.devices:
        if dev.id != target_id:  # Don't include self
            device_list.append((dev.id, dev.name))
    return device_list
```

```xml
<Field id="linkedDevice" type="menu">
    <Label>Linked Device:</Label>
    <List class="self" method="get_device_list" dynamicReload="true"/>
</Field>
```

## Device Properties

For complete device class reference including all properties and methods, see [API → IOM → Devices](../api/iom/devices.md).

Common access patterns:

```python
# Plugin-defined properties (from ConfigUI)
address = dev.pluginProps.get('address', '')

# Device states
temp = dev.states['temperature']

# Built-in properties
dev.id              # Unique device ID
dev.name            # Device name
dev.deviceTypeId    # Type ID from Devices.xml
dev.enabled         # Is device enabled?
```

## Best Practices

### State Design
- Use descriptive state IDs: `temperatureSensor1` not `temp1`
- Choose appropriate value types for your data
- Set `UiDisplayStateId` to most important state

### Device Communication
- Initialize connections in `deviceStartComm()`
- Clean up in `deviceStopComm()`
- Handle device offline gracefully

### Configuration
- Provide sensible defaults
- Validate all user input
- Use dynamic lists for device/variable selection

### Performance
- Batch state updates with `updateStatesOnServer()`
- Update states only when values change
- Use `indigo.devices.iter("self")` to iterate only your plugin's devices

## See Also

- [Device Classes Reference](../api/iom/devices.md) - Device properties and methods
- [Plugin Lifecycle](plugin-lifecycle.md) - Lifecycle callbacks
- [Constants Reference](../api/iom/constants.md) - State icons
