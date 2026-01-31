# Plugin Preferences

Plugin preferences store persistent configuration that survives plugin restarts.

## Overview

- Preferences are automatically saved to disk
- Available via `self.pluginPrefs` dictionary
- Fields in `PluginConfig.xml` map to `pluginPrefs` automatically
- Can store: numbers, booleans, strings, `indigo.Dict()`, `indigo.List()`

## Reading Preferences

```python
# Direct access (raises KeyError if missing)
api_key = self.pluginPrefs["apiKey"]

# Safe access with default
debug = self.pluginPrefs.get("showDebugInfo", False)
interval = self.pluginPrefs.get("pollingInterval", 60)
```

## Writing Preferences

```python
# Set/update a preference
self.pluginPrefs["lastUpdate"] = str(datetime.now())
self.pluginPrefs["retryCount"] = 5
self.pluginPrefs["cachedData"] = {"key": "value"}

# Preferences auto-save, but force immediate save:
indigo.server.savePluginPrefs()
```

## PluginConfig.xml Integration

Fields defined in `PluginConfig.xml` automatically map to `pluginPrefs`:

```xml
<?xml version="1.0"?>
<PluginConfig>
    <Field id="apiKey" type="textfield">
        <Label>API Key:</Label>
    </Field>
    <Field id="pollingInterval" type="textfield" defaultValue="60">
        <Label>Polling Interval (seconds):</Label>
    </Field>
    <Field id="showDebugInfo" type="checkbox" defaultValue="false">
        <Label>Enable Debug Logging:</Label>
    </Field>
</PluginConfig>
```

Access in plugin:

```python
def startup(self):
    api_key = self.pluginPrefs.get("apiKey", "")
    interval = int(self.pluginPrefs.get("pollingInterval", 60))
    debug = self.pluginPrefs.get("showDebugInfo", False)
```

## Hidden Preferences

Store values not shown in the config UI:

```python
def startup(self):
    # Read hidden prefs
    self.last_sync = self.pluginPrefs.get("_lastSync", None)

def _after_sync(self):
    # Store hidden prefs
    self.pluginPrefs["_lastSync"] = str(datetime.now())
    self.pluginPrefs["_syncCount"] = self.pluginPrefs.get("_syncCount", 0) + 1
```

## Validating Preferences

```python
def validatePrefsConfigUi(self, valuesDict):
    """Validate plugin preferences before saving."""
    errorsDict = indigo.Dict()

    # Validate API key
    api_key = valuesDict.get("apiKey", "").strip()
    if not api_key:
        errorsDict["apiKey"] = "API key is required"

    # Validate polling interval
    try:
        interval = int(valuesDict.get("pollingInterval", 60))
        if interval < 10:
            errorsDict["pollingInterval"] = "Minimum is 10 seconds"
    except ValueError:
        errorsDict["pollingInterval"] = "Must be a number"

    if errorsDict:
        return (False, valuesDict, errorsDict)

    return (True, valuesDict)
```

## Preference Change Callback

React when preferences are saved:

```python
def closedPrefsConfigUi(self, valuesDict, userCancelled):
    """Called after preferences dialog closes."""
    if userCancelled:
        return

    # Apply new settings
    self.debug = valuesDict.get("showDebugInfo", False)

    # Reinitialize if API key changed
    if valuesDict.get("apiKey") != self.api_key:
        self.api_key = valuesDict.get("apiKey")
        self._reinitialize_api_client()
```

## Common Patterns

### Caching API Data

```python
def _fetch_data(self):
    """Fetch data with caching."""
    cached = self.pluginPrefs.get("_cachedData")
    cache_time = self.pluginPrefs.get("_cacheTime")

    # Check cache validity (1 hour)
    if cached and cache_time:
        if datetime.now() - datetime.fromisoformat(cache_time) < timedelta(hours=1):
            return cached

    # Fetch fresh data
    data = self.api_client.get_data()

    # Update cache
    self.pluginPrefs["_cachedData"] = data
    self.pluginPrefs["_cacheTime"] = datetime.now().isoformat()

    return data
```

### Tracking Statistics

```python
def _on_successful_action(self):
    """Track usage statistics in preferences."""
    self.pluginPrefs["_successCount"] = self.pluginPrefs.get("_successCount", 0) + 1
    self.pluginPrefs["_lastSuccess"] = str(datetime.now())

def _on_failed_action(self, error):
    """Track errors in preferences."""
    self.pluginPrefs["_errorCount"] = self.pluginPrefs.get("_errorCount", 0) + 1
    self.pluginPrefs["_lastError"] = str(error)
```

### Migration Between Versions

```python
def startup(self):
    # Check preference version
    pref_version = self.pluginPrefs.get("_prefVersion", 1)

    if pref_version < 2:
        # Migrate old format to new
        if "oldKey" in self.pluginPrefs:
            self.pluginPrefs["newKey"] = self.pluginPrefs["oldKey"]
            del self.pluginPrefs["oldKey"]
        self.pluginPrefs["_prefVersion"] = 2
```

## Best Practices

- Use `get()` with defaults for safe access
- Prefix hidden preferences with underscore (`_cacheTime`)
- Validate all user input in `validatePrefsConfigUi()`
- React to changes in `closedPrefsConfigUi()`
- Don't store sensitive data like passwords in plain text

## See Also

- [Plugin Lifecycle](plugin-lifecycle.md) - When to access preferences
- [Device Development](devices.md) - Device-specific configuration (pluginProps)
