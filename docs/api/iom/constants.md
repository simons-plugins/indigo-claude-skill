# Constants Reference

## State Image Icons

Used with `dev.updateStateImageOnServer()`:

```python
dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
```

| Constant | Use Case |
|----------|----------|
| `indigo.kStateImageSel.Auto` | Automatic selection |
| `indigo.kStateImageSel.NoImage` | No icon |
| `indigo.kStateImageSel.Error` | Error state |

### Dimmer/Relay Icons

| Constant |
|----------|
| `indigo.kStateImageSel.DimmerOff` |
| `indigo.kStateImageSel.DimmerOn` |
| `indigo.kStateImageSel.PowerOff` |
| `indigo.kStateImageSel.PowerOn` |

### Sensor Icons

| Constant |
|----------|
| `indigo.kStateImageSel.SensorOff` |
| `indigo.kStateImageSel.SensorOn` |
| `indigo.kStateImageSel.SensorTripped` |
| `indigo.kStateImageSel.MotionSensor` |
| `indigo.kStateImageSel.MotionSensorTripped` |
| `indigo.kStateImageSel.LightSensor` |
| `indigo.kStateImageSel.LightSensorOn` |

### HVAC Icons

| Constant |
|----------|
| `indigo.kStateImageSel.HvacOff` |
| `indigo.kStateImageSel.HvacHeatMode` |
| `indigo.kStateImageSel.HvacCoolMode` |
| `indigo.kStateImageSel.HvacAutoMode` |
| `indigo.kStateImageSel.HvacFanMode` |

### Fan Icons

| Constant |
|----------|
| `indigo.kStateImageSel.FanOff` |
| `indigo.kStateImageSel.FanLow` |
| `indigo.kStateImageSel.FanMedium` |
| `indigo.kStateImageSel.FanHigh` |

### Media Icons

| Constant |
|----------|
| `indigo.kStateImageSel.AvPaused` |
| `indigo.kStateImageSel.AvPlaying` |
| `indigo.kStateImageSel.AvStopped` |

### Lock Icons

| Constant |
|----------|
| `indigo.kStateImageSel.Locked` |
| `indigo.kStateImageSel.Unlocked` |

### Sprinkler Icons

| Constant |
|----------|
| `indigo.kStateImageSel.SprinklerOff` |
| `indigo.kStateImageSel.SprinklerOn` |

### Timer Icons

| Constant |
|----------|
| `indigo.kStateImageSel.TimerOff` |
| `indigo.kStateImageSel.TimerOn` |

## Device Action Constants

### Relay/Dimmer Actions

```python
indigo.kDeviceAction.TurnOn
indigo.kDeviceAction.TurnOff
indigo.kDeviceAction.Toggle
indigo.kDeviceAction.SetBrightness
indigo.kDeviceAction.BrightenBy
indigo.kDeviceAction.DimBy
indigo.kDeviceAction.RequestStatus
```

### Thermostat Actions

```python
indigo.kThermostatAction.SetHeatSetpoint
indigo.kThermostatAction.SetCoolSetpoint
indigo.kThermostatAction.SetHvacMode
indigo.kThermostatAction.SetFanMode
indigo.kThermostatAction.RequestStatusAll
```

### Sensor Actions

```python
indigo.kSensorAction.TurnOn
indigo.kSensorAction.TurnOff
indigo.kSensorAction.RequestStatus
```

### Sprinkler Actions

```python
indigo.kSprinklerAction.ZoneOn
indigo.kSprinklerAction.ZoneOff
indigo.kSprinklerAction.AllZonesOff
indigo.kSprinklerAction.RunNewSchedule
indigo.kSprinklerAction.RunPreviousSchedule
indigo.kSprinklerAction.PauseSchedule
indigo.kSprinklerAction.ResumeSchedule
indigo.kSprinklerAction.StopSchedule
```

### Speed Control Actions

```python
indigo.kSpeedControlAction.TurnOn
indigo.kSpeedControlAction.TurnOff
indigo.kSpeedControlAction.Toggle
indigo.kSpeedControlAction.SetSpeedLevel
indigo.kSpeedControlAction.SetSpeedIndex
indigo.kSpeedControlAction.IncreaseSpeedIndex
indigo.kSpeedControlAction.DecreaseSpeedIndex
```

## Protocol Constants

```python
indigo.kProtocol.Plugin     # Plugin-defined device
indigo.kProtocol.Insteon    # INSTEON protocol
indigo.kProtocol.X10        # X10 protocol
indigo.kProtocol.ZWave      # Z-Wave protocol
```

## HVAC Mode Constants

```python
indigo.kHvacMode.Off
indigo.kHvacMode.Heat
indigo.kHvacMode.Cool
indigo.kHvacMode.HeatCool       # Auto mode
indigo.kHvacMode.ProgramHeat
indigo.kHvacMode.ProgramCool
indigo.kHvacMode.ProgramHeatCool
```

## Fan Mode Constants

```python
indigo.kFanMode.Auto
indigo.kFanMode.AlwaysOn
```

## State Value Types

Used in `Devices.xml` state definitions:

| Type | Description |
|------|-------------|
| `Integer` | Whole numbers |
| `Number` | Floating point |
| `String` | Text values |
| `Boolean` | True/False |
| `Separator` | UI separator (no value) |

## UI Value Types

Used in `ConfigUI` field definitions:

| Type | Description |
|------|-------------|
| `textfield` | Single-line text input |
| `textarea` | Multi-line text input |
| `checkbox` | Boolean checkbox |
| `menu` | Dropdown menu |
| `list` | Selection list |
| `button` | Action button |
| `label` | Static text |
| `separator` | Visual separator |
