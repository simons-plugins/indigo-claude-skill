# Core Concepts

Essential architectural concepts for Indigo plugin development.

## Available Documentation

### [Plugin Lifecycle](plugin-lifecycle.md)
Complete guide to plugin initialization, startup, execution, and shutdown.

**Topics covered**:
- Lifecycle methods: `__init__()`, `startup()`, `runConcurrentThread()`, `shutdown()`
- Device lifecycle callbacks
- Sleep/wake handling
- Common patterns and mistakes
- Resource management best practices

**Start here if**: You're creating a new plugin or debugging lifecycle issues

### [Device Development](devices.md)
Comprehensive guide to creating and managing plugin devices.

**Topics covered**:
- Device types (relay, dimmer, sensor, thermostat, custom, etc.)
- Device XML definition
- State management and updates
- Configuration UIs
- Validation callbacks
- Dynamic lists

**Start here if**: You need to create devices or manage device states

## Coming Soon

Documentation planned for this section:

- **State Management** - Deep dive into device state patterns and performance
- **Concurrent Threading** - Advanced background task patterns and thread safety
- **Event System** - Subscribing to and handling Indigo events
- **Action System** - Creating and handling custom actions
- **Variable System** - Working with Indigo variables
- **Trigger System** - Creating custom trigger types
- **Plugin Communication** - Broadcasting and subscribing between plugins

## Quick Reference

### When to use each concept:

| Task | Read This |
|------|-----------|
| Creating first plugin | [Plugin Lifecycle](plugin-lifecycle.md) |
| Plugin won't start | [Plugin Lifecycle](plugin-lifecycle.md) → Debugging |
| Plugin won't stop | [Plugin Lifecycle](plugin-lifecycle.md) → Common Mistakes |
| Creating devices | [Device Development](devices.md) |
| Updating device states | [Device Development](devices.md) → Updating Device States |
| Validating config | [Device Development](devices.md) → Configuration Validation |
| Polling APIs | [Plugin Lifecycle](plugin-lifecycle.md) → runConcurrentThread() |

## Related Documentation

- **[Quick Start](../quick-start.md)** - Get a plugin running in minutes
- **[API Reference](../api/)** - Detailed API documentation
- **[Patterns](../patterns/)** - Reusable implementation patterns
- **[Examples](../examples/)** - Complete working examples

## External Resources

- [Official Plugin Developer's Guide](https://www.indigodomo.com/docs/plugin_guide)
- [Indigo Object Model Reference](https://www.indigodomo.com/docs/object_model_reference)
- [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)

## Contributing

Want to add documentation to this section? See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

**Valuable topics include**:
- State update performance patterns
- Thread safety with concurrent access
- Communication between plugins
- Working with server scripts
- Memory management best practices
