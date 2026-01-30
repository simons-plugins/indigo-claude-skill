# Indigo Plugin Development Documentation

Optimized documentation for building Indigo plugins.

## Start Here

### New to Indigo Plugin Development?

**[Quick Start Guide](quick-start.md)** - Create your first plugin in minutes

## Documentation Structure

| Section | Purpose |
|---------|---------|
| [Concepts](concepts/) | Plugin lifecycle, devices, events, preferences |
| [API Reference](api/) | Indigo Object Model reference |
| [Patterns](patterns/) | Implementation patterns and best practices |
| [Examples](examples/) | SDK example plugin catalog |
| [Troubleshooting](troubleshooting/) | Common issues and solutions |

## Quick Navigation by Use Case

### "How do I create a device?"

1. **Start**: [Concepts → Devices](concepts/devices.md) - Device types, Devices.xml, ConfigUI
2. **API details**: [API → IOM → Devices](api/iom/devices.md) - Device class properties/methods
3. **Example**: [SDK Examples Guide](examples/sdk-examples-guide.md)

### "What device properties/methods exist?"

→ [API → IOM → Devices](api/iom/devices.md)

### "How do I handle device lifecycle?"

→ [Concepts → Plugin Lifecycle](concepts/plugin-lifecycle.md#device-lifecycle-callbacks)

### "How do I update device state?"

→ [Patterns → API Patterns](patterns/api-patterns.md#device-state-updates)

### "How do I save plugin preferences?"

→ [Concepts → Plugin Preferences](concepts/plugin-preferences.md)

### "How do I create custom trigger events?"

→ [Concepts → Custom Events](concepts/events.md)

### "How do I iterate/filter devices?"

→ [API → IOM → Filters](api/iom/filters.md)

### "How does replaceOnServer work?"

→ [API → IOM → Architecture](api/iom/architecture.md)

### "How do I subscribe to changes?"

→ [API → IOM → Subscriptions](api/iom/subscriptions.md)

### "What constants/icons are available?"

→ [API → IOM → Constants](api/iom/constants.md)

## By Device Type

| Device | Example |
|--------|---------|
| Custom device | [Example Device - Custom](examples/sdk-examples-guide.md#example-device---custom) |
| Lights/switches | [Example Device - Relay/Dimmer](examples/sdk-examples-guide.md#example-device---relay-and-dimmer) |
| Thermostat | [Example Device - Thermostat](examples/sdk-examples-guide.md#example-device---thermostat) |
| Sensors | [Example Device - Sensor](examples/sdk-examples-guide.md#example-device---sensor) |
| Web API | [Example HTTP Responder](examples/sdk-examples-guide.md#example-http-responder) |

## For Claude (Context Optimization)

### File Loading Strategy

**Concepts vs API**: These are complementary, not duplicates:
- `concepts/devices.md` → Design (Devices.xml, ConfigUI, validation)
- `api/iom/devices.md` → Reference (class properties, methods)

**Load based on question type**:

| User Question | Load |
|---------------|------|
| "How do I create a device?" | `concepts/devices.md` |
| "What properties does a device have?" | `api/iom/devices.md` |
| "How do I update state?" | `patterns/api-patterns.md` |
| "How do I save settings?" | `concepts/plugin-preferences.md` |
| "How do I create trigger events?" | `concepts/events.md` |
| "Show me an example" | Specific example from `sdk-examples/` |

### Modular IOM Files

The IOM documentation is split into focused files (~4KB each):

| Topic | File |
|-------|------|
| Core architecture | `api/iom/architecture.md` |
| Device classes | `api/iom/devices.md` |
| Trigger classes | `api/iom/triggers.md` |
| Iteration filters | `api/iom/filters.md` |
| Change subscriptions | `api/iom/subscriptions.md` |
| Constants/icons | `api/iom/constants.md` |
| indigo.Dict/List | `api/iom/containers.md` |
| Utility functions | `api/iom/utilities.md` |

### Concept Files

| Topic | File |
|-------|------|
| Plugin lifecycle | `concepts/plugin-lifecycle.md` |
| Device development | `concepts/devices.md` |
| Plugin preferences | `concepts/plugin-preferences.md` |
| Custom events | `concepts/events.md` |

Load only the specific topic needed.

### Never Load All at Once

- `sdk-examples/` - 16 complete plugins (1.3MB) - Load individually
- Don't load all IOM files together - load by topic

## External Resources

- [Official Plugin Guide](https://wiki.indigodomo.com/doku.php?id=indigo_2025.1_documentation:plugin_guide)
- [Object Model Reference](https://wiki.indigodomo.com/doku.php?id=indigo_2025.1_documentation:object_model_reference)
- [Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)

## Version Information

- **Current**: Indigo 2025.1+ (Python 3.10+)
- **Migration**: See [`../reference/Python3-Migration-Guide.md`](../reference/Python3-Migration-Guide.md)
