# Indigo Plugin Development Documentation

Welcome to the comprehensive documentation for Indigo plugin development!

## Documentation Structure

### 📚 [Getting Started](getting-started/)
New to Indigo plugin development? Start here!
- [First Plugin](getting-started/README.md) - Create your first plugin
- Plugin structure and setup
- Development environment
- Testing and debugging basics

### 🏗️ [Core Concepts](core-concepts/)
Understanding the architecture and lifecycle
- [Plugin Lifecycle](core-concepts/plugin-lifecycle.md) - Understanding init, startup, shutdown
- Device types and models
- State management
- Concurrent thread patterns
- Event handling

### 📖 [API Reference](api-reference/)
Detailed API documentation
- Plugin base class methods
- Device object properties and methods
- Action callbacks
- UI validation callbacks
- Indigo constants and enums

### 🎯 [Patterns](patterns/)
Common implementation patterns and best practices
- API integration techniques
- Polling strategies and rate limiting
- Error handling approaches
- Configuration UI patterns
- State synchronization
- Threading patterns

### 💡 [Examples](examples/)
Complete working examples organized by device type
- Custom devices
- Relay and dimmer devices
- Thermostat controllers
- Sensor devices
- HTTP responders
- Complex integrations

### 🔧 [Troubleshooting](troubleshooting/)
Common issues and solutions
- Debugging techniques
- Performance optimization
- Common errors and fixes
- Plugin won't load issues
- State update problems

## Quick Links

### For Beginners
1. [Your First Plugin](getting-started/README.md#your-first-plugin-hello-world)
2. [Plugin Structure](getting-started/README.md#plugin-structure)
3. [Common Mistakes](getting-started/README.md#common-beginner-mistakes)

### For Developers
- [Plugin Lifecycle](core-concepts/plugin-lifecycle.md)
- [Best Practices](patterns/)
- [Code Snippets](../snippets/)

### Need Help?
- [Troubleshooting Guide](troubleshooting/)
- [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)
- [GitHub Discussions](https://github.com/indigo-community/indigo-skill/discussions)

## Contributing

This documentation is community-maintained. Found an issue or want to add documentation? See [CONTRIBUTING.md](../CONTRIBUTING.md)!

## External Resources

- [Official Indigo Plugin Guide](https://www.indigodomo.com/docs/plugin_guide)
- [Indigo Object Model Reference](https://www.indigodomo.com/docs/object_model_reference)
- [Indigo Scripting Tutorial](https://www.indigodomo.com/docs/plugin_scripting_tutorial)
- [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)

---

**Note**: This documentation focuses on Indigo 2023.2+ (Python 3.10+). For legacy versions, see the `versions/` directory.
