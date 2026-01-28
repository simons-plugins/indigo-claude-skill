# Plugin Examples

Complete, working plugin examples demonstrating various device types and integration patterns.

## Example Categories

### Device Type Examples

Examples showing how to implement different Indigo device types:

- **Custom Devices** - General-purpose devices with custom states
- **Relay Devices** - On/off devices (switches, outlets, etc.)
- **Dimmer Devices** - Brightness-controllable devices (lights, etc.)
- **Thermostat Devices** - Temperature control devices
- **Sensor Devices** - Read-only devices (temperature, humidity, motion, etc.)
- **Speed Control Devices** - Variable speed devices (fans, etc.)

### Integration Examples

Examples demonstrating integration patterns:

- **REST API Integration** - Polling and controlling REST APIs
- **WebSocket Integration** - Real-time communication
- **MQTT Integration** - Message queue patterns
- **Local Device Integration** - Serial, USB, network devices
- **Cloud Service Integration** - Third-party cloud platforms

### Advanced Examples

Complex scenarios and advanced techniques:

- **Multi-device Plugins** - Managing multiple device types
- **HTTP Responder** - Creating web interfaces
- **Custom Triggers** - Creating custom event triggers
- **Data Visualization** - Charts and graphs in Resources/
- **Complex State Management** - Multiple dependent devices

## Example Structure

Each example should include:

```
example-name/
├── README.md                    # Overview and setup instructions
├── ExamplePlugin.indigoPlugin/  # Complete, working plugin
│   └── Contents/
│       ├── Info.plist
│       └── Server Plugin/
│           ├── plugin.py
│           ├── Devices.xml
│           ├── Actions.xml
│           └── ...
├── screenshots/                 # Screenshots of the plugin in action
└── notes.md                     # Implementation notes and lessons learned
```

## Contributing Examples

Examples are incredibly valuable for the community! To contribute:

1. Create a complete, working plugin
2. Test thoroughly in Indigo
3. Document setup and configuration
4. Include screenshots
5. Explain key implementation decisions
6. Follow [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Planned Examples

Vote on or claim examples you'd like to see or contribute:

- [ ] Simple REST API polling (weather, status, etc.)
- [ ] OAuth authentication flow
- [ ] WebSocket real-time updates
- [ ] Serial device communication
- [ ] Local network device discovery
- [ ] Database integration
- [ ] Email/notification integration
- [ ] File monitoring
- [ ] Custom scheduling
- [ ] Device grouping/scenes

## External Examples

Until more examples are added here, check out:

- [Indigo SDK Examples](https://www.indigodomo.com/pluginstore/sdk-examples/)
- [Plugin Store](https://www.indigodomo.com/pluginstore/)
- [Forum examples](https://forums.indigodomo.com/viewforum.php?f=18)
