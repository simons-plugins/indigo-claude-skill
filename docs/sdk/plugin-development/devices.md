# Device Development

**Official Documentation**: https://www.indigodomo.com/docs/plugin_guide#devices

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

**Example**: [../IndigoSDK-2025.1/Example Device - Relay and Dimmer.indigoPlugin](../IndigoSDK-2025.1/Example%20Device%20-%20Relay%20and%20Dimmer.indigoPlugin)

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

**Example**: [../IndigoSDK-2025.1/Example Device - Custom.indigoPlugin](../IndigoSDK-2025.1/Example%20Device%20-%20Custom.indigoPlugin)

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
    <State id="separator1">
        <ValueType>Separator</ValueType>
    </State>
</States>
```

**Value Types**:
- `Integer` - Whole numbers
- `Number` - Floating point
- `String` - Text
- `Boolean` - True/False
- `Separator` - Visual separator in UI

### Configuration UI

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

**Field Types**:
- `textfield` - Single line text
- `textarea` - Multi-line text
- `checkbox` - Boolean checkbox
- `menu` - Dropdown menu
- `list` - Selection list
- `button` - Action button
- `label` - Static text/instructions
- `separator` - Visual divider

## Device Lifecycle Callbacks

### Device Creation/Start

```python
def deviceStartComm(self, dev):
    """
    Called when device communication should start:
    - When device is created
    - When device is enabled
    - When plugin starts and device is enabled
    """
    self.logger.debug(f"Starting device: {dev.name}")

    # Refresh state list if Devices.xml changed
    dev.stateListOrDisplayStateIdChanged()

    # Initialize hardware connection
    address = dev.pluginProps.get('address', '')
    self.connect_to_device(address)

    # Set initial state
    dev.updateStateOnServer('status', value='initializing')
```

### Device Stop

```python
def deviceStopComm(self, dev):
    """
    Called when device communication should stop:
    - When device is disabled
    - When device is deleted
    - When plugin is shutting down
    """
    self.logger.debug(f"Stopping device: {dev.name}")

    # Clean up device-specific resources
    self.disconnect_from_device(dev)

    # Clear states if desired
    dev.updateStateOnServer('status', value='offline')
```

### Device Updates

```python
def deviceCreated(self, dev):
    """Called when a new device is created"""
    self.logger.debug(f"Device created: {dev.name}")

def deviceUpdated(self, orig_dev, new_dev):
    """
    Called when device configuration changes

    :param orig_dev: Device before changes
    :param new_dev: Device after changes
    """
    self.logger.debug(f"Device updated: {new_dev.name}")

    # Check if critical config changed
    if orig_dev.pluginProps['address'] != new_dev.pluginProps['address']:
        # Reconnect to new address
        self.reconnect_device(new_dev)

def deviceDeleted(self, dev):
    """Called when device is deleted"""
    self.logger.debug(f"Device deleted: {dev.name}")
    # Clean up any persistent data
```

## Updating Device States

### Single State Update

```python
dev.updateStateOnServer('temperature', value=72.5)
dev.updateStateOnServer('status', value='online')
dev.updateStateOnServer('isOnline', value=True)
```

### Multiple States (More Efficient)

```python
key_value_list = [
    {'key': 'temperature', 'value': 72.5, 'decimalPlaces': 1},
    {'key': 'humidity', 'value': 45.2, 'decimalPlaces': 1},
    {'key': 'status', 'value': 'online'},
    {'key': 'lastUpdate', 'value': str(datetime.now())}
]
dev.updateStatesOnServer(key_value_list)
```

### UI Error States

```python
# Set error state with message
dev.setErrorStateOnServer("Connection failed")

# Clear error state
dev.setErrorStateOnServer(None)
```

### State Icons

```python
# Common state icons
dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
dev.updateStateImageOnServer(indigo.kStateImageSel.TimerOn)
dev.updateStateImageOnServer(indigo.kStateImageSel.PowerOn)
dev.updateStateImageOnServer(indigo.kStateImageSel.PowerOff)
dev.updateStateImageOnServer(indigo.kStateImageSel.Error)

# No icon (Python 3)
dev.updateStateImageOnServer(indigo.kStateImageSel.NoImage)
```

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
    elif not self.is_valid_address(address):
        errors_dict['address'] = "Invalid address format"

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
    """
    Return list of available devices for dropdown

    :return: List of tuples (value, display_name)
    """
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

## Accessing Device Properties

```python
# Plugin-defined properties (from ConfigUI)
address = dev.pluginProps.get('address', '')
interval = dev.pluginProps.get('pollingInterval', 60)

# Device states
temp = dev.states['temperature']
status = dev.states.get('status', 'unknown')

# Built-in properties
dev.id              # Unique device ID
dev.name            # Device name
dev.deviceTypeId    # Type ID from Devices.xml
dev.enabled         # Is device enabled?
dev.configured      # Is device configured?
dev.description     # Device description
```

## Best Practices

### State Design
- Use descriptive state IDs: `temperatureSensor1` not `temp1`
- Choose appropriate value types for your data
- Use separators to group related states
- Set `UiDisplayStateId` to most important state

### Device Communication
- Initialize connections in `deviceStartComm()`
- Clean up in `deviceStopComm()`
- Handle device offline gracefully
- Update states only when values change to reduce database writes

### Configuration
- Provide sensible defaults
- Validate all user input
- Give helpful error messages
- Use dynamic lists for device/variable selection

### Performance
- Batch state updates when possible
- Don't poll devices too frequently
- Cache device references if accessed frequently
- Use `indigo.devices.iter("self")` to iterate only your plugin's devices

## Example Plugins

- **Simple Custom Device**: [../IndigoSDK-2025.1/Example Device - Custom.indigoPlugin](../IndigoSDK-2025.1/Example%20Device%20-%20Custom.indigoPlugin)
- **Relay/Dimmer**: [../IndigoSDK-2025.1/Example Device - Relay and Dimmer.indigoPlugin](../IndigoSDK-2025.1/Example%20Device%20-%20Relay%20and%20Dimmer.indigoPlugin)
- **Thermostat**: [../IndigoSDK-2025.1/Example Device - Thermostat.indigoPlugin](../IndigoSDK-2025.1/Example%20Device%20-%20Thermostat.indigoPlugin)
- **Sensor**: [../IndigoSDK-2025.1/Example Device - Sensor.indigoPlugin](../IndigoSDK-2025.1/Example%20Device%20-%20Sensor.indigoPlugin)

## Official References

- [Plugin Developer's Guide - Devices](https://www.indigodomo.com/docs/plugin_guide#devices)
- [Plugin Developer's Guide - Device XML](https://www.indigodomo.com/docs/plugin_guide#devices_xml)
- [Object Model Reference - Device Class](https://www.indigodomo.com/docs/object_model_reference#device)
