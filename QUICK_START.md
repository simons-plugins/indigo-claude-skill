# Quick Start Guide

Get started with the Indigo Plugin Development Skill in 5 minutes!

## Installation

### Option 1: Using the Install Script (Recommended)

```bash
# Download and run the installer
curl -fsSL https://raw.githubusercontent.com/simons-plugins/indigo-claude-skill/main/install.sh | bash
```

### Option 2: Manual Clone

```bash
cd /path/to/your/indigo/project
mkdir -p .claude/skills
git clone https://github.com/simons-plugins/indigo-claude-skill.git .claude/skills/indigo
```

### Option 3: Git Submodule

```bash
cd /path/to/your/indigo/project
mkdir -p .claude/skills
git submodule add https://github.com/simons-plugins/indigo-claude-skill.git .claude/skills/indigo
```

## Verify Installation

In Claude Code, try:

```
/indigo "Hello! Are you working?"
```

If the skill is installed correctly, Claude will respond with Indigo-specific knowledge and guidance.

## Basic Usage

### Getting Help

```
/indigo "How do I create a new plugin?"
/indigo "Explain the plugin lifecycle"
/indigo "Show me device type examples"
```

### Debugging

```
/indigo "My plugin won't load, help me debug"
/indigo "Device states aren't updating"
/indigo "Why is my concurrent thread crashing?"
```

### Code Examples

```
/indigo "Show me how to poll an API"
/indigo "Give me a validation callback example"
/indigo "How do I update device states efficiently?"
```

### Best Practices

```
/indigo "What are the best practices for API integration?"
/indigo "How should I handle errors in my plugin?"
/indigo "What's the correct way to use threading?"
```

## Example Interactions

### Creating Your First Plugin

**You**: `/indigo "I want to create a plugin that integrates with a REST API that returns weather data. How do I start?"`

**Claude**: Will provide:
- Starter template
- API integration patterns
- Polling recommendations
- Device state mapping
- Complete example code

### Debugging an Issue

**You**: `/indigo "My plugin loads but the concurrent thread keeps crashing. Here's the error: [paste error]"`

**Claude**: Will help:
- Diagnose the error
- Identify the root cause
- Provide corrected code
- Suggest debugging techniques
- Recommend best practices

### Understanding Concepts

**You**: `/indigo "Explain how device state management works"`

**Claude**: Will explain:
- What device states are
- How to define states
- How to update states
- Performance considerations
- Code examples

## What the Skill Knows

The skill has access to:

### ✅ Documentation
- Plugin development guides
- API references
- Core concepts
- Best practices

### ✅ Code Examples
- Complete plugin templates
- Common patterns
- Integration examples
- Device type examples

### ✅ Troubleshooting
- Common issues and solutions
- Debugging techniques
- Performance optimization
- Error handling

### ✅ Best Practices
- API integration
- Threading patterns
- State management
- Configuration UI
- Error handling

## Tips for Best Results

### Be Specific

❌ "Help with my plugin"
✅ "My thermostat plugin isn't updating temperature states after API calls"

### Provide Context

```
/indigo "I'm creating a sensor device that reads temperature from a REST API. The API returns JSON like {"temp": 72.5, "humidity": 45}. How do I map this to Indigo states?"
```

### Ask Follow-up Questions

```
/indigo "Can you explain that state update pattern in more detail?"
/indigo "Show me how to add error handling to that example"
/indigo "What if the API returns an array instead?"
```

### Share Code for Review

```
/indigo "Review this plugin code for best practices: [paste code]"
/indigo "Is this the right way to handle API timeouts? [paste code]"
```

## Common Use Cases

### 1. Starting a New Plugin

```
/indigo "Create a plugin template for a custom device that monitors a REST API"
```

### 2. Adding Features

```
/indigo "How do I add action callbacks to my plugin?"
/indigo "Show me how to create a configuration UI"
```

### 3. Debugging

```
/indigo "My plugin crashes with this error: [error message]"
/indigo "Why aren't my device states updating?"
```

### 4. Learning

```
/indigo "Explain the difference between deviceStartComm and startup"
/indigo "When should I use runConcurrentThread vs actions?"
```

### 5. Code Review

```
/indigo "Review this code and suggest improvements: [code]"
/indigo "Is there a better way to structure this? [code]"
```

## Exploring the Documentation

You can also read the documentation directly:

```
.claude/skills/indigo/docs/
├── getting-started/         # New to Indigo development
├── core-concepts/           # Architecture and lifecycle
├── api-reference/           # API documentation
├── patterns/                # Common patterns
├── examples/                # Working examples
└── troubleshooting/         # Common issues
```

Or ask Claude to read specific docs:

```
/indigo "Read the plugin lifecycle documentation and explain it"
/indigo "Show me the examples in docs/examples/"
```

## Getting Updates

### For Clone Installation

```bash
cd .claude/skills/indigo
git pull origin main
```

### For Submodule Installation

```bash
git submodule update --remote .claude/skills/indigo
```

### For Symlink Installation

```bash
cd ~/path/to/original/clone
git pull origin main
```

## Contributing

Found the skill helpful? Consider contributing:

1. **Report Issues**: Found incorrect info? [Open an issue](https://github.com/simons-plugins/indigo-claude-skill/issues)
2. **Add Documentation**: See [CONTRIBUTING.md](CONTRIBUTING.md)
3. **Share Examples**: Your plugin could help others!
4. **Improve Docs**: Fix typos, clarify explanations

## Need More Help?

- 📚 Read the full [README](README.md)
- 📖 Browse [Documentation](docs/README.md)
- 💬 Join [Discussions](https://github.com/simons-plugins/indigo-claude-skill/discussions)
- 🐛 Report [Issues](https://github.com/simons-plugins/indigo-claude-skill/issues)
- 🌐 Visit [Indigo Forum](https://forums.indigodomo.com/viewforum.php?f=18)

---

Happy plugin development! 🚀
