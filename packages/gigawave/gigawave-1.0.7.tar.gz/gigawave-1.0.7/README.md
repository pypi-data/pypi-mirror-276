# GigaWave™ Official Python SDK
Easy-to-use Python interface for [GigaWave™ 6000-Series](https://sjl-instruments.com) Digital Sampling Oscilloscopes.

## Quickstart
Install via `pip3 install gigawave`. The `example.py` file is an easy way to get started:
```python
from gigawave import GigaWave
import numpy as np
import matplotlib.pyplot as plt

# Connect to scope
scope = GigaWave('/dev/ttyUSB0')

# Initialize trigger settings
scope.trigger_direction = 'rising'
scope.trigger_level = 0 # V
scope.trigger_holdoff = 100 # ns

# Read voltage on Channel 1 at T + 50 ns
print(scope.get_voltage(delay=50, channel=1))

# Create time-domain plot
delays = np.linspace(48, 50, 32)
voltages = [scope.get_voltage(delay, channel=1, calibrate_timebase=False) for delay in delays]

plt.plot(delays, voltages)
plt.xlabel('Time [ns]')
plt.ylabel('Voltage [V]')
plt.show()

# Sample CDF for Channel 1 at T + 50 ns
voltages, cdf = scope.get_cdf(delay=50, channel=1)
plt.plot(voltages, cdf)
plt.xlabel('Voltage [V]')
plt.ylabel('CDF Value')
plt.show()
```

## Timebase Calibration
By default, the `get_voltage` and `get_cdf` commands will calibrate the internal timebase on every call.
Acquisition can be significantly sped up by skipping this step (pass `calibrate_timebase = False`).

If this option is used, it is the user's responsibility to calibrate the timebase on a regular basis.
The required calibration frequency will vary depending on the application,
and will decrease as the scope's temperature stabilizes.
