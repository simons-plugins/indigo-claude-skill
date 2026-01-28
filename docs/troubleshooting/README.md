# Troubleshooting

Common issues, debugging techniques, and solutions for Indigo plugin development.

## Quick Debugging Checklist

When your plugin isn't working:

1. ✅ Check the Event Log (`View → Event Log Window`)
2. ✅ Enable debug logging in plugin config
3. ✅ Verify `CFBundleIdentifier` is unique
4. ✅ Check `ServerApiVersion` matches (3.0 for Python 3)
5. ✅ Restart Indigo after code changes
6. ✅ Look for Python exceptions in Event Log

## Common Issues

### Plugin Won't Load

**Symptoms**: Plugin doesn't appear in Plugins menu, or shows as "Error Loading Plugin"

**Causes**:
- Syntax error in plugin.py
- Missing or malformed Info.plist
- Wrong ServerApiVersion
- Import error (missing module)

**Solutions**:
```bash
# Check Python syntax
python3 -m py_compile plugin.py

# Verify Info.plist
plutil -lint Info.plist

# Check Event Log for specific error
```

### Plugin Crashes on Startup

**Symptoms**: Plugin loads but immediately disables

**Common causes**:
- Exception in `__init__()` or `startup()`
- Indigo API calls in `__init__()` (not allowed)
- Network/API calls that fail immediately

**Debug approach**:
```python
def startup(self):
    try:
        super().startup()
        self.logger.debug("Startup: step 1")
        # ... your code ...
        self.logger.debug("Startup: step 2")
    except Exception as exc:
        self.logger.exception("Startup failed")
        raise
```

### Devices Not Updating

**Symptoms**: Device states don't change, or update slowly

**Common causes**:
- Not calling `updateStatesOnServer()` or `updateStateOnServer()`
- Concurrent thread crashed
- API calls timing out
- Rate limiting

**Check**:
```python
# Enable thread debugging
def runConcurrentThread(self):
    self.logger.debug("Thread starting")
    while True:
        self.logger.threaddebug("Thread loop")
        # ... update code ...
        self.sleep(60)
```

### Configuration Won't Save

**Symptoms**: Config dialog closes but settings aren't applied

**Common causes**:
- Validation callback returning False
- Not returning proper tuple from `validatePrefsConfigUi()`
- Missing fields in PluginConfig.xml

**Check**:
```python
def validatePrefsConfigUi(self, valuesDict):
    self.logger.debug(f"Validating: {valuesDict}")
    errorsDict = indigo.Dict()
    # ... validation ...
    self.logger.debug(f"Errors: {errorsDict}")
    return (len(errorsDict) == 0, valuesDict, errorsDict)
```

## Debugging Techniques

### Enable Debug Logging

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.debug = True  # Force debug on
```

### Log Everything

```python
def deviceStartComm(self, dev):
    self.logger.debug(f"deviceStartComm: {dev.name} (id: {dev.id})")
    self.logger.debug(f"  address: {dev.address}")
    self.logger.debug(f"  model: {dev.model}")
    self.logger.debug(f"  states: {dev.states}")
    super().deviceStartComm(dev)
```

### Use Exception Logging

```python
try:
    response = requests.get(url)
    response.raise_for_status()
except Exception as exc:
    self.logger.exception("API call failed")  # Includes stack trace
```

### Test in Python Interpreter

```python
# Test API parsing outside of Indigo
import json
response_text = '{"status": "ok", "data": [...]}'
data = json.loads(response_text)
print(data['data'][0])
```

## Performance Issues

### Plugin Slowing Down Indigo

**Symptoms**: Indigo becomes sluggish when plugin is running

**Common causes**:
- Too frequent polling
- Blocking operations in callbacks
- Memory leaks
- Too many state updates

**Solutions**:
- Increase polling interval
- Use `self.sleep()` properly
- Batch state updates
- Profile memory usage

### High Memory Usage

```python
# Check for leaks - log memory usage
import sys
def runConcurrentThread(self):
    while True:
        self.logger.debug(f"Devices in memory: {len(self.devices_dict)}")
        # ... update logic ...
        self.sleep(300)
```

## Documentation Needed

We need community contributions for:

- [ ] XML validation errors
- [ ] Device model mismatches
- [ ] State update timing issues
- [ ] Thread synchronization problems
- [ ] API rate limiting strategies
- [ ] Memory leak detection
- [ ] Performance profiling
- [ ] UI callback issues

## Contributing

Encountered a tricky issue and solved it? Document it here!

Good troubleshooting docs include:
- Clear symptom description
- Root cause explanation
- Step-by-step solution
- How to prevent it
- Code examples

See [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Getting Help

If you can't solve your issue:

1. 📋 Check [Indigo Developer Forum](https://forums.indigodomo.com/viewforum.php?f=18)
2. 💬 Ask in [GitHub Discussions](https://github.com/indigo-community/indigo-skill/discussions)
3. 📖 Review [Official Docs](https://www.indigodomo.com/docs/plugin_guide)
4. 📧 Contact Indigo support for platform issues
