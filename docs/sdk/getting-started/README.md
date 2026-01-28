# Getting Started with Indigo Plugin Development

## Official Tutorials

### Indigo Scripting Tutorial
**URL**: https://www.indigodomo.com/docs/plugin_scripting_tutorial

This comprehensive tutorial walks through plugin development step-by-step:

1. **Introduction to Indigo Scripting** - Overview of the scripting environment
2. **Your First Plugin** - Create a simple "Hello World" plugin
3. **Plugin Structure** - Understanding the `.indigoPlugin` bundle
4. **The Plugin Class** - Implementing `indigo.PluginBase`
5. **Device Communication** - Creating and managing devices
6. **Actions and Events** - Responding to user actions
7. **Configuration UIs** - Building device and plugin configuration dialogs

**When to use**: Start here if you're new to Indigo plugin development.

## Setting Up Your Development Environment

### Prerequisites
- macOS computer
- Indigo home automation server installed
- Text editor or IDE (PyCharm, VS Code, etc.)
- Basic Python knowledge

### Installation Steps

1. **Locate Indigo's Python**
   - Indigo uses Python 3.10+ (as of Indigo 2023+)
   - Located at: `/Library/Frameworks/Python.framework/Versions/Current/bin/python3`

2. **Clone or Copy Example Plugin**
   ```bash
   cd "/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins (Disabled)/"
   # Copy one of the SDK examples as your starting point
   ```

3. **Edit Info.plist**
   - Change `CFBundleIdentifier` to unique value
   - Update `CFBundleDisplayName`
   - Set appropriate `ServerApiVersion` (3.6 or later)

4. **Enable Plugin in Indigo**
   - Open Indigo
   - Go to Plugins → Manage Plugins
   - Your plugin should appear in the list
   - Click checkbox to enable

## First Plugin Checklist

- [ ] Unique `CFBundleIdentifier` in Info.plist
- [ ] `Plugin` class in plugin.py inherits from `indigo.PluginBase`
- [ ] `__init__` method calls `super().__init__()`
- [ ] `startup()` and `shutdown()` methods defined
- [ ] Plugin appears in Indigo's Plugins menu
- [ ] Plugin can be enabled/disabled without errors

## Quick Reference: Minimum Plugin Structure

```python
# plugin.py
try:
    import indigo
except ImportError:
    pass

class Plugin(indigo.PluginBase):
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug = True

    def startup(self):
        self.logger.info("Plugin started")

    def shutdown(self):
        self.logger.info("Plugin stopped")
```

```xml
<!-- Info.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PluginVersion</key>
    <string>1.0.0</string>
    <key>ServerApiVersion</key>
    <string>3.6</string>
    <key>CFBundleDisplayName</key>
    <string>My Plugin</string>
    <key>CFBundleIdentifier</key>
    <string>com.mycompany.indigoplugin.myplugin</string>
</dict>
</plist>
```

## Next Steps

After creating your first plugin:
1. Review [../plugin-development/plugin-lifecycle.md](../plugin-development/plugin-lifecycle.md)
2. Learn about [../plugin-development/devices.md](../plugin-development/devices.md)
3. Explore the SDK example plugins
4. Join the [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)

## Common First-Time Issues

### Plugin Won't Enable
- Check `CFBundleIdentifier` is unique and doesn't conflict
- Verify `ServerApiVersion` is 3.0 or higher for Python 3
- Check Indigo Event Log for Python errors

### Can't See Plugin in Indigo
- Verify `.indigoPlugin` bundle is in correct location
- Restart Indigo server
- Check file permissions on plugin bundle

### Import Errors
- Ensure all required packages are in `Contents/Packages/`
- Don't use system Python packages - bundle them with plugin
- Check for Python 2 vs Python 3 syntax issues

## Resources

- SDK Examples: See parent directory for working examples
- [Plugin Developer's Guide](https://www.indigodomo.com/docs/plugin_guide)
- [API Migration Guide](../IndigoSDK-2025.1/Updating%20to%20API%20version%203.0%20(Python%203).md)
