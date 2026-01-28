# Indigo Plugin Development Documentation

**Streamlined, optimized documentation for building Indigo plugins.**

---

## 🚀 Start Here

### New to Indigo Plugin Development?

**[Quick Start Guide](quick-start.md)** - Create your first plugin in minutes
- Setup and prerequisites
- Hello World plugin walkthrough
- Plugin structure explained
- Common beginner mistakes

---

## 📖 Core Documentation

### [Concepts](concepts/)
**Essential architectural concepts**
- **[Plugin Lifecycle](concepts/plugin-lifecycle.md)** - `__init__()`, `startup()`, `shutdown()`, concurrent threads
- **[Device Development](concepts/devices.md)** - Device types, states, configuration UIs

### [API Reference](api/)
**Complete API documentation**
- **[Indigo Object Model](api/indigo-object-model.md)** - Devices, variables, server objects, constants

### [Examples](examples/)
**16 official SDK example plugins + patterns**
- **[SDK Examples Guide](examples/sdk-examples-guide.md)** - Complete catalog of all examples
- Device types, integrations, hardware protocols

### [Troubleshooting](troubleshooting/)
**Common issues and solutions**
- **[Common Issues](troubleshooting/common-issues.md)** - Debugging guide with solutions

### [Patterns](patterns/)
**Implementation patterns** (coming soon)
- API integration, polling, error handling, configuration UI

---

## 🎯 Quick Navigation

### I want to...

| Task | Go To |
|------|-------|
| Create my first plugin | [Quick Start](quick-start.md) |
| Understand plugin lifecycle | [Concepts → Plugin Lifecycle](concepts/plugin-lifecycle.md) |
| Create devices | [Concepts → Devices](concepts/devices.md) |
| Look up API methods | [API → Indigo Object Model](api/indigo-object-model.md) |
| Find code examples | [Examples → SDK Guide](examples/sdk-examples-guide.md) |
| Debug an error | [Troubleshooting → Common Issues](troubleshooting/common-issues.md) |

### By Device Type

| Device | Example |
|--------|---------|
| Custom device with unique states | [Example Device - Custom](examples/sdk-examples-guide.md#example-device---custom) |
| Lights/switches | [Example Device - Relay/Dimmer](examples/sdk-examples-guide.md#example-device---relay-and-dimmer) |
| Thermostat | [Example Device - Thermostat](examples/sdk-examples-guide.md#example-device---thermostat) |
| Sensors | [Example Device - Sensor](examples/sdk-examples-guide.md#example-device---sensor) |
| Web API/Dashboard | [Example HTTP Responder](examples/sdk-examples-guide.md#example-http-responder) |

---

## 📦 What's Included

- ✅ **Comprehensive guides** - Step-by-step tutorials and references
- ✅ **16 official SDK examples** - Production-quality code in `../sdk-examples/`
- ✅ **API reference** - Complete Indigo Object Model documentation
- ✅ **Troubleshooting** - Common issues and solutions
- ✅ **Code snippets** - Ready-to-use templates in `../snippets/`

---

## 🔍 For Claude (AI Assistant)

**Context optimization guidelines**:

**Load these files (all < 12KB)**:
- `quick-start.md` - Complete getting started guide
- `concepts/plugin-lifecycle.md` - Lifecycle reference
- `concepts/devices.md` - Device development
- `api/indigo-object-model.md` - API reference
- `examples/sdk-examples-guide.md` - Example catalog
- `troubleshooting/common-issues.md` - Troubleshooting

**Never load all at once**:
- `../sdk-examples/` - 16 complete plugins (1.3MB) - Load individually only

**Strategy**:
1. Check `examples/sdk-examples-guide.md` to find relevant example
2. Use Read tool to load ONLY that specific example
3. Don't load multiple examples simultaneously

---

## 📚 External Resources

- [Official Plugin Guide](https://www.indigodomo.com/docs/plugin_guide) - Complete development guide
- [Object Model Reference](https://www.indigodomo.com/docs/object_model_reference) - API reference
- [Scripting Tutorial](https://www.indigodomo.com/docs/plugin_scripting_tutorial) - Learn by examples
- [Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18) - Community support

---

## 🤝 Contributing

This documentation is community-maintained!

Found an issue or want to add documentation?
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines
- Open an issue or pull request
- Join discussions on GitHub

---

## ℹ️ Version Information

- **Current**: Indigo 2023.2+ (Python 3.10+)
- **Legacy**: 2022.x and earlier (Python 2.7, not recommended)

All documentation focuses on current versions. For migration help, see [`../reference/Python3-Migration-Guide.md`](../reference/Python3-Migration-Guide.md).
