# Quick Start: Indigo Plugin Development

Your comprehensive guide to creating your first Indigo plugin in minutes.

## Prerequisites

- **macOS**: Indigo runs only on macOS
- **Indigo 2023.2+**: Home automation server installed and running
- **Python 3.10+**: Comes with macOS, used by Indigo
- **Text Editor**: VS Code, PyCharm, or any code editor
- **Basic Python**: Understanding of Python and object-oriented programming

## Official Tutorial

📖 **Start here if you're completely new**: [Indigo Scripting Tutorial](https://www.indigodomo.com/docs/plugin_scripting_tutorial)

The official tutorial covers:
- Introduction to Indigo scripting environment
- Your first "Hello World" plugin
- Plugin structure and architecture
- Device communication
- Actions, events, and configuration UIs

## Three Ways to Start

### Option 1: Copy an SDK Example (Recommended)

Start with a working example as your template:

```bash
# Navigate to your development directory
cd ~/Documents

# Copy the Custom Device example
cp -r "/Library/Application Support/Perceptive Automation/Indigo 2023.2/IndigoSDK/Example Device - Custom.indigoPlugin" MyFirstPlugin.indigoPlugin

# Edit the plugin
cd MyFirstPlugin.indigoPlugin/Contents
```

**Edit `Info.plist`** - Make these changes:
- `CFBundleIdentifier`: `com.yourname.myfirstplugin` (must be unique)
- `CFBundleDisplayName`: `My First Plugin`
- `CFBundleVersion`: `1.0.0`

**Edit `Server Plugin/plugin.py`** - Customize the plugin class

### Option 2: Use the Skill Template

Use the included template from this skill:

```bash
# Copy the base template
cp /path/to/indigo-skill/snippets/plugin-base-template.py plugin.py
```

Then create the required Info.plist and plugin structure.

### Option 3: Build from Scratch

Create a minimal "Hello World" plugin to understand the basics.

## Minimal Plugin: Hello World

### 1. Create Plugin Structure

```bash
mkdir -p "HelloWorld.indigoPlugin/Contents/Server Plugin"
cd HelloWorld.indigoPlugin/Contents
```

### 2. Create Info.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>com.yourname.helloworld</string>
    <key>CFBundleDisplayName</key>
    <string>Hello World</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>ServerApiVersion</key>
    <string>3.0</string>
</dict>
</plist>
```

### 3. Create Server Plugin/plugin.py

```python
try:
    import indigo
except ImportError:
    pass

class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True

    def startup(self):
        self.logger.info("Hello World! Plugin started.")

    def shutdown(self):
        self.logger.info("Goodbye! Plugin stopped.")
```

### 4. Install and Test

```bash
# Copy to Indigo's plugin folder
cp -r HelloWorld.indigoPlugin "/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins/"
```

### 5. Enable in Indigo

1. Open Indigo application
2. Go to **Plugins → Manage Plugins**
3. Find "Hello World" in the list
4. Click checkbox to enable
5. Open **View → Event Log Window**
6. You should see "Hello World! Plugin started."

## Plugin Structure Reference

Every Indigo plugin follows this bundle structure:

```
MyPlugin.indigoPlugin/
├── Contents/
│   ├── Info.plist                 # Plugin metadata (REQUIRED)
│   ├── Server Plugin/
│   │   ├── plugin.py              # Main plugin class (REQUIRED)
│   │   ├── Devices.xml            # Device type definitions
│   │   ├── Actions.xml            # Action definitions
│   │   ├── MenuItems.xml          # Plugin menu items
│   │   ├── PluginConfig.xml       # Plugin configuration UI
│   │   └── Events.xml             # Event/trigger definitions
│   ├── Resources/                  # Web content (auto-served)
│   └── Packages/                   # Bundled Python libraries
```

**Minimum required files:**
- ✅ `Info.plist` - Plugin metadata
- ✅ `Server Plugin/plugin.py` - Plugin class inheriting from `indigo.PluginBase`

## First Plugin Checklist

Before enabling your plugin, verify:

- [ ] Unique `CFBundleIdentifier` in Info.plist (no conflicts with other plugins)
- [ ] `ServerApiVersion` is `3.0` or higher (for Python 3 support)
- [ ] `Plugin` class inherits from `indigo.PluginBase`
- [ ] `__init__` method calls `super().__init__()`
- [ ] `startup()` and `shutdown()` methods are defined
- [ ] Plugin bundle ends with `.indigoPlugin`
- [ ] Plugin is in correct folder: `/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins/`

## Common Beginner Mistakes

### ❌ Mistake 1: Forgetting to call `super()`

```python
# WRONG - Skips parent initialization
def startup(self):
    self.logger.info("Starting")

# RIGHT - Always call super first
def startup(self):
    super().startup()
    self.logger.info("Starting")
```

### ❌ Mistake 2: Using `time.sleep()` in concurrent thread

```python
# WRONG - Blocks shutdown, plugin won't stop cleanly
def runConcurrentThread(self):
    while True:
        self.update_data()
        time.sleep(60)

# RIGHT - Use self.sleep() for clean shutdown
def runConcurrentThread(self):
    try:
        while True:
            self.update_data()
            self.sleep(60)  # Allows StopThread exception
    except self.StopThread:
        pass
```

### ❌ Mistake 3: Not validating user input

```python
# WRONG - Accepts any input, will crash later
def validatePrefsConfigUi(self, valuesDict):
    return True

# RIGHT - Validate and provide helpful errors
def validatePrefsConfigUi(self, valuesDict):
    errorsDict = indigo.Dict()

    if not valuesDict.get("apiKey"):
        errorsDict["apiKey"] = "API key is required"

    if not valuesDict.get("updateInterval", "").isdigit():
        errorsDict["updateInterval"] = "Must be a number"

    return (len(errorsDict) == 0, valuesDict, errorsDict)
```

### ❌ Mistake 4: Using system Python packages

```python
# WRONG - Relies on system packages (may not exist)
import requests

# RIGHT - Bundle packages in Contents/Packages/
# Install: pip install -t "Contents/Packages/" requests
import sys
sys.path.insert(0, './Contents/Packages')
import requests
```

## Common First-Time Issues

### Plugin Won't Enable

**Symptoms**: Plugin appears in list but won't enable, or disappears after restart

**Solutions**:
- Check `CFBundleIdentifier` is unique (doesn't match another plugin)
- Verify `ServerApiVersion` is `3.0` or higher
- Open Event Log for Python errors
- Check file permissions: `chmod -R 755 MyPlugin.indigoPlugin`

### Plugin Not Visible in Indigo

**Symptoms**: Plugin doesn't appear in Plugins → Manage Plugins

**Solutions**:
- Verify bundle name ends with `.indigoPlugin`
- Check bundle is in correct location: `/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins/`
- Restart Indigo Server Helper
- Check Info.plist is valid XML (no syntax errors)

### Import Errors in Event Log

**Symptoms**: `ModuleNotFoundError` or `ImportError` in Event Log

**Solutions**:
- Bundle all dependencies in `Contents/Packages/`
- Don't rely on system Python packages
- Use Python 3 syntax (not Python 2)
- Check package compatibility with Python 3.10+

## Python Version Reference

| Indigo Version | Python Version | Notes |
|----------------|----------------|-------|
| 2023.2+ | Python 3.10+ | Current, recommended |
| 2022.x | Python 2.7 | Legacy, end-of-life |

**For Python 3 migration**, see: [`reference/Python3-Migration-Guide.md`](../reference/Python3-Migration-Guide.md)

## Next Steps

Now that you have a working plugin:

1. **Understand Plugin Architecture**
   - Read [`concepts/plugin-lifecycle.md`](concepts/plugin-lifecycle.md)
   - Learn about device types in [`concepts/device-types.md`](concepts/device-types.md)

2. **Add Functionality**
   - Create devices: See [`concepts/devices.md`](concepts/devices.md)
   - Add actions: See [`patterns/actions-and-events.md`](patterns/actions-and-events.md)
   - Build config UIs: See [`api/ui-validation.md`](api/ui-validation.md)

3. **Study Examples**
   - Browse [`sdk-examples/README.md`](../sdk-examples/README.md) for 16 complete examples
   - Review [`examples/`](examples/) for pattern documentation

4. **Get Help**
   - Check [`troubleshooting/common-issues.md`](troubleshooting/common-issues.md)
   - Ask on [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)

## External Resources

- 📖 [Official Plugin Developer's Guide](https://www.indigodomo.com/docs/plugin_guide)
- 📚 [Indigo Object Model Reference](https://www.indigodomo.com/docs/object_model_reference)
- 💬 [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)
- 🔧 [GitHub: Indigo Skill Repository](https://github.com/indigo-community/indigo-skill)

---

**Ready to build something amazing?** Start with a working example, modify it to fit your needs, and iterate!
