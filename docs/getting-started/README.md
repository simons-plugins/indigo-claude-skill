# Getting Started with Indigo Plugin Development

Welcome to Indigo plugin development! This guide will help you create your first plugin.

## Prerequisites

- **macOS**: Indigo runs only on macOS
- **Indigo**: Installed and running (2023.2+ recommended)
- **Python**: Python 3.10+ (comes with macOS, used by Indigo 2023.2+)
- **Text Editor**: VS Code, PyCharm, or any text editor
- **Basic Python Knowledge**: Understanding of Python syntax and object-oriented programming

## Quick Start

### 1. Set Up Development Environment

```bash
# Create a development directory
mkdir ~/IndigoPlugins
cd ~/IndigoPlugins
```

### 2. Copy an Example Plugin as Template

The Indigo SDK includes example plugins you can use as starting points:

```bash
# Copy the basic custom device example
cp -r "/Library/Application Support/Perceptive Automation/Indigo 2023.2/IndigoSDK/Example Device - Custom.indigoPlugin" MyFirstPlugin.indigoPlugin
```

### 3. Edit Plugin Metadata

Open `MyFirstPlugin.indigoPlugin/Contents/Info.plist` and change:

- **CFBundleIdentifier**: Make it unique (e.g., `com.yourname.myfirstplugin`)
- **CFBundleDisplayName**: Your plugin's name
- **CFBundleVersion**: Start with `1.0.0`

### 4. Edit Plugin Code

The main plugin code is in `Contents/Server Plugin/plugin.py`:

```python
import indigo

class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True

    def startup(self):
        self.logger.info("MyFirstPlugin starting up")

    def shutdown(self):
        self.logger.info("MyFirstPlugin shutting down")
```

### 5. Install for Testing

```bash
# Copy to Indigo's plugin folder
cp -r MyFirstPlugin.indigoPlugin "/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins/"
```

### 6. Enable in Indigo

1. Open Indigo
2. Go to **Plugins → Manage Plugins**
3. Find your plugin and click **Enable**
4. Check **View → Event Log Window** for messages

## Plugin Structure

Every Indigo plugin follows this structure:

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
│   ├── Resources/                  # Web content (auto-served at /plugin-id/)
│   └── Packages/                   # Bundled Python libraries
```

## Your First Plugin: Hello World

Let's create a minimal plugin that logs "Hello World":

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

### 3. Create plugin.py

```python
import indigo

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
cp -r ../HelloWorld.indigoPlugin "/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins/"
```

Enable in Indigo and check the Event Log for "Hello World!" message.

## Next Steps

- **[Core Concepts](../core-concepts/)** - Understand plugin architecture
- **[Plugin Lifecycle](../core-concepts/plugin-lifecycle.md)** - Learn the plugin execution flow
- **[Device Types](../core-concepts/device-types.md)** - Create different types of devices
- **[Examples](../examples/)** - Study complete working examples

## Common Beginner Mistakes

1. ❌ **Forgetting to call `super()`** in callbacks
   ```python
   # WRONG
   def startup(self):
       self.logger.info("Starting")

   # RIGHT
   def startup(self):
       super().startup()  # Always call super first!
       self.logger.info("Starting")
   ```

2. ❌ **Using `time.sleep()` in concurrent thread**
   ```python
   # WRONG
   def runConcurrentThread(self):
       while True:
           time.sleep(60)  # Blocks shutdown

   # RIGHT
   def runConcurrentThread(self):
       while True:
           self.sleep(60)  # Allows clean shutdown
   ```

3. ❌ **Not validating user input**
   ```python
   # WRONG
   def validatePrefsConfigUi(self, valuesDict):
       return True  # Accepts anything!

   # RIGHT
   def validatePrefsConfigUi(self, valuesDict):
       errorsDict = indigo.Dict()
       if not valuesDict.get("apiKey"):
           errorsDict["apiKey"] = "API key is required"
       return (len(errorsDict) == 0, valuesDict, errorsDict)
   ```

## Getting Help

- 📚 [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)
- 📖 [Official Plugin Guide](https://www.indigodomo.com/docs/plugin_guide)
- 💬 Ask in this repository's Discussions

Happy plugin development! 🚀
