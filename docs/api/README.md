# API Reference

Reference documentation for the Indigo Plugin API.

## Indigo Object Model (IOM)

The IOM provides Python access to all Indigo objects. Start with the [overview](indigo-object-model.md), then dive into specific topics:

| Topic | Description |
|-------|-------------|
| [Overview & Quick Reference](indigo-object-model.md) | Index and common patterns |
| [Architecture](iom/architecture.md) | Client-server model, replaceOnServer pattern |
| [Command Namespaces](iom/command-namespaces.md) | indigo.dimmer.*, indigo.relay.*, etc. |
| [Device Classes](iom/devices.md) | DimmerDevice, SensorDevice, ThermostatDevice, etc. |
| [Trigger Classes](iom/triggers.md) | Trigger types and plugin events |
| [Containers](iom/containers.md) | indigo.Dict and indigo.List behavior |
| [Filters](iom/filters.md) | Device/trigger iteration filters |
| [Subscriptions](iom/subscriptions.md) | Change callbacks and low-level events |
| [Constants](iom/constants.md) | Icons, actions, protocols, modes |
| [Utilities](iom/utilities.md) | Helper functions and classes |

## Quick Task Lookup

| Task | Documentation |
|------|---------------|
| Turn on/off devices | [Command Namespaces](iom/command-namespaces.md) |
| Update device states | [Device Classes](iom/devices.md#device-methods) |
| Iterate specific device types | [Filters](iom/filters.md#device-filters) |
| Subscribe to device changes | [Subscriptions](iom/subscriptions.md) |
| Modify object properties | [Architecture](iom/architecture.md#replaceOnServer-pattern) |
| Handle nested indigo.Dict | [Containers](iom/containers.md#critical-copy-semantics) |
| Serve static files | [Utilities](iom/utilities.md#return_static_file) |
| State icon reference | [Constants](iom/constants.md#state-image-icons) |

## Related Documentation

| Topic | Location |
|-------|----------|
| Plugin structure and lifecycle | [Concepts](../concepts/) |
| Device configuration UI | [Concepts → Devices](../concepts/devices.md) |
| Implementation patterns | [Patterns](../patterns/) |
| Working examples | [Examples](../examples/) |
| SDK example plugins | [sdk-examples/](../../sdk-examples/) |

## External References

- [Official Object Model Reference](https://wiki.indigodomo.com/doku.php?id=indigo_2025.1_documentation:object_model_reference)
- [Plugin Developer's Guide](https://wiki.indigodomo.com/doku.php?id=indigo_2025.1_documentation:plugin_guide)
