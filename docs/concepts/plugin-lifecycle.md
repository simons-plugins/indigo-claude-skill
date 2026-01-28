# Plugin Lifecycle

**Official Documentation**: https://www.indigodomo.com/docs/plugin_guide#plugin_lifecycle

Understanding the plugin lifecycle is essential for proper plugin development, resource management, and avoiding memory leaks or zombie processes.

## Lifecycle Flow

```
Plugin Enable/Indigo Start
         ↓
    __init__()
         ↓
     startup()
         ↓
runConcurrentThread() (optional, runs continuously)
         ↓
   [Plugin runs normally]
         ↓
prepareToSleep() (optional, computer sleeping)
         ↓
    wakeUp() (optional, computer waking)
         ↓
    shutdown()
         ↓
   Plugin Disabled/Indigo Quit
```

## Lifecycle Methods

### `__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs, **kwargs)`

**When**: Plugin object is first instantiated by Indigo

**Purpose**: Initialize instance variables ONLY

**Rules**:
- ✅ MUST call `super().__init__()` first
- ✅ Set instance variables
- ✅ Initialize data structures
- ❌ NO Indigo API calls (no accessing `indigo.devices`, `indigo.variables`, etc.)
- ❌ NO network requests
- ❌ NO device communication
- ❌ NO event subscriptions

```python
def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs, **kwargs):
    super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

    # Initialize instance variables
    self.debug = pluginPrefs.get("showDebugInfo", False)
    self.api_key = pluginPrefs.get("apiKey", "")
    self.devices_dict = {}
    self.api_client = None  # Will initialize in startup()

    # Set up logging
    if self.debug:
        self.logger.debug("Debug logging enabled")
```

**Why the restrictions?** Indigo's database isn't ready yet during `__init__()`. Device and variable access will fail.

### `startup()`

**When**: After `__init__()`, before plugin becomes active

**Purpose**: Initialize resources, subscribe to events, start connections

**Rules**:
- ❌ Do NOT call `super().startup()` (method doesn't exist in base class)
- ✅ Initialize API connections
- ✅ Subscribe to Indigo events
- ✅ Load persistent data
- ✅ Validate configuration
- ✅ Access Indigo database (devices, variables)

```python
def startup(self):
    # Note: Do NOT call super().startup() - it doesn't exist
    self.logger.info(f"{self.pluginDisplayName} starting")

    # Now safe to access Indigo database
    for dev in indigo.devices.iter("self"):
        self.logger.debug(f"Found device: {dev.name}")

    # Initialize API client
    if self.api_key:
        self.api_client = APIClient(self.api_key)
    else:
        self.logger.error("No API key configured")

    # Subscribe to device updates
    indigo.devices.subscribeToChanges()
    indigo.variables.subscribeToChanges()

    # Load saved state
    self._load_state()
```

**Example**: [Example Variable Change Subscriber](../../sdk-examples/Example%20Variable%20Change%20Subscriber.indigoPlugin/Contents/Server%20Plugin/plugin.py)

### `runConcurrentThread()` (Optional)

**When**: Automatically started in separate thread after `startup()`

**Purpose**: Background tasks like polling APIs, periodic updates

**Rules**:
- ✅ Use `self.sleep()` NOT `time.sleep()`
- ✅ Catch `self.StopThread` exception for clean shutdown
- ✅ Handle exceptions to prevent thread exit
- ✅ Use reasonable sleep intervals
- ✅ Loop forever until `self.stopThread` flag is set

**Important**: If this method returns prematurely (due to uncaught exception), Indigo will restart it, potentially causing loops and performance issues.

```python
def runConcurrentThread(self):
    """Poll API every 5 minutes."""
    try:
        while True:
            try:
                self._update_all_devices()
            except Exception as exc:
                self.logger.exception("Error updating devices")

            # Use self.sleep() to allow clean shutdown
            self.sleep(300)  # 5 minutes
    except self.StopThread:
        # Normal shutdown, thread is being stopped
        pass
```

**Example**: [Example Device - Custom](../../sdk-examples/Example%20Device%20-%20Custom.indigoPlugin/Contents/Server%20Plugin/plugin.py)

**Polling Best Practices**:
- Use configurable intervals from plugin preferences
- Respect API rate limits (see pattern below)
- Log errors but don't crash the thread
- Use `self.sleep()` for interruptible waits
- Consider using event-driven patterns instead if possible

**Rate Limiting Pattern**:
```python
def runConcurrentThread(self):
    try:
        while True:
            # Check if we're being rate limited
            if self.rate_limit_until and datetime.now() < self.rate_limit_until:
                wait_seconds = (self.rate_limit_until - datetime.now()).total_seconds()
                self.logger.debug(f"Rate limited, waiting {wait_seconds}s")
                self.sleep(wait_seconds)
                continue

            try:
                self._update_all_devices()
            except RateLimitError as exc:
                self.rate_limit_until = datetime.now() + timedelta(minutes=10)
                self.logger.warning(f"Rate limited: {exc}")
            except Exception as exc:
                self.logger.exception("Error updating devices")

            self.sleep(self.update_frequency)
    except self.StopThread:
        pass
```

### `shutdown()`

**When**: Plugin is being disabled or Indigo is quitting

**Purpose**: Clean up resources, close connections, save state

**Rules**:
- ✅ Clean up connections
- ✅ Save persistent data
- ✅ Unsubscribe from events
- ✅ Close files and sockets
- ✅ Cancel timers
- ❌ Do NOT call `super().shutdown()` (method doesn't exist in base class)

```python
def shutdown(self):
    self.logger.info(f"{self.pluginDisplayName} shutting down")

    # Save state
    try:
        self._save_state()
    except Exception as exc:
        self.logger.exception("Error saving state")

    # Close API connections
    if hasattr(self, 'api_client') and self.api_client:
        try:
            self.api_client.close()
        except Exception as exc:
            self.logger.exception("Error closing API client")

    # Unsubscribe from changes
    try:
        indigo.devices.unsubscribeToChanges()
        indigo.variables.unsubscribeToChanges()
    except Exception as exc:
        self.logger.exception("Error unsubscribing")

    # Clear device states if desired
    for dev in indigo.devices.iter("self"):
        try:
            dev.updateStateOnServer('status', value='offline')
        except Exception:
            pass

    # Note: Do NOT call super().shutdown() - it doesn't exist
```

**Best Practice**: Wrap cleanup operations in try/except blocks to ensure all cleanup happens even if one step fails.

### `prepareToSleep()` (Optional)

**When**: Computer is about to sleep

**Purpose**: Prepare for system sleep (close connections that won't survive sleep)

```python
def prepareToSleep(self):
    self.logger.debug("Preparing for sleep")
    # Close connections that won't survive sleep
    if self.api_client:
        self.api_client.disconnect()
```

### `wakeUp()` (Optional)

**When**: Computer wakes from sleep

**Purpose**: Restore connections and refresh state after sleep

```python
def wakeUp(self):
    self.logger.debug("Waking up from sleep")
    # Reconnect to hardware/services
    if self.api_client:
        self.api_client.reconnect()
    # Refresh device states
    self._update_all_devices()
```

## Device Lifecycle Callbacks

These callbacks are called for each device as it starts, stops, or changes:

### `deviceStartComm(dev)`

**When**:
- Device is created
- Device is enabled
- Plugin starts with device already enabled

**Purpose**: Initialize device-specific resources and connections

```python
def deviceStartComm(self, dev):
    super().deviceStartComm(dev)

    self.logger.info(f"Starting device: {dev.name}")

    # Refresh state list if Devices.xml changed
    dev.stateListOrDisplayStateIdChanged()

    # Initialize device-specific resources
    self.devices_dict[dev.id] = {
        'last_update': None,
        'retry_count': 0
    }

    # Initialize hardware connection
    address = dev.pluginProps.get('address', '')
    self.connect_to_device(address)

    # Set initial state
    dev.updateStateOnServer("status", "initializing")
    dev.updateStateOnServer("onOffState", False)
```

### `deviceStopComm(dev)`

**When**:
- Device is disabled
- Device is deleted
- Plugin is shutting down

**Purpose**: Clean up device-specific resources

```python
def deviceStopComm(self, dev):
    super().deviceStopComm(dev)

    self.logger.info(f"Stopping device: {dev.name}")

    # Disconnect from hardware
    self.disconnect_from_device(dev)

    # Clean up device-specific resources
    if dev.id in self.devices_dict:
        del self.devices_dict[dev.id]

    # Clear states if desired
    dev.updateStateOnServer('status', value='offline')
```

### `deviceCreated(dev)`

**When**: A new device is created

```python
def deviceCreated(self, dev):
    self.logger.debug(f"Device created: {dev.name}")
    # Perform one-time setup if needed
```

### `deviceUpdated(origDev, newDev)`

**When**: Device properties are changed in Indigo

**Purpose**: React to configuration changes

```python
def deviceUpdated(self, origDev, newDev):
    super().deviceUpdated(origDev, newDev)

    # Only process changes to our plugin's devices
    if newDev.pluginId == self.pluginId:
        # Check if relevant properties changed
        if origDev.address != newDev.address:
            self.logger.info(f"Device {newDev.name} address changed")
            self._reinitialize_device(newDev)

        if origDev.pluginProps.get('pollingInterval') != newDev.pluginProps.get('pollingInterval'):
            self.logger.info(f"Device {newDev.name} polling interval changed")
            # Update polling schedule
```

### `deviceDeleted(dev)`

**When**: Device is deleted

```python
def deviceDeleted(self, dev):
    self.logger.debug(f"Device deleted: {dev.name}")
    # Clean up any persistent data or external resources
    self._cleanup_device_data(dev.id)
```

## Common Patterns

### Deferred Initialization

Sometimes you need to wait for configuration before initializing:

```python
def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs, **kwargs):
    super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
    self.api_client = None  # Will initialize in startup()

def startup(self):
    # Note: Do NOT call super().startup() - it doesn't exist
    api_key = self.pluginPrefs.get("apiKey", "")
    if api_key:
        self.api_client = APIClient(api_key)
    else:
        self.logger.error("No API key configured - plugin will not function")
```

### Graceful Shutdown

Ensure cleanup happens even on errors:

```python
def shutdown(self):
    # Save state
    try:
        self._save_state()
    except Exception as exc:
        self.logger.exception("Error saving state")

    # Close API client
    try:
        if self.api_client:
            self.api_client.close()
    except Exception as exc:
        self.logger.exception("Error closing API client")

    # Note: Do NOT call super().shutdown() - it doesn't exist
```

### Thread-Safe Polling

When accessing shared data from concurrent thread:

```python
import threading

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.data_lock = threading.Lock()
    self.shared_data = {}

def runConcurrentThread(self):
    try:
        while True:
            data = self._fetch_from_api()

            with self.data_lock:
                self.shared_data = data

            self.sleep(60)
    except self.StopThread:
        pass

def actionControlDevice(self, action, dev):
    # Access shared data safely
    with self.data_lock:
        value = self.shared_data.get(dev.address)
```

## Debugging Lifecycle Issues

### Enable Debug Logging

```python
def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs, **kwargs):
    super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
    self.debug = True  # Force debug on during development

def startup(self):
    # Note: Do NOT call super().startup() - it doesn't exist
    self.logger.debug("Startup called")
    self.logger.debug(f"Plugin prefs: {self.pluginPrefs}")
```

### Log Lifecycle Events

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.logger.debug("__init__ called")

def startup(self):
    # Note: Do NOT call super().startup() - it doesn't exist
    self.logger.debug("startup() called")

def runConcurrentThread(self):
    self.logger.debug("runConcurrentThread() started")
    try:
        while True:
            self.logger.threaddebug("Thread loop iteration")
            self.sleep(60)
    except self.StopThread:
        self.logger.debug("StopThread exception caught")

def shutdown(self):
    self.logger.debug("shutdown() called")
    # Note: Do NOT call super().shutdown() - it doesn't exist
```

## Common Mistakes

### ❌ API Calls in `__init__()`

```python
# WRONG - __init__ should not access Indigo database or make API calls
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.my_device = indigo.devices["MyDevice"]  # Fails! Database not ready
    self.data = requests.get(url).json()  # Bad practice!
```

**Fix**: Move to `startup()`:
```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.my_device = None

def startup(self):
    # Note: Do NOT call super().startup() - it doesn't exist
    try:
        self.my_device = indigo.devices["MyDevice"]
    except KeyError:
        self.logger.error("MyDevice not found")
```

### ❌ Calling `super()` in Wrong Methods

```python
# WRONG - startup() doesn't have a parent implementation
def startup(self):
    super().startup()  # AttributeError!
    self.logger.info("Starting")

# WRONG - shutdown() doesn't have a parent implementation
def shutdown(self):
    super().shutdown()  # AttributeError!
```

**Fix**:
```python
# RIGHT - startup() is a pure callback
def startup(self):
    # No super() call needed
    self.logger.info("Starting")

# RIGHT - shutdown() is a pure callback
def shutdown(self):
    # No super() call needed
    self.logger.info("Shutting down")
```

**Remember**: Only call `super()` in `__init__()` (required) and device callbacks like `deviceStartComm()` (recommended)

### ❌ Using `time.sleep()` in Concurrent Thread

```python
import time

# WRONG - Blocks shutdown, plugin won't stop cleanly
def runConcurrentThread(self):
    while True:
        self._update()
        time.sleep(60)  # Can't be interrupted!
```

**Fix**:
```python
# RIGHT - Allows clean shutdown
def runConcurrentThread(self):
    try:
        while True:
            self._update()
            self.sleep(60)  # Interruptible
    except self.StopThread:
        pass
```

### ❌ Crashing the Concurrent Thread

```python
# WRONG - Exception kills thread, updates stop
def runConcurrentThread(self):
    while True:
        self._update_devices()  # Uncaught exception stops thread permanently
        self.sleep(60)
```

**Fix**:
```python
# RIGHT - Thread keeps running even if updates fail
def runConcurrentThread(self):
    try:
        while True:
            try:
                self._update_devices()
            except Exception as exc:
                self.logger.exception("Update error")
            self.sleep(60)
    except self.StopThread:
        pass
```

### ❌ Not Cleaning Up Resources

```python
# WRONG - File left open
def startup(self):
    self.log_file = open("/tmp/mylog.txt", "a")

def shutdown(self):
    # Forgot to close file!
    pass
```

**Fix**:
```python
def startup(self):
    self.log_file = open("/tmp/mylog.txt", "a")

def shutdown(self):
    try:
        if hasattr(self, 'log_file'):
            self.log_file.close()
    except Exception as exc:
        self.logger.exception("Error closing log file")
    # Note: Do NOT call super().shutdown() - it doesn't exist
```

## Resource Management Checklist

- [ ] All instance variables initialized in `__init__()`
- [ ] No Indigo database access in `__init__()`
- [ ] `super()` called in all lifecycle methods
- [ ] Connections opened in `startup()`
- [ ] Event subscriptions done in `startup()`
- [ ] `self.sleep()` used (not `time.sleep()`) in `runConcurrentThread()`
- [ ] `self.StopThread` exception caught in `runConcurrentThread()`
- [ ] All exceptions handled in concurrent thread
- [ ] Connections closed in `shutdown()`
- [ ] Files and sockets closed in `shutdown()`
- [ ] Event subscriptions cancelled in `shutdown()`

## Related Documentation

- [Device Development](devices.md) - Device lifecycle callbacks and patterns
- [State Management](state-management.md) - Managing device states
- [Configuration Validation](../api/ui-validation.md) - Validating user input

## Official References

- [Plugin Developer's Guide - Plugin Lifecycle](https://www.indigodomo.com/docs/plugin_guide#plugin_lifecycle)
- [Plugin Developer's Guide - Concurrent Thread](https://www.indigodomo.com/docs/plugin_guide#concurrent_thread)
- [Object Model Reference - Plugin Class](https://www.indigodomo.com/docs/object_model_reference#plugin)
