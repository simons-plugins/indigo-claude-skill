# Utility Classes and Functions

The `indigo.utils` module provides helper classes and functions.

## Classes

### FileNotFoundError

Exception for file operations:

```python
try:
    # file operation
    pass
except indigo.utils.FileNotFoundError:
    self.logger.error("File not found")
```

### IndigoJSONEncoder

JSON encoder that handles Python date/time objects:

```python
import json

dev = indigo.devices[123456]
dev_dict = dict(dev)

# Properly encodes datetime objects
json_str = json.dumps(dev_dict, indent=4, cls=indigo.utils.IndigoJSONEncoder)
```

## Functions

### return_static_file()

Returns a file for the Indigo Web Server to serve:

```python
indigo.utils.return_static_file("relative/path/to/file.html")

indigo.utils.return_static_file(
    "/absolute/path/to/file.json",
    status=200,
    path_is_relative=False,
    content_type="application/json"
)
```

**Parameters:**

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `file_path` | Yes | str | Path to file |
| `status` | No | int | HTTP status code (default: 200) |
| `path_is_relative` | No | bool | Relative to plugin (default: True) |
| `content_type` | No | str | MIME type (auto-detected if omitted) |

**Returns:** `indigo.Dict` for IWS to process:

```python
{
    "status": 200,
    "headers": {"Content-Type": "text/html"},
    "file_path": "/full/path/to/file.html"
}
```

**Raises:** `FileNotFoundError` or `TypeError`

### validate_email_address()

Validates email address format:

```python
if indigo.utils.validate_email_address("user@example.com"):
    # Valid format
    pass
```

**Note:** Validates format only, not whether the address exists.

### str_to_bool()

Converts boolean-like strings to actual booleans:

```python
indigo.utils.str_to_bool("yes")     # True
indigo.utils.str_to_bool("no")      # False
indigo.utils.str_to_bool("on")      # True
indigo.utils.str_to_bool("off")     # False
indigo.utils.str_to_bool("open")    # True
indigo.utils.str_to_bool("closed")  # False
```

**Recognized mappings:**

| True | False |
|------|-------|
| y | n |
| yes | no |
| t | f |
| true | false |
| on | off |
| 1 | 0 |
| open | closed |
| locked | unlocked |

**Raises:** `ValueError` if string cannot be converted.

### reverse_bool_str_value()

Returns the opposite boolean string:

```python
indigo.utils.reverse_bool_str_value("open")    # "closed"
indigo.utils.reverse_bool_str_value("yes")     # "no"
indigo.utils.reverse_bool_str_value("locked")  # "unlocked"
```

**Raises:** `ValueError` if string not recognized.

## Common Use Cases

### Serving Static Files from HTTP Responder

```python
def handleWebRequest(self, path, params):
    if path == "/status":
        return indigo.utils.return_static_file("static/status.html")
    elif path == "/data.json":
        return indigo.utils.return_static_file("static/data.json")
    else:
        return indigo.utils.return_static_file(
            "static/404.html",
            status=404
        )
```

### Validating Email in Config UI

```python
def validatePrefsConfigUi(self, valuesDict):
    errorsDict = indigo.Dict()

    email = valuesDict.get("notificationEmail", "")
    if email and not indigo.utils.validate_email_address(email):
        errorsDict["notificationEmail"] = "Invalid email format"

    if errorsDict:
        return (False, valuesDict, errorsDict)
    return (True, valuesDict)
```

### Converting User Input

```python
def processUserSetting(self, value_str):
    try:
        enabled = indigo.utils.str_to_bool(value_str)
        return enabled
    except ValueError:
        self.logger.warning(f"Unrecognized value: {value_str}")
        return False
```

### Serializing Device State

```python
import json

def getDeviceStateAsJson(self, dev):
    dev_dict = dict(dev)
    return json.dumps(dev_dict, cls=indigo.utils.IndigoJSONEncoder)
```
