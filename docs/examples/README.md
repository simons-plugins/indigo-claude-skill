# Example Plugins and Patterns

Complete working examples and implementation patterns for Indigo plugin development.

## Two Types of Examples

### 1. SDK Example Plugins (Full Working Code)

The skill includes **16 complete, production-quality example plugins** from the official Indigo SDK.

**See**: [SDK Examples Guide](sdk-examples-guide.md) - Complete catalog with descriptions and use cases

These are located in [`../../sdk-examples/`](../../sdk-examples/) and cover:
- **Device Types**: Custom, Relay, Dimmer, Thermostat, Sensor, Speed Control, Sprinkler, Energy Meter
- **Integration**: HTTP Responder, Action API, Custom Broadcaster/Subscriber, Variable Subscriber
- **Hardware**: INSTEON/X10, Z-Wave listeners
- **Advanced**: Database Traverse, Device Factory

**For Claude (AI Assistant)**: Don't load all SDK examples into context. Instead:
1. Reference [sdk-examples-guide.md](sdk-examples-guide.md) to find the relevant example
2. Use Read tool to load only the specific example needed
3. Point users to the example location in `../../sdk-examples/`

### 2. Pattern Documentation (This Directory)

Extracted patterns and best practices from real-world plugins. These are lightweight guides focused on specific implementation patterns rather than complete plugins.

## Quick Reference: Which Example to Use?

| I need to... | Use This Example |
|--------------|------------------|
| Create a custom device with unique states | [Example Device - Custom](sdk-examples-guide.md#example-device---custom) |
| Control lights or switches | [Example Device - Relay and Dimmer](sdk-examples-guide.md#example-device---relay-and-dimmer) |
| Build a thermostat | [Example Device - Thermostat](sdk-examples-guide.md#example-device---thermostat) |
| Create read-only sensors | [Example Device - Sensor](sdk-examples-guide.md#example-device---sensor) |
| Track energy usage | [Example Device - Energy Meter](sdk-examples-guide.md#example-device---energy-meter) |
| Control irrigation zones | [Example Device - Sprinkler](sdk-examples-guide.md#example-device---sprinkler) |
| Build a web API or dashboard | [Example HTTP Responder](sdk-examples-guide.md#example-http-responder) |
| Create plugin actions | [Example Action API](sdk-examples-guide.md#example-action-api) |
| Communicate between plugins | [Example Custom Broadcaster/Subscriber](sdk-examples-guide.md#example-custom-broadcaster) |
| React to variable changes | [Example Variable Change Subscriber](sdk-examples-guide.md#example-variable-change-subscriber) |
| Scan the Indigo database | [Example Database Traverse](sdk-examples-guide.md#example-database-traverse) |

## Pattern Documentation (Coming Soon)

We're building a library of extracted patterns from successful plugins:

### Planned Pattern Docs:
- **API Integration Patterns** - RESTful APIs, OAuth, rate limiting
- **Polling Strategies** - Efficient device polling, backoff algorithms
- **Error Handling** - Robust error recovery, retry logic
- **State Synchronization** - Keeping plugin state in sync with hardware
- **Configuration UI Patterns** - Dynamic lists, validation, user feedback
- **Threading Patterns** - Safe concurrent access, thread coordination
- **Web Dashboard Patterns** - Building responsive web UIs
- **Device Discovery** - Auto-discovering network devices
- **Authentication Patterns** - API keys, tokens, OAuth flows
- **Caching Strategies** - Reducing API calls, cache invalidation

## How to Use These Examples

### For Learning

1. **Browse the Catalog**: Read [sdk-examples-guide.md](sdk-examples-guide.md) to understand what each example demonstrates
2. **Find Similar Example**: Match your use case to the closest example
3. **Study the Code**: Right-click bundle → Show Package Contents → review `plugin.py`
4. **Try It**: Enable the example in Indigo to see it in action

### As a Template

1. **Copy the Example**:
   ```bash
   cp -r "../../sdk-examples/Example Device - Custom.indigoPlugin" MyPlugin.indigoPlugin
   ```

2. **Customize Info.plist**:
   - Change `CFBundleIdentifier` to unique value
   - Update `CFBundleDisplayName`
   - Adjust version numbers

3. **Adapt the Code**:
   - Replace example logic with your integration
   - Modify Devices.xml for your device types
   - Update Actions.xml for your actions

4. **Test**:
   ```bash
   cp -r MyPlugin.indigoPlugin "/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins/"
   ```

### For Reference

Use examples to answer specific questions:
- "How do I handle thermostat setpoints?" → See Thermostat example
- "How do I build a REST API?" → See HTTP Responder example
- "How do I subscribe to variable changes?" → See Variable Change Subscriber

## Contributing Examples

Have a useful pattern or example? We'd love to include it!

**Good pattern documentation includes**:
- Clear problem statement
- Complete working code
- Explanation of key concepts
- When to use this pattern
- Alternatives and tradeoffs
- Common pitfalls

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## Related Documentation

- **[SDK Examples Guide](sdk-examples-guide.md)** - Complete catalog of all 16 SDK examples
- **[Quick Start](../quick-start.md)** - Get a plugin running in minutes
- **[Concepts](../concepts/)** - Core architectural concepts
- **[Patterns](../patterns/)** - Implementation patterns (coming soon)
- **[API Reference](../api/)** - Detailed API documentation

## External Resources

- [Indigo Plugin Forum](https://forums.indigodomo.com/viewforum.php?f=26) - User-contributed plugins
- [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18) - Development discussions
- [Official Plugin Guide](https://www.indigodomo.com/docs/plugin_guide)

## For Claude (AI Assistant)

When helping users find examples:

1. **Check [sdk-examples-guide.md](sdk-examples-guide.md)** first - it has comprehensive descriptions
2. **Match use case to example type** using the quick reference table above
3. **Read specific example code** only when needed - don't load all examples
4. **Reference by name** - e.g., "See Example Device - Thermostat"
5. **Point to specific sections** - e.g., "See the actionControlThermostat() method"

**Context optimization**: The sdk-examples-guide.md is 8KB - safe to reference. The actual example plugins total 1.3MB - only load specific files when needed.
