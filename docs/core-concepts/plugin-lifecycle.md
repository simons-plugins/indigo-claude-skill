# Plugin Lifecycle

Understanding the plugin lifecycle is essential for proper plugin development.

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
    shutdown()
         ↓
   Plugin Disabled/Indigo Quit
```

## Lifecycle Methods

### `__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)`

**When**: Plugin object is created

**Purpose**: Initialize instance variables ONLY

**Rules**:
- ✅ Set instance variables
- ✅ Initialize data structures
- ❌ NO Indigo API calls
- ❌ NO network requests
- ❌ NO device communication

```python
def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
    super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

    # Initialize instance variables
    self.debug = pluginPrefs.get("showDebugInfo", False)
    self.api_key = pluginPrefs.get("apiKey", "")
    self.devices_dict = {}

    # Set up logging
    if self.debug:
        self.logger.debug("Debug logging enabled")
```

### `startup()`

**When**: After `__init__()`, before plugin runs

**Purpose**: Initialize resources, subscribe to events, start connections

**Rules**:
- ✅ Call `super().startup()` first
- ✅ Initialize API connections
- ✅ Subscribe to Indigo events
- ✅ Load persistent data
- ✅ Validate configuration

```python
def startup(self):
    super().startup()

    self.logger.info(f"{self.pluginDisplayName} starting")

    # Initialize API client
    self.api_client = APIClient(self.api_key)

    # Subscribe to device updates
    indigo.devices.subscribeToChanges()

    # Load saved state
    self._load_state()
```

### `runConcurrentThread()` (Optional)

**When**: Starts after `startup()`, runs continuously

**Purpose**: Background tasks like polling APIs, periodic updates

**Rules**:
- ✅ Use `self.sleep()` NOT `time.sleep()`
- ✅ Catch `self.StopThread` exception
- ✅ Handle exceptions to prevent thread exit
- ✅ Use reasonable sleep intervals

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
        pass  # Normal shutdown
```

**Polling Best Practices**:
- Use configurable intervals
- Respect API rate limits
- Log errors but don't crash the thread
- Use `self.sleep()` for interruptible waits

### `shutdown()`

**When**: Plugin is being disabled or Indigo is quitting

**Purpose**: Clean up resources, close connections, save state

**Rules**:
- ✅ Clean up connections
- ✅ Save persistent data
- ✅ Unsubscribe from events
- ✅ Call `super().shutdown()` last (optional but recommended)

```python
def shutdown(self):
    self.logger.info(f"{self.pluginDisplayName} shutting down")

    # Save state
    self._save_state()

    # Close API connections
    if hasattr(self, 'api_client'):
        self.api_client.close()

    # Unsubscribe from changes
    indigo.devices.unsubscribeToChanges()

    super().shutdown()
```

## Device Lifecycle Callbacks

These are called for each device as it starts/stops:

### `deviceStartComm(dev)`

**When**: Device is enabled or plugin starts with device already enabled

```python
def deviceStartComm(self, dev):
    super().deviceStartComm(dev)

    self.logger.info(f"Starting device: {dev.name}")

    # Initialize device-specific resources
    self.devices_dict[dev.id] = {
        'last_update': None,
        'retry_count': 0
    }

    # Set initial state
    dev.updateStateOnServer("onOffState", False)
```

### `deviceStopComm(dev)`

**When**: Device is disabled or plugin is shutting down

```python
def deviceStopComm(self, dev):
    super().deviceStopComm(dev)

    self.logger.info(f"Stopping device: {dev.name}")

    # Clean up device-specific resources
    if dev.id in self.devices_dict:
        del self.devices_dict[dev.id]
```

### `deviceUpdated(origDev, newDev)`

**When**: Device properties are changed in Indigo

```python
def deviceUpdated(self, origDev, newDev):
    super().deviceUpdated(origDev, newDev)

    # Only process changes to our plugin's devices
    if newDev.pluginId == self.pluginId:
        # Check if relevant properties changed
        if origDev.address != newDev.address:
            self.logger.info(f"Device {newDev.name} address changed")
            self._reinitialize_device(newDev)
```

## Common Patterns

### Deferred Initialization

Sometimes you need to wait for configuration before initializing:

```python
def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
    super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
    self.api_client = None  # Will initialize in startup()

def startup(self):
    super().startup()

    api_key = self.pluginPrefs.get("apiKey", "")
    if api_key:
        self.api_client = APIClient(api_key)
    else:
        self.logger.error("No API key configured")
```

### Graceful Shutdown

Ensure cleanup happens even on errors:

```python
def shutdown(self):
    try:
        self._save_state()
    except Exception as exc:
        self.logger.exception("Error saving state")

    try:
        if self.api_client:
            self.api_client.close()
    except Exception as exc:
        self.logger.exception("Error closing API client")

    super().shutdown()
```

### Polling with Rate Limiting

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

## Debugging Lifecycle Issues

### Enable Debug Logging

```python
def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
    super().__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
    self.debug = True  # Force debug on

def startup(self):
    super().startup()
    self.logger.debug("Startup called")
```

### Log Lifecycle Events

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.logger.debug("__init__ called")

def startup(self):
    super().startup()
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
    super().shutdown()
```

## Common Mistakes

### ❌ API Calls in `__init__()`

```python
# WRONG - __init__ should not make API calls
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.data = requests.get(url).json()  # DON'T DO THIS!
```

### ❌ Forgetting to Call `super()`

```python
# WRONG - Always call super()
def startup(self):
    self.logger.info("Starting")  # super().startup() not called!
```

### ❌ Using `time.sleep()` in Concurrent Thread

```python
# WRONG - Blocks shutdown
def runConcurrentThread(self):
    while True:
        time.sleep(60)  # Can't be interrupted!

# RIGHT - Allows clean shutdown
def runConcurrentThread(self):
    try:
        while True:
            self.sleep(60)  # Interruptible
    except self.StopThread:
        pass
```

### ❌ Crashing the Concurrent Thread

```python
# WRONG - Exception kills thread
def runConcurrentThread(self):
    while True:
        self._update_devices()  # Uncaught exception stops thread
        self.sleep(60)

# RIGHT - Thread keeps running
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

## See Also

- [Device Types](device-types.md) - Different types of devices you can create
- [State Management](state-management.md) - Managing device states
- [Error Handling](../patterns/error-handling.md) - Robust error handling patterns
