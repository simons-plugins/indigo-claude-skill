# Common Issues and Troubleshooting

## Plugin Won't Start

### Plugin Not Appearing in Indigo

**Symptoms**: Plugin doesn't show up in Plugins menu

**Causes & Solutions**:

1. **Wrong Location**
   ```bash
   # Plugins should be in one of these locations:
   ~/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins/
   ~/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins (Disabled)/
   ```

2. **Bundle Extension Wrong**
   - Must be `.indigoPlugin` (not `.plugin` or `.indigoplugin`)

3. **Info.plist Invalid**
   - Check XML syntax is valid
   - Ensure required keys present: `CFBundleIdentifier`, `ServerApiVersion`, `PluginVersion`

4. **Restart Indigo**
   - Quit and restart Indigo server completely

### Plugin Won't Enable

**Symptoms**: Plugin appears but can't be enabled or immediately disables

**Check Event Log** for errors:

1. **Python Syntax Errors**
   ```
   Error: File "plugin.py", line 42
       print "hello"
                   ^
   SyntaxError: Missing parentheses in call to 'print'
   ```
   - Fix Python 3 syntax (see [Python 3 Migration](../IndigoSDK-2025.1/Updating%20to%20API%20version%203.0%20(Python%203).md))

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'requests'
   ```
   - Install missing package to `Contents/Packages/` directory
   - Don't rely on system Python packages

3. **API Version Mismatch**
   ```
   Error: Plugin requires API version 3.0 but server is running 2.5
   ```
   - Update Indigo or change `ServerApiVersion` in Info.plist

4. **Duplicate Bundle Identifier**
   ```
   Error: Plugin with bundle ID com.example.plugin already loaded
   ```
   - Change `CFBundleIdentifier` to unique value

### Plugin Crashes on Startup

**Check for**:

1. **Accessing Indigo Database in `__init__`**
   ```python
   # WRONG
   def __init__(self, ...):
       super().__init__(...)
       self.dev = indigo.devices["MyDevice"]  # Too early!

   # RIGHT
   def __init__(self, ...):
       super().__init__(...)

   def startup(self):
       self.dev = indigo.devices["MyDevice"]  # Safe here
   ```

2. **Not Calling `super().__init__()`**
   ```python
   def __init__(self, ...):
       super().__init__(...)  # MUST be here
   ```

3. **Exception in startup()**
   ```python
   def startup(self):
       try:
           # Your code
       except Exception as e:
           self.logger.exception(e)  # Log it!
   ```

## Device Issues

### Device Won't Create

**Check**:

1. **Device type ID matches Devices.xml**
   ```python
   # In code:
   dev = indigo.device.create(..., deviceTypeId="myDeviceType")

   # In Devices.xml:
   <Device type="custom" id="myDeviceType">
   ```

2. **Required configuration fields**
   - Implement `validateDeviceConfigUi()` to catch config errors

### Device States Not Updating

**Common causes**:

1. **State ID doesn't match Devices.xml**
   ```python
   # In code:
   dev.updateStateOnServer('temperature', value=72)

   # Must match Devices.xml:
   <State id="temperature">
   ```

2. **Device not enabled**
   ```python
   if dev.enabled:
       dev.updateStateOnServer(...)
   ```

3. **State type mismatch**
   ```python
   # State defined as Integer in XML
   dev.updateStateOnServer('temp', value="72")  # WRONG - should be int
   dev.updateStateOnServer('temp', value=72)    # RIGHT
   ```

### Device State List Changes Not Appearing

**Solution**: Call after changing Devices.xml:
```python
def deviceStartComm(self, dev):
    dev.stateListOrDisplayStateIdChanged()  # Refresh states
```

## Threading Issues

### Plugin Won't Shut Down Cleanly

**Cause**: `runConcurrentThread()` not using `self.sleep()`

```python
# WRONG
def runConcurrentThread(self):
    while True:
        self.poll_devices()
        time.sleep(60)  # Blocks shutdown!

# RIGHT
def runConcurrentThread(self):
    try:
        while True:
            self.poll_devices()
            self.sleep(60)  # Allows interruption
    except self.StopThread:
        pass  # Clean shutdown
```

### Thread Exits Prematurely

**Cause**: `runConcurrentThread()` returning instead of looping

```python
# WRONG
def runConcurrentThread(self):
    self.poll_devices()  # Runs once and exits!

# RIGHT
def runConcurrentThread(self):
    try:
        while True:
            self.poll_devices()
            self.sleep(60)
    except self.StopThread:
        pass
```

## Configuration UI Issues

### Dynamic List Not Updating

**Solution**: Add `dynamicReload="true"` to field:
```xml
<Field id="deviceList" type="menu">
    <List class="self" method="get_devices" dynamicReload="true"/>
</Field>
```

### Validation Not Working

**Check**:

1. **Return tuple format**
   ```python
   def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
       errors_dict = indigo.Dict()

       if error_condition:
           errors_dict['fieldId'] = "Error message"
           return (False, values_dict, errors_dict)  # Note the tuple

       return (True, values_dict)  # Success tuple
   ```

2. **Field IDs match**
   ```python
   # Error dict key must match field ID in XML
   errors_dict['address'] = "Invalid address"
   ```

### Changes Not Saving

**Cause**: Returning `False` instead of tuple from validation:
```python
# WRONG
def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
    return True  # Wrong return type

# RIGHT
def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
    return (True, values_dict)  # Correct tuple
```

## Python 3 Issues

### Common Migration Errors

See [Python 3 Migration Guide](../IndigoSDK-2025.1/Updating%20to%20API%20version%203.0%20(Python%203).md) for complete list.

**Most Common**:

1. **Print statements**
   ```python
   # Python 2
   print "hello"

   # Python 3
   print("hello")
   ```

2. **Exception syntax**
   ```python
   # Python 2
   except Exception, e:

   # Python 3
   except Exception as e:
   ```

3. **Unicode/String**
   ```python
   # Python 2
   isinstance(s, unicode)

   # Python 3
   # All strings are unicode, just use str
   isinstance(s, str)
   ```

4. **Dictionary iteration**
   ```python
   # Python 2
   for k, v in d.iteritems():

   # Python 3
   for k, v in d.items():
   ```

5. **State image constant**
   ```python
   # Python 2
   indigo.kStateImageSel.None

   # Python 3
   indigo.kStateImageSel.NoImage
   ```

## HTTP Responder Issues

### 404 Errors

**Check URL format**:
```
http://localhost:8176/message/{bundle_id}/{method_name}/...
```

**Example**:
```
http://localhost:8176/message/com.example.plugin/api/device.json
```

### Method Not Called

**Verify**:

1. **Method signature correct**
   ```python
   def my_handler(self, action, dev=None, caller_waiting_for_result=None):
       reply = indigo.Dict()
       reply["content"] = "response"
       reply["status"] = 200
       return reply
   ```

2. **Return dict with required keys**
   - `status` - HTTP status code
   - `content` - Response body
   - `headers` (optional) - Dict of HTTP headers

## Performance Issues

### Slow Plugin

**Check**:

1. **Polling too frequently**
   ```python
   # Too fast
   self.sleep(1)  # Every second

   # Better
   self.sleep(30)  # Every 30 seconds
   ```

2. **Too many state updates**
   ```python
   # SLOW - 5 separate database writes
   dev.updateStateOnServer('state1', value=1)
   dev.updateStateOnServer('state2', value=2)
   dev.updateStateOnServer('state3', value=3)
   dev.updateStateOnServer('state4', value=4)
   dev.updateStateOnServer('state5', value=5)

   # FAST - 1 database write
   dev.updateStatesOnServer([
       {'key': 'state1', 'value': 1},
       {'key': 'state2', 'value': 2},
       {'key': 'state3', 'value': 3},
       {'key': 'state4', 'value': 4},
       {'key': 'state5', 'value': 5},
   ])
   ```

3. **Unnecessary device iteration**
   ```python
   # Iterates ALL devices in Indigo
   for dev in indigo.devices:

   # Only your plugin's devices
   for dev in indigo.devices.iter("self"):
   ```

### High CPU Usage

**Causes**:

1. **Tight loop without sleep**
   ```python
   # WRONG
   while True:
       do_work()  # No delay!

   # RIGHT
   while True:
       do_work()
       self.sleep(0.1)  # Give CPU a break
   ```

2. **Inefficient polling**
   - Poll less frequently
   - Use event subscriptions instead of polling when possible

## Debugging Tips

### Enable Debug Logging

```python
def __init__(self, ...):
    super().__init__(...)
    self.debug = True  # Enable debug logging

def some_method(self):
    self.logger.debug("Debug message")
    self.logger.info("Info message")
    self.logger.warning("Warning message")
    self.logger.error("Error message")
```

### Log Exceptions

```python
try:
    risky_operation()
except Exception as e:
    self.logger.exception(e)  # Logs full traceback
```

### Inspect Objects

```python
# Log device properties
self.logger.debug(f"Device: {dev.name}, ID: {dev.id}")
self.logger.debug(f"States: {dev.states}")
self.logger.debug(f"Props: {dev.pluginProps}")

# Convert to dict for JSON logging
import json
dev_dict = dict(dev)
self.logger.debug(json.dumps(dev_dict, indent=2, cls=indigo.utils.JSONDateEncoder))
```

### Check Indigo Event Log

All plugin output goes to Indigo Event Log window:
- **View** → **Event Log Window**
- Filter by your plugin name
- Look for ERROR and WARNING messages

### Use Indigo Debugger

Add breakpoint in code:
```python
indigo.debugger()  # Execution pauses here
```

Then use Indigo's Script Debugger to step through code.

## Getting Help

1. **Search Developer Forum**: https://forums.indigodomo.com/viewforum.php?f=18
2. **Post in Forum** with:
   - Indigo version
   - macOS version
   - Python version
   - Full error message from Event Log
   - Relevant code snippet
3. **Check Example Plugins** in SDK
4. **Review Official Docs**: https://www.indigodomo.com/docs/documents#technical_documents

## Official Resources

- [Plugin Developer's Guide](https://www.indigodomo.com/docs/plugin_guide)
- [Object Model Reference](https://www.indigodomo.com/docs/object_model_reference)
- [Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)
