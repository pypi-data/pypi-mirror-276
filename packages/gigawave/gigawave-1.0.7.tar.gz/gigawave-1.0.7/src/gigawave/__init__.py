from typing import Optional, List

import serial
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import erf

from gigawave.exceptions import TriggerError

class GigaWave:
    def __init__(
        self,
        port: str = '/dev/ttyUSB0'
    ):
        self._port = port
        self._init_conn()

        self.calibrate_timebase()

        name = self._query('*IDN?')

        self._n_channels = 8 if '6800' in name else 4

        self.trigger_level = 0
        self.trigger_direction = 'rising'
        self.trigger_holdoff = 50

        self.min_samples = 4096
        self.max_samples = 4000000
        self.samples_per_cdf = 40

        # Read calibration coefficients
        cal_coeffs = list(map(float, self._query('^').split()))
        self._firmware_revision = round(cal_coeffs[0])
        self._serial = round(cal_coeffs[1])
        self._offsets = np.array(cal_coeffs[2:2 + self._n_channels]) + 1 # 1 mV default offset
        self._scales = np.array(cal_coeffs[2 + self._n_channels:])


    def _init_conn(self) -> None:
        """Initialize connection to the scope."""
        self._conn = serial.Serial(self._port, baudrate=921600, timeout=5)
        self._conn.reset_input_buffer()

    def _query(self, command: str) -> str:
        """Send a command and wait for a response."""
        try:
            self._conn.reset_input_buffer()
        except Exception as e: # macOS bug
            print(e)
            self._init_conn()

        self._conn.write((command + '\r').encode('utf-8'))
        return self._conn.readline(8192).decode('utf-8').strip()

    def calibrate_timebase(self) -> None:
        """
        Calibrate the internal timebase.

        :raises AssertionError: If hardware error occurs. Will likely resolve on retry.
        """
        assert self._query('C').startswith('OK CAL')

    def _set_delay(self, delay: float) -> None:
        """
        Sets the post-trigger delay in nanoseconds.

        :param delay:
            The post-trigger delay in nanoseconds to sample at.
            Must be at least 11 and at most `trigger_holdoff - 25`.
        :raises ValueError:
            If outside usable range at the current trigger holdoff.
        :raises AssertionError:
            If outside usable range for current trigger holdoff,
            or hardware error occurs.
        """
        if not (11 <= delay <= self._holdoff - 25):
            raise ValueError(f'Delay must be at least 11 ns and at most `trigger_holdoff - 25` ns.')
        assert self._query(f'D{round(delay*1e4)}').startswith('OK D')

    @property
    def trigger_direction(self) -> str: return self._trigger_direction

    @trigger_direction.setter
    def trigger_direction(self, direction: str):
        """
        Set the trigger direction.

        :param direction: Either 'rising' or 'falling'.
        :raises ValueError:
            If invalid trigger mode is selected.
        :raises AssertionError:
            If hardware error occurs. Will likely resolve on retry.
        """
        if direction not in ['rising', 'falling']:
            raise ValueError('Trigger direction must be `rising` or `falling`.')
        idx = 0 if (direction == 'falling') else 1
        self._trigger_direction = direction
        assert self._query(f'E{idx}').startswith('OK E')

    @property
    def trigger_level(self) -> float: return self._trigger_level

    @trigger_level.setter
    def trigger_level(self, level: float) -> None:
        """
        Set the trigger level in mV.

        :param level: Trigger level in mV. Must be between -950 mV and +950 mV.
        :raises ValueError:
            If trigger level is outside valid range.
        :raises AssertionError:
            If hardware error occurs. Will likely resolve on retry.
        """
        if not (-0.95 <= level <= 0.95):
            raise ValueError('Trigger level must be between -950 mV and +950 mV.')

        bits = round(((level + 15e-3) / 1.5 + 1) * 32768)
        self._trigger_level = level
        assert self._query(f'L{bits}').startswith('OK L')

    @property
    def trigger_holdoff(self) -> float:
        return self._holdoff

    @trigger_holdoff.setter
    def trigger_holdoff(self, holdoff: float) -> None:
        """
        Set the trigger holdoff in nanoseconds.

        :param holdoff: The trigger holdoff in nanoseconds. Must be between 40 ns and 1 ms inclusive.
        :raises ValueError: If holdoff is shorter than 40 ns or longer than 1 ms.
        :raises AssertionError: If hardware error occurs. Will likely resolve on retry.
        """
        if not (40 <= holdoff <= 1e6):
            raise ValueError(f'Valid holdoff range is 40 ns to 1 ms.')

        self._holdoff = holdoff
        assert self._query(f'H{holdoff:.0f}').startswith('OK H')

    @property
    def min_samples(self) -> int:
        """
        The minimum number of triggers used to acquire each CDF sample.
        """
        return self._min_samples

    @min_samples.setter
    def min_samples(self, n: int) -> None:
        """
        Sets the number of triggers used to acquire each CDF sample.
        Must be between 5 and 30000 inclusive.
        """
        if not (5 <= n <= 30000):
            raise ValueError(f'Minimum number of samples must be between 5 and 30000.')

        self._min_samples = n
        assert self._query(f'S{n}').startswith('OK S')

    @property
    def max_samples(self) -> int:
        """
        The maximum number of triggers used to acquire each CDF sample.
        """
        return self._max_samples

    @max_samples.setter
    def max_samples(self, n: int) -> None:
        """
        Sets the number of triggers used to acquire each CDF sample.
        Must be between 5 and 4 billion inclusive.
        """
        if not (5 <= n <= 4000000000):
            raise ValueError(f'Maximum number of samples must be between 5 and 4 billion.')

        self._max_samples = n
        assert self._query(f'${n}').startswith('OK $')

    @property
    def samples_per_cdf(self) -> int:
        """
        The number of sample voltages to acquire per CDF.
        """
        return self._samples_per_cdf

    @samples_per_cdf.setter
    def samples_per_cdf(self, n: int) -> None:
        """
        Sets the number of sample voltages to acquire per CDF.
        Must be between 5 and 100 inclusive.
        """
        if not (5 <= n <= 100):
            raise ValueError(f'Number of samples must be between 5 and 100.')

        self._samples_per_cdf = n
        assert self._query(f'Q{n}').startswith('OK Q')

    def get_voltage(
        self,
        delay: float,
        channel: Optional[int] = None,
        calibrate_timebase: bool = True,
    ) -> float | List[float]:
        """
        :param delay: The post-trigger delay in nanoseconds to sample at.
        :param channel: The channel to sample, or None to sample all channels.
        :param calibrate_timebase:
            [Advanced feature] Whether to calibrate timebase prior to sampling.
            Disabling calibration can significantly speed up acquisition.
            If False, the user is responsible for calling calibrate_timebase() at regular intervals.
        :returns: The voltage on the specified channel at the specified post-trigger delay,
            or a list of voltages on each channel (if no channel is specified).
        :raises gigawave.exceptions.TriggerError: If trigger is missing.
        :raises AssertionError: If hardware error occurs. Will likely resolve on retry.
        """
        assert (channel is None) or 1 <= channel <= self._n_channels

        if calibrate_timebase: self.calibrate_timebase()
        self._set_delay(delay)

        def model(x, loc, scale):
            return erf((x-loc)/scale)

        x, y, _ = self._get_cdf()
        voltages = []
        for xx, yy in zip(x, y):
            est = np.interp(0.5, yy, xx)
            try:
                refinement = curve_fit(model, xx, yy, p0=[est, 0.1])[0][0]
                if abs(refinement - est) < 0.01: est = refinement
            except (ValueError, RuntimeError):
                pass
            voltages.append(est)

        if channel is None:
            return voltages
        else:
            return voltages[channel-1]

    def get_cdf(
        self,
        delay: float,
        channel: Optional[int] = None,
        calibrate_timebase: bool = True,
    ) -> np.ndarray:
        """
        :param delay: The post-trigger delay in nanoseconds to sample at.
        :param channel: The channel to sample, or None to sample all channels.
        :param calibrate_timebase:
            [Advanced feature] Whether to calibrate timebase prior to sampling.
            Disabling calibration can significantly speed up acquisition.
            If False, the user is responsible for calling calibrate_timebase() at regular intervals.
        :returns:
            If channel is specified, returns a 2xN array [voltages, cdf_values].
            If no channel is specified, returns an Mx2xN array [[voltages, cdf_values] for each channel].
        :raises gigawave.exceptions.TriggerError: If trigger is missing.
        :raises AssertionError: If hardware error occurs. Will likely resolve on retry.
        """
        assert (channel is None) or 1 <= channel <= self._n_channels

        if calibrate_timebase: self.calibrate_timebase()
        self._set_delay(delay)

        x, y, _ = self._get_cdf()
        samples = np.array([x, y]).swapaxes(0, 1)
        if channel is None:
            return samples
        else:
            return samples[channel-1]

    def _get_cdf(self):
        # DAC bounds for full input range
        channel_bounds = np.array([[10000, 55000]] * self._n_channels).T
        channel_string = ' '.join(map(str, channel_bounds.flatten()))

        read_string = {
            2: b'R3',
            4: b'R15',
            8: b'R255',
        }[self._n_channels]
        sentry = b'SJLI'

        self._conn.write(read_string + b' ' + channel_string.encode('utf-8') + b'\r')
        raw_data = self._conn.read_until(sentry)
        if raw_data.startswith(b'NO TRIG'): raise TriggerError('No trigger detected!')
        if not raw_data.endswith(sentry): raise AssertionError('CDF read failed! [Sentry missing]')

        for header_length in [34, 35]: # Try both header lengths for different firmware revisions
            prefix, data = raw_data[:header_length].strip().split(b' '), raw_data[header_length:-len(sentry)]
            if len(prefix) != 5: raise AssertionError('CDF read failed! [Incorrect prefix length]')
            samples, sysclk_time, tot_cycles, N = int(prefix[1]), int(prefix[2]), int(prefix[3]), int(prefix[4])
            sample_rate = samples/sysclk_time

            if len(data) != self._n_channels*3*N:
                if header_length == 34: continue
                raise AssertionError('CDF read failed! [Incorrect data length]')

            break

        # Parse array
        dt = np.dtype(np.uint8)
        data = np.frombuffer(data, dt)
        data = data.reshape((-1, self._n_channels, 3))

        ys = 1.5*((data[:, :, 0]/128. + data[:, :, 1]/32768.) - 1)
        ys = ys * self._scales - self._offsets * 1e-3
        cdfs = data[:, :, 2]/255.
        ys = ys.T
        cdfs = 1-cdfs.T
        return np.array([
            [-1.1, *row, 1.1] for row in ys
        ]), np.array([
            [row[0], *row, row[-1]] for row in cdfs
        ]), sample_rate
