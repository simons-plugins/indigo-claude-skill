# Plugin Lifecycle

**Official Documentation**: https://www.indigodomo.com/docs/plugin_guide#plugin_lifecycle

## Overview

Understanding the plugin lifecycle is crucial for proper resource management and avoiding memory leaks or zombie processes.

## Lifecycle Methods

### 1. `__init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs)`

**When Called**: Plugin is first instantiated by Indigo

**Purpose**: Initialize instance variables

**Rules**:
- MUST call `super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)`
- Do NOT access Indigo database here (devices, variables, etc.)
- Do NOT subscribe to events here
- Only initialize instance attributes

```python
def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs):
    super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
    self.debug = plugin_prefs.get('showDebugInfo', False)
    self.device_dict = {}  # Store device references
```

### 2. `startup(self)`

**When Called**: After `__init__`, before plugin becomes active

**Purpose**: Initialize resources, subscribe to events, start connections

**Use Cases**:
- Subscribe to variable/device changes
- Initialize hardware connections
- Load cached data
- Create programmatic devices

```python
def startup(self):
    self.logger.debug("Plugin startup")
    indigo.devices.subscribeToChanges()
    indigo.variables.subscribeToChanges()
    self.connect_to_hardware()
```

**Example**: [../IndigoSDK-2025.1/Example Variable Change Subscriber.indigoPlugin/Contents/Server Plugin/plugin.py](../IndigoSDK-2025.1/Example%20Variable%20Change%20Subscriber.indigoPlugin/Contents/Server%20Plugin/plugin.py)

### 3. `runConcurrentThread(self)` *(Optional)*

**When Called**: Automatically started in separate thread after `startup()`

**Purpose**: Background polling, periodic tasks

**Rules**:
- MUST loop forever until `self.stopThread` flag is set
- Use `self.sleep(seconds)` instead of `time.sleep()` for clean shutdown
- Catch `self.StopThread` exception for cleanup
- If this method returns prematurely, Indigo will restart it

```python
def runConcurrentThread(self):
    try:
        while True:
            for dev in indigo.devices.iter("self"):
                if dev.enabled:
                    self.poll_device(dev)
            self.sleep(60)  # Poll every 60 seconds
    except self.StopThread:
        self.logger.debug("Thread stopped")
```

**Example**: [../IndigoSDK-2025.1/Example Device - Custom.indigoPlugin/Contents/Server Plugin/plugin.py](../IndigoSDK-2025.1/Example%20Device%20-%20Custom.indigoPlugin/Contents/Server%20Plugin/plugin.py)

### 4. `shutdown(self)`

**When Called**: Plugin is being stopped (disabled, Indigo quitting, etc.)

**Purpose**: Clean up resources, close connections, save state

**Rules**:
- Clean up all resources
- Close network connections
- Cancel timers
- Stop background tasks

```python
def shutdown(self):
    self.logger.debug("Plugin shutdown")
    self.disconnect_from_hardware()
    # Clear device states if desired
    for dev in indigo.devices.iter("self"):
        dev.updateStateOnServer('status', value='offline')
```

### 5. `prepareToSleep(self)` *(Optional)*

**When Called**: Computer is about to sleep

```python
def prepareToSleep(self):
    self.logger.debug("Preparing for sleep")
    # Close connections that won't survive sleep
```

### 6. `wakeUp(self)` *(Optional)*

**When Called**: Computer wakes from sleep

```python
def wakeUp(self):
    self.logger.debug("Waking up")
    # Reconnect to hardware
    # Refresh device states
```

## Lifecycle Diagram

```
Plugin Load
     ↓
__init__()
     ↓
startup()
     ↓
runConcurrentThread() [separate thread, optional]
     ↓
[Plugin runs normally, handling callbacks]
     ↓
prepareToSleep() [optional, when computer sleeps]
     ↓
wakeUp() [optional, when computer wakes]
     ↓
shutdown()
     ↓
Plugin Unload
```

## Best Practices

### Resource Initialization
- Initialize in `startup()`, not `__init__()`
- Subscribe to changes in `startup()`
- Create persistent connections in `startup()`

### Resource Cleanup
- Always clean up in `shutdown()`
- Don't rely on `__del__()` - it may not be called
- Close files, sockets, and other resources explicitly

### Thread Management
- Only use `runConcurrentThread()` if you need polling
- For event-driven plugins, rely on callbacks instead
- Always use `self.sleep()` instead of `time.sleep()`
- Catch `self.StopThread` exception for graceful shutdown

### Timing Issues
- Don't access `indigo.devices` or `indigo.variables` in `__init__()`
- Database access is safe starting in `startup()`
- Device references can become stale - re-fetch when needed

## Common Pitfalls

### ❌ Accessing Indigo Database in `__init__`
```python
def __init__(self, ...):
    super().__init__(...)
    self.my_device = indigo.devices["MyDevice"]  # WRONG - too early!
```

### ✅ Correct Approach
```python
def __init__(self, ...):
    super().__init__(...)
    self.my_device = None  # Initialize to None

def startup(self):
    self.my_device = indigo.devices["MyDevice"]  # Correct - safe here
```

### ❌ Not Using `self.sleep()` in Concurrent Thread
```python
def runConcurrentThread(self):
    while True:
        self.poll_devices()
        time.sleep(60)  # WRONG - prevents clean shutdown
```

### ✅ Correct Approach
```python
def runConcurrentThread(self):
    try:
        while True:
            self.poll_devices()
            self.sleep(60)  # Correct - allows interruption
    except self.StopThread:
        pass
```

## Related Topics

- [devices.md](devices.md) - Device lifecycle callbacks
- [actions.md](actions.md) - Action handlers
- [events.md](events.md) - Event subscriptions

## Official References

- [Plugin Developer's Guide - Plugin Lifecycle](https://www.indigodomo.com/docs/plugin_guide#plugin_lifecycle)
- [Plugin Developer's Guide - Concurrent Thread](https://www.indigodomo.com/docs/plugin_guide#concurrent_thread)
