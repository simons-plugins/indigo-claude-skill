# IOM Architecture and Core Concepts

## Client-Server Architecture

The Indigo Object Model runs in a **separate process** from IndigoServer. This design prevents scripts/plugins from crashing the server.

**Key implication**: When you get an object, you receive a **copy**, not the actual object.

## Object Manipulation Rules

### For All Scripts and Plugins

| Task | Method |
|------|--------|
| Create/duplicate/delete objects | Use command namespace (e.g., `indigo.device.create()`) |
| Send commands (turnOn, etc.) | Use command namespace with object reference |
| Modify object definition | Get copy → modify → `myObject.replaceOnServer()` |
| Refresh local copy | Call `myObject.refreshFromServer()` |

### For Plugin Developers Only

| Task | Method |
|------|--------|
| Update device plugin props | `myDevice.replacePluginPropsOnServer(newPropsDict)` |
| Update device state | `myDevice.updateStateOnServer(key="keyName", value="Value")` |

## Object IDs

Every top-level object has a **globally unique integer ID**:
- Action groups, devices, folders, schedules, triggers, variables
- Commands accept ID, object reference, or name
- **Always store IDs, never names** (names can change)

```python
# All equivalent
indigo.device.turnOn(123456)
indigo.device.turnOn(dev)
indigo.device.turnOn("Living Room Lamp")  # Not recommended for storage
```

## replaceOnServer Pattern

The standard pattern for modifying object definitions:

```python
# Get a copy
dev = indigo.devices[123456]

# Modify locally
dev.name = "New Name"
dev.description = "Updated description"

# Push changes to server
dev.replaceOnServer()
```

## refreshFromServer Pattern

Update your local copy to match the server:

```python
dev = indigo.devices[123456]
# ... time passes, device may have changed ...
dev.refreshFromServer()
# dev now has current server values
```

## Plugin Props

Plugin properties (`pluginProps`) are read-write for the owning plugin, read-only for scripts.

```python
# Plugin updating its own device props
newProps = dev.pluginProps
newProps["someKey"] = "newValue"
dev.replacePluginPropsOnServer(newProps)
```

## Built-in Collection Objects

| Object | Description |
|--------|-------------|
| `indigo.devices` | All devices |
| `indigo.triggers` | All triggers |
| `indigo.schedules` | All schedules |
| `indigo.actionGroups` | All action groups |
| `indigo.variables` | All variables |

These collections are **read-only** - use command namespaces to modify.

### Folders Attribute

Each collection has a `folders` attribute:

```python
# Access device folders
for folder in indigo.devices.folders:
    print(folder.name)

# Access variable folders
for folder in indigo.variables.folders:
    print(folder.name)
```

### getName() Convenience Method

Efficiently get an object's name without fetching the entire object:

```python
# More efficient than indigo.devices[123].name
name = indigo.devices.getName(123456)

# Works for folders too
folder_name = indigo.variables.folders.getName(folder_id)
```

### iterkeys() Method

Iterate over just the IDs (more efficient when you only need IDs):

```python
for dev_id in indigo.devices.iterkeys():
    # process just the ID without loading the full object
    pass
```

## Common Exceptions

| Exception | Cause |
|-----------|-------|
| `ArgumentError` | Missing or incorrect parameter type |
| `IndexError` | Index out of range |
| `KeyError` | Dictionary key not found |
| `PluginNotFoundError` | Target plugin is disabled or missing |
| `TypeError` | Incorrect runtime type |
| `ValueError` | Illegal or disallowed value |

## Python Introspection

Use standard Python introspection to explore objects:

```python
dev = indigo.devices[123456]

# Get class type
dev.__class__  # <class 'indigo.DimmerDevice'>

# List all attributes and methods
dir(dev)

# Check for attribute
hasattr(dev, 'brightness')  # True for dimmers

# Get plugin device type
dev.deviceTypeId  # 'myDeviceType'
```

## Object to Dictionary Conversion

Convert any Indigo object to a Python dict for serialization:

```python
dev = indigo.devices[123456]
dev_dict = dict(dev)  # Standard Python dict with all properties
```
