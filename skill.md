# Indigo Plugin Development Expert

**Repository**: https://github.com/simons-plugins/indigo-claude-skill
**Version**: 2025.1
**Slash command**: `/indigo`

## Description

Community-maintained expert assistant for Indigo home automation plugin development. Provides comprehensive guidance with official SDK examples and optimized context usage.

## CRITICAL: Context Optimization Strategy

**DO NOT load all files.** This skill contains 1.3MB of SDK examples. Use Read tool selectively:

✅ **Safe to load** (small files):
- `docs/quick-start.md` (9KB) - Getting started guide
- `docs/concepts/plugin-lifecycle.md` (12KB) - Lifecycle reference
- `docs/concepts/devices.md` (11KB) - Device development
- `docs/api/indigo-object-model.md` (9KB) - API reference
- `docs/examples/sdk-examples-guide.md` (8KB) - Example catalog
- `docs/troubleshooting/common-issues.md` (11KB) - Troubleshooting

❌ **NEVER load all at once**:
- `sdk-examples/` - 16 complete plugins (1.3MB total) - Load ONLY specific example when needed

## Query Routing Guide

Route user questions efficiently using Read tool:

### 1. "Create a plugin" / "Getting started"
```
1. Read docs/quick-start.md
2. Read snippets/plugin-base-template.py
3. If specific device type: Read docs/examples/sdk-examples-guide.md to find example
4. Read ONLY that specific SDK example if needed
```

### 2. "Debug error" / "Plugin not working"
```
1. Read docs/troubleshooting/common-issues.md
2. Match error to solution
3. If lifecycle issue: Read docs/concepts/plugin-lifecycle.md
```

### 3. "How do I [API task]?"
```
1. Read docs/api/indigo-object-model.md
2. Show code example from doc
```

### 4. "Show me an example"
```
1. Read docs/examples/sdk-examples-guide.md (catalog)
2. Find matching example
3. Read ONLY that specific example's code
```

### 5. "Explain [concept]"
```
1. Read appropriate docs/concepts/ file
2. Explain with examples
```

## Workflow: Creating Plugins

**User**: "Create a thermostat plugin"

1. ✅ Read `docs/quick-start.md` - Setup and structure
2. ✅ Read `docs/examples/sdk-examples-guide.md` - Find thermostat example
3. ✅ Read `sdk-examples/Example Device - Thermostat.indigoPlugin/.../plugin.py` - Specific code
4. ✅ Generate custom code based on pattern
5. ❌ Don't load all 16 examples

## Workflow: Debugging

**User**: "Plugin crashes on startup"

1. ✅ Read `docs/troubleshooting/common-issues.md#plugin-crashes-on-startup`
2. ✅ Check common causes (API in __init__, missing super())
3. ✅ If needed: Read `docs/concepts/plugin-lifecycle.md`
4. ❌ Don't load examples unless relevant

## Documentation Structure

**Optimized for selective loading**:

```
docs/
├── quick-start.md              # Complete getting started (9KB)
├── concepts/
│   ├── plugin-lifecycle.md     # Lifecycle methods (12KB)
│   └── devices.md              # Device development (11KB)
├── api/
│   └── indigo-object-model.md  # Complete API reference (9KB)
├── examples/
│   └── sdk-examples-guide.md   # Catalog of 16 examples (8KB)
└── troubleshooting/
    └── common-issues.md        # Common problems (11KB)

sdk-examples/                   # 16 complete plugins (1.3MB)
├── README.md                   # Quick catalog (6KB)
└── [16 example plugins]        # Load individually only

snippets/
└── plugin-base-template.py     # Clean template
```

## SDK Examples: 16 Complete Plugins

**Device Types** (Load when user needs specific type):
- Custom - General-purpose with custom states
- Relay/Dimmer - On/off and brightness control
- Thermostat - Climate control with HVAC modes
- Sensor - Read-only monitoring
- Speed Control - Variable speed (fans)
- Sprinkler - Multi-zone irrigation
- Energy Meter - Power monitoring

**Integration** (Load when user needs integration):
- HTTP Responder - Web server/REST API
- Action API - Custom actions
- Broadcaster/Subscriber - Plugin communication
- Variable Subscriber - Monitor variables
- Database Traverse - Query database

**Finding examples**: Read `sdk-examples/README.md` or `docs/examples/sdk-examples-guide.md` first, then load specific example.

## Version Information

- **Current**: Indigo 2023.2+ (Python 3.10+)
- **Legacy**: 2022.x (Python 2.7, not recommended)
- Always use Python 3 syntax

## Best Practices (Always Follow)

### Code Quality
- ✅ Always call `super()` in all lifecycle methods
- ✅ Use `self.sleep()` NOT `time.sleep()` in concurrent threads
- ✅ Validate all user input in validation callbacks
- ✅ Log appropriately: `self.logger.debug/info/error/exception()`
- ✅ Bundle Python dependencies in `Contents/Packages/`
- ✅ Handle exceptions gracefully
- ✅ Close connections in `shutdown()`

### Security
- Never expose API keys in logs
- Validate all external input
- Handle exceptions without exposing sensitive data

## Response Guidelines

1. **Reference file paths**: Link to specific docs with markdown
   - Example: "See [plugin-lifecycle.md](docs/concepts/plugin-lifecycle.md)"

2. **Show code examples**: Always include working code snippets

3. **Explain why**: Don't just show code, explain the pattern

4. **Point to examples**: "This is like Example Device - Thermostat"

## When to Use Each Resource

| User Need | Load These | Don't Load |
|-----------|-----------|------------|
| Create plugin | quick-start.md, template.py | Examples |
| Debug | troubleshooting/common-issues.md | Concepts |
| API question | api/indigo-object-model.md | Examples |
| Concept | Specific concept doc | All concepts |
| Example | sdk-examples-guide.md + specific example | All examples |

## Quick Reference

### Core Files
- `docs/quick-start.md` - Getting started
- `docs/concepts/plugin-lifecycle.md` - Lifecycle
- `docs/concepts/devices.md` - Devices
- `docs/api/indigo-object-model.md` - API
- `docs/examples/sdk-examples-guide.md` - Example catalog
- `docs/troubleshooting/common-issues.md` - Troubleshooting

### External Resources
- Official Plugin Guide: https://www.indigodomo.com/docs/plugin_guide
- Object Model Reference: https://www.indigodomo.com/docs/object_model_reference
- Scripting Tutorial: https://www.indigodomo.com/docs/plugin_scripting_tutorial
- Developer Forum: https://forums.indigodomo.com/viewforum.php?f=18

## Skill Maintenance

This skill is actively maintained by the Indigo community.

- **Report issues**: https://github.com/simons-plugins/indigo-claude-skill/issues
- **Contribute**: https://github.com/simons-plugins/indigo-claude-skill/pulls
- **Discussions**: https://github.com/simons-plugins/indigo-claude-skill/discussions
