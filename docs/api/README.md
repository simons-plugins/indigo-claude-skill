# API Reference

Detailed reference documentation for the Indigo Plugin API.

## Available Documentation

### [Indigo Object Model](indigo-object-model.md)
Complete reference for the Indigo Object Model (IOM) - the Python API for accessing Indigo objects.

**Topics covered**:
- Core collections (devices, variables, triggers, actions, schedules)
- Device object properties and methods
- Variable object and management
- Server object and utilities
- Constants (state icons, device actions, protocols)
- Subscriptions and change callbacks

**Use when**: Looking up specific API methods, constants, or object properties

## Quick Lookups

### Common API Tasks

| Task | See |
|------|-----|
| Access device by ID/name | [Indigo Object Model → Devices](indigo-object-model.md#devices) |
| Update device states | [Indigo Object Model → Device Methods](indigo-object-model.md#device-methods) |
| Access variables | [Indigo Object Model → Variables](indigo-object-model.md#variables) |
| Subscribe to changes | [Indigo Object Model → Subscriptions](indigo-object-model.md#subscriptions) |
| State icons reference | [Indigo Object Model → State Icons](indigo-object-model.md#state-icons) |
| Device action constants | [Indigo Object Model → Device Actions](indigo-object-model.md#device-actions) |

### Validation and Configuration

These topics are covered in the [Concepts](../concepts/) section:

- **Device configuration validation**: See [Concepts → Devices → Configuration Validation](../concepts/devices.md#configuration-validation)
- **Dynamic lists**: See [Concepts → Devices → Dynamic Lists](../concepts/devices.md#dynamic-lists)
- **Plugin configuration UI**: See [Concepts → Devices → Configuration UI](../concepts/devices.md#configuration-ui)

## Documentation Roadmap

We're actively expanding API documentation. Planned additions:

### Plugin Base Class
- Complete method signatures and parameters
- Lifecycle method reference
- Action handling methods
- Validation callback reference
- Logging methods (`self.logger`)

### XML Configuration Reference
- Devices.xml complete reference
- Actions.xml schema
- Events.xml schema
- MenuItems.xml patterns
- PluginConfig.xml reference

### Advanced Topics
- Threading and concurrency patterns
- Database access patterns
- Performance optimization
- Memory management

## External References

### Official Documentation

- **[Object Model Reference](https://www.indigodomo.com/docs/object_model_reference)** - Complete official API reference
- **[Plugin Guide](https://www.indigodomo.com/docs/plugin_guide)** - Plugin development guide with API examples

### Related Skill Documentation

- [Quick Start](../quick-start.md) - Get started building plugins
- [Concepts](../concepts/) - Core architectural concepts
- [Patterns](../patterns/) - Implementation patterns and best practices
- [Examples](../examples/) - Working code examples

## Usage Tips

### For Claude (AI Assistant)

When helping users with API questions:

1. **Check [indigo-object-model.md](indigo-object-model.md) first** for constants, object properties, and core API methods
2. **Reference official docs** for detailed specifications
3. **Show code examples** from the skill's example plugins
4. **Link to patterns** for complex integrations

### For Developers

1. **Bookmark the official Object Model Reference** - It's comprehensive and authoritative
2. **Use this skill's API docs** for quick lookups and code examples
3. **Check [Concepts](../concepts/)** for understanding how APIs fit together
4. **See [Patterns](../patterns/)** for best practices using the APIs

## Contributing

This is a high-priority documentation area! Contributions welcome for:

- Method signatures with parameter descriptions
- Return value documentation
- Code examples for API calls
- Common usage patterns
- Edge cases and gotchas
- Performance tips

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## Example: Quick API Reference

### Accessing Devices

```python
# By ID
dev = indigo.devices[123456]

# By name
dev = indigo.devices["Living Room Lamp"]

# Iterate plugin's devices only
for dev in indigo.devices.iter("self"):
    print(dev.name)
```

### Updating States

```python
# Single state
dev.updateStateOnServer('temperature', value=72.5)

# Multiple states (more efficient)
dev.updateStatesOnServer([
    {'key': 'temperature', 'value': 72.5},
    {'key': 'humidity', 'value': 45.2},
    {'key': 'status', 'value': 'online'}
])
```

### Setting Icons

```python
dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
dev.updateStateImageOnServer(indigo.kStateImageSel.PowerOff)
dev.updateStateImageOnServer(indigo.kStateImageSel.Error)
```

For complete examples, see [indigo-object-model.md](indigo-object-model.md).
