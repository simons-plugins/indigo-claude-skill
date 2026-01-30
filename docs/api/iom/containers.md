# indigo.Dict and indigo.List

Indigo provides special container classes that integrate with the Indigo database and preference system.

## Key Differences from Python Containers

| Behavior | `indigo.Dict`/`indigo.List` | Python `dict`/`list` |
|----------|----------------------------|----------------------|
| Value retrieval | Returns **copy** | Returns **reference** |
| Nested modification | Must reassign parent | Modifies in place |
| Database integration | Native | Requires conversion |
| Key restrictions | ASCII only, no spaces | Any hashable |

## indigo.Dict

### Basic Usage

```python
d = indigo.Dict()
d['key'] = "value"
d.key = "value"      # Dot notation also works
value = d['key']
value = d.key
value = d.get('key', 'default')

if 'key' in d:
    pass
```

### Key Restrictions

Keys must:
- Contain only letters, numbers, and ASCII characters
- NOT contain spaces
- NOT start with a number or punctuation
- NOT start with "xml", "XML", or "Xml"

### Value Type Restrictions

Values must be: `bool`, `float`, `int`, `string`, `list`, or `dict`

Nested containers must recursively contain only compatible values.

## indigo.List

```python
c = indigo.List()
c.append(4)
c.append("string")
c.append(True)

for item in c:
    print(item)
```

## Critical: Copy Semantics

**Values are always retrieved as copies, not references.**

### The Gotcha

```python
c = indigo.List()
c.append(4)
c.append(5)

a = indigo.Dict()
a['c'] = c          # COPY of c is inserted

# This does NOT modify a['c']:
c.append(6)         # Only modifies local c
print(a['c'])       # Still [4, 5]

# This also does NOT work:
a['c'].append(6)    # Gets copy, appends to copy, copy discarded
print(a['c'])       # Still [4, 5]
```

### The Solution: Reassign

```python
# Must reassign to parent container:
c.append(6)
a['c'] = c          # Now a['c'] has [4, 5, 6]
```

## Efficient Nested Access

Avoid creating temporary copies with helper methods:

### setitem_in_item()

```python
# Slow - creates temporary copy of a['c']:
temp = a['c']
temp[4] = "value"
a['c'] = temp

# Fast - no temporary copy:
a.setitem_in_item('c', 4, "value")
```

### getitem_in_item()

```python
# Slow - creates temporary copy:
value = a['c'][4]

# Fast - no temporary copy:
value = a.getitem_in_item('c', 4)
```

## Converting to Native Python

### to_dict() / to_list()

Recursively converts nested structures:

```python
python_dict = my_indigo_dict.to_dict()
python_list = my_indigo_list.to_list()
```

### Native Conversion (Indigo 2021.2+)

```python
python_dict = dict(my_indigo_dict)
python_list = list(my_indigo_list)
```

## Common Use Cases

### Plugin Properties

```python
# Read plugin props (returns indigo.Dict)
props = dev.pluginProps

# Modify and save
props['setting'] = "new value"
dev.replacePluginPropsOnServer(props)
```

### Device States

```python
# Access states (returns indigo.Dict)
states = dev.states
current_value = states['myState']
```

### Config UI Values

```python
def validateDeviceConfigUi(self, valuesDict, typeId, devId):
    # valuesDict is an indigo.Dict
    if not valuesDict.get('requiredField'):
        errorsDict = indigo.Dict()
        errorsDict['requiredField'] = "This field is required"
        return (False, valuesDict, errorsDict)
    return (True, valuesDict)
```
