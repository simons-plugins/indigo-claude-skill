# Official Indigo SDK Examples

This directory contains the complete set of official example plugins from the Indigo SDK (version 2025.1).

These are working, production-quality examples that demonstrate best practices for different types of plugins.

## Device Type Examples

### Core Device Types

#### [Example Device - Custom](Example%20Device%20-%20Custom.indigoPlugin/)
**Use for**: General-purpose devices with custom states

The most flexible device type. Use this when you need:
- Custom state names and types
- Device-specific properties
- Full control over device behavior

**Key concepts demonstrated**:
- Custom state definitions in Devices.xml
- State updates with `updateStatesOnServer()`
- Device property management
- Custom UI fields

#### [Example Device - Relay and Dimmer](Example%20Device%20-%20Relay%20and%20Dimmer.indigoPlugin/)
**Use for**: On/off and dimmable devices (lights, switches, outlets)

Demonstrates standard relay (on/off) and dimmer (brightness) devices.

**Key concepts demonstrated**:
- `indigo.kDeviceTypeId.Relay` device type
- `indigo.kDeviceTypeId.Dimmer` device type
- `actionControlDevice()` for on/off/dim actions
- Brightness control (0-100)
- Status request handling

#### [Example Device - Thermostat](Example%20Device%20-%20Thermostat.indigoPlugin/)
**Use for**: Climate control, HVAC systems

Full thermostat implementation with heating/cooling modes.

**Key concepts demonstrated**:
- `indigo.kDeviceTypeId.Thermostat` device type
- Temperature setpoints (heat, cool)
- HVAC modes (off, heat, cool, auto)
- Fan control
- Temperature display and units
- `actionControlThermostat()` callback

#### [Example Device - Sensor](Example%20Device%20-%20Sensor.indigoPlugin/)
**Use for**: Read-only monitoring devices (temperature, humidity, motion)

Demonstrates sensor devices that report values but don't accept commands.

**Key concepts demonstrated**:
- `indigo.kDeviceTypeId.Sensor` device type
- Read-only state updates
- Sensor value types
- Display in Indigo UI
- Periodic polling patterns

#### [Example Device - Speed Control](Example%20Device%20-%20Speed%20Control.indigoPlugin/)
**Use for**: Variable speed devices (fans, motor controls)

Speed control device with variable speed settings.

**Key concepts demonstrated**:
- `indigo.kDeviceTypeId.SpeedControl` device type
- Speed levels (0-100%)
- Speed presets
- `actionControlSpeedControl()` callback

#### [Example Device - Sprinkler](Example%20Device%20-%20Sprinkler.indigoPlugin/)
**Use for**: Irrigation systems, multi-zone controllers

Multi-zone sprinkler controller.

**Key concepts demonstrated**:
- `indigo.kDeviceTypeId.Sprinkler` device type
- Zone management
- Zone scheduling
- Run times and durations
- `actionControlSprinkler()` callback

#### [Example Device - Energy Meter](Example%20Device%20-%20Energy%20Meter.indigoPlugin/)
**Use for**: Energy monitoring, power measurement

Energy meter device for tracking power consumption.

**Key concepts demonstrated**:
- Energy/power accumulation
- Real-time power readings
- Total energy consumed
- Cost calculations
- Time-series data

### Special Purpose Examples

#### [Example Device - Factory](Example%20Device%20-%20Factory.indigoPlugin/)
**Use for**: Dynamic device creation, device templates

Demonstrates programmatic device creation and management.

**Key concepts demonstrated**:
- Creating devices from plugin code
- Device templates
- Dynamic device lists
- Device configuration UI generation

## Integration & Communication Examples

### [Example HTTP Responder](Example%20HTTP%20Responder.indigoPlugin/)
**Use for**: Web interfaces, REST APIs, dashboards

Creates a web server within your plugin to serve web pages and APIs.

**Key concepts demonstrated**:
- Built-in HTTP server
- Serving static files from Resources/
- Dynamic content generation
- RESTful API endpoints
- JSON responses
- Control panel/dashboard creation

### [Example Action API](Example%20Action%20API.indigoPlugin/)
**Use for**: Complex actions, custom commands

Demonstrates the Action API for creating custom actions.

**Key concepts demonstrated**:
- Action definitions in Actions.xml
- Action callbacks
- Action parameters
- Action validation
- Concurrent action execution

### [Example Custom Broadcaster](Example%20Custom%20Broadcaster.indigoPlugin/)
**Use for**: Plugin-to-plugin communication

Broadcasts custom messages that other plugins can subscribe to.

**Key concepts demonstrated**:
- Broadcasting custom messages
- Message payload structure
- Broadcast timing
- Communication patterns

### [Example Custom Subscriber](Example%20Custom%20Subscriber.indigoPlugin/)
**Use for**: Listening to other plugins

Subscribes to and handles messages from broadcaster plugins.

**Key concepts demonstrated**:
- Subscribing to broadcasts
- Message handling
- Filtering messages
- Response actions

### [Example Variable Change Subscriber](Example%20Variable%20Change%20Subscriber.indigoPlugin/)
**Use for**: Monitoring Indigo variables

Monitors Indigo variables and responds to changes.

**Key concepts demonstrated**:
- `indigo.variables.subscribeToChanges()`
- `variableUpdated()` callback
- Variable value access
- Triggered actions on variable changes

### [Example Database Traverse](Example%20Database%20Traverse.indigoPlugin/)
**Use for**: Accessing Indigo's database, reporting

Demonstrates traversing and querying Indigo's internal database.

**Key concepts demonstrated**:
- Database access patterns
- Iterating devices
- Iterating variables
- Iterating action groups
- Data collection and reporting

## Hardware Integration Examples

### [Example INSTEON:X10 Listener](Example%20INSTEON:X10%20Listener.indigoPlugin/)
**Use for**: INSTEON/X10 device integration

Listens for INSTEON and X10 protocol messages.

**Key concepts demonstrated**:
- INSTEON message listening
- X10 protocol handling
- Device address parsing
- Raw message processing

### [Example ZWave Listener](Example%20ZWave%20Listener.indigoPlugin/)
**Use for**: Z-Wave device integration

Listens for Z-Wave protocol messages.

**Key concepts demonstrated**:
- Z-Wave message listening
- Node ID handling
- Command class parsing
- Z-Wave event processing

## How to Use These Examples

### 1. Study the Code

Each example is a complete, working plugin you can install and test:

```bash
# Copy to Indigo plugins folder
cp -r "Example Device - Custom.indigoPlugin" \
  "/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins/"
```

Then enable in Indigo: **Plugins → Manage Plugins**

### 2. Use as Templates

Copy an example as a starting point for your plugin:

```bash
# Copy example to your workspace
cp -r "Example Device - Custom.indigoPlugin" "MyPlugin.indigoPlugin"

# Edit Info.plist to change CFBundleIdentifier
# Edit plugin.py with your logic
```

### 3. Reference Implementation

Study how the examples solve common problems:
- Configuration UI patterns
- State management
- Error handling
- API callbacks
- Threading

### 4. Compare Approaches

Multiple examples may solve similar problems differently. Compare approaches to understand trade-offs.

## Example Structure

Each example plugin follows this structure:

```
Example.indigoPlugin/
└── Contents/
    ├── Info.plist                 # Plugin metadata
    ├── Server Plugin/
    │   ├── plugin.py              # Main plugin class
    │   ├── Devices.xml            # Device definitions
    │   ├── Actions.xml            # Action definitions (if applicable)
    │   ├── Events.xml             # Event/trigger definitions (if applicable)
    │   ├── MenuItems.xml          # Menu items (if applicable)
    │   └── PluginConfig.xml       # Plugin config UI (if applicable)
    └── Resources/                  # Web content (HTTP Responder example)
```

## SDK Version

These examples are from **Indigo SDK 2025.1** and are designed for:
- **Indigo 2023.2+**
- **Python 3.10+**
- **ServerApiVersion 3.0**

For older Indigo versions (Python 2.7), see the reference folder for migration guides.

## Additional Resources

- **[Official Plugin Guide](https://www.indigodomo.com/docs/plugin_guide)**
- **[Object Model Reference](https://www.indigodomo.com/docs/object_model_reference)**
- **[SDK Documentation](../docs/sdk/)** - Organized guides and references
- **[Python 3 Migration Guide](../reference/Python3-Migration-Guide.md)**

## Getting Help

- 📚 Check the [SDK Documentation](../docs/sdk/)
- 💬 Ask in [GitHub Discussions](https://github.com/indigo-community/indigo-skill/discussions)
- 🌐 Visit [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)

## Contributing

Found an issue or improvement in these examples?
1. Check if it's a documentation issue (we can fix)
2. Or report to Indigo's official SDK repository

These are copies of official Indigo SDK examples for convenience and reference.
