# Indigo Plugin Development Skill

Community-maintained Claude Code skill for Indigo home automation plugin development.

## What is This?

This is a Claude Code skill that provides expert assistance for developing [Indigo](https://www.indigodomo.com) home automation plugins. It includes comprehensive documentation, code examples, and best practices maintained by the Indigo developer community.

## Installation

### Option 1: Clone into your project

```bash
cd /path/to/your/indigo/project
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/indigo-community/indigo-skill.git indigo
```

### Option 2: Add as submodule

```bash
cd /path/to/your/indigo/project
mkdir -p .claude/skills
git submodule add https://github.com/indigo-community/indigo-skill.git .claude/skills/indigo
```

### Option 3: Symlink (for multiple projects)

```bash
# Clone once
git clone https://github.com/indigo-community/indigo-skill.git ~/indigo-skill

# Symlink in each project
cd /path/to/your/indigo/project
mkdir -p .claude/skills
ln -s ~/indigo-skill .claude/skills/indigo
```

## Usage

Once installed, invoke the skill in Claude Code:

```
/indigo "How do I create a custom device?"
/indigo "Debug this plugin lifecycle issue"
/indigo "Show me an example of a thermostat plugin"
/indigo "What's the best way to poll an API?"
```

The skill has access to:
- Comprehensive documentation on plugin development
- Code snippets and templates
- Common patterns and best practices
- Troubleshooting guides
- Example implementations

## Documentation

All documentation is organized in the `docs/` directory:

### 📚 [Getting Started](docs/getting-started/)
New to Indigo plugin development? Start here!
- Setting up your development environment
- Creating your first plugin
- Understanding plugin structure
- Testing and debugging

### 🏗️ [Core Concepts](docs/core-concepts/)
Understanding the architecture and lifecycle
- Plugin lifecycle (init, startup, shutdown)
- Device types (custom, relay, dimmer, sensor, thermostat)
- State management
- Concurrent thread patterns

### 📖 [API Reference](docs/api-reference/)
Detailed API documentation
- Plugin base class methods
- Device object properties
- Action callbacks
- UI validation callbacks

### 🎯 [Patterns](docs/patterns/)
Common implementation patterns
- API integration techniques
- Polling strategies
- Error handling approaches
- Configuration UI patterns

### 💡 [Examples](docs/examples/)
Complete working examples
- Custom device implementations
- Relay and dimmer devices
- Thermostat controllers
- Sensor devices
- HTTP responders

### 🔧 [Troubleshooting](docs/troubleshooting/)
Common issues and solutions
- Debugging techniques
- Performance optimization
- Common errors and fixes

## Contributing

We welcome contributions from the Indigo developer community! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### What to contribute:
- 📝 Documentation improvements
- 💻 Code examples and snippets
- 🐛 Troubleshooting guides
- 📚 Best practices
- 🎯 Design patterns

### How to contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b docs/add-device-state-guide`)
3. Make your changes
4. Submit a pull request

## Version Support

- **Current**: Indigo 2023.2+ (Python 3.10+)
- **Legacy**: Indigo 2022.x and earlier (Python 2.7)

This skill focuses on current versions. Version-specific documentation is in the `versions/` directory.

## Community

- 💬 **Discussions**: Ask questions, share tips
- 🐛 **Issues**: Report bugs or request documentation
- 🌐 **Forum**: [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)

## Official Resources

- [Indigo Plugin Developer's Guide](https://www.indigodomo.com/docs/plugin_guide)
- [Indigo Object Model Reference](https://www.indigodomo.com/docs/object_model_reference)
- [Indigo Scripting Tutorial](https://www.indigodomo.com/docs/plugin_scripting_tutorial)

## License

MIT License - See [LICENSE](LICENSE)

## Maintainers

This is a community project. Want to help maintain? Open an issue or discussion!

---

**Made with ❤️ by the Indigo developer community**
