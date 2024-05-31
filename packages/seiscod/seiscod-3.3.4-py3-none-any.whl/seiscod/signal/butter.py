from scipy.signal import butter, sosfilt, sosfreqz
from scipy.fftpack import fftfreq, rfftfreq, rfft, irfft, fft, ifft, fft2, ifft2
import numpy as np

"""
time / fourier domain butterworth filter
warning : the fourier domain filter has a slightly different response that the time domain one
          comparing both reveals that the time domain filter may include a water-level that do not 
          not exist with fourier domain, this results in slight differences near the signal edges
          taper the waveform properly fixes the difference
"""


class ButterworthFilter(object):
    _sos = None
    _sampling_rate = None

    def __init__(self, freqmin, freqmax, sampling_rate, order=4):
        nyquist = 0.5 * sampling_rate
        self._sampling_rate = sampling_rate

        if freqmin is None and freqmax is None:
            raise ValueError(freqmin, freqmax)

        elif freqmin is not None and freqmax is not None:
            self._sos = butter(order, [freqmin / nyquist, freqmax / nyquist],
                               output="sos", btype="band")

        elif freqmin is not None:
            self._sos = butter(order, [freqmin / nyquist],
                               output="sos", btype="high")

        elif freqmax is not None:
            self._sos = butter(order, [freqmax / nyquist],
                               output="sos", btype="low")

        else:
            raise ValueError(freqmin, freqmax)

    def timecall(self, data, zerophase=False, axis=-1):
        filtered_data = sosfilt(sos=self._sos, x=data, axis=axis)
        # filtered_data = lfilter(b=self.b, a=self.a, x=data, axis=axis)

        if zerophase:
            # recall the filter in referse order
            filtered_data = self.__call__(
                data=filtered_data[::-1],
                zerophase=False,
                axis=axis)[::-1]

        return filtered_data

    def response(self, npts, zerophase=False, input_domain="fft", qc=False):
        """ almost equivalent to timecall
         the response looks better than timecall, no water level applied
         """

        if input_domain == "fft":
            freqs = fftfreq(npts, 1. / self._sampling_rate)
            # equivalent to (except for freqs (0 to nyquist, no wrapping))
            # freqs, response = sosfreqz(self._sos, worN=npts, whole=True, fs=self._sampling_rate)

        elif input_domain == "rfft":
            freqs = rfftfreq(npts, 1. / self._sampling_rate)

        else:
            raise NotImplementedError(input_domain)

        _, response = sosfreqz(self._sos, worN=freqs, whole=True, fs=self._sampling_rate)

        if zerophase:
            response = np.abs(response) ** 2.

        if qc:
            import matplotlib.pyplot as plt
            data = np.random.randn(npts)
            filtered_data = self.timecall(data=data, zerophase=zerophase)

            if input_domain == "fft":
                # freqs = fftfreq(npts, 1./self._sampling_rate)
                tfdata = fft(data)
                filtered_tfdata = fft(filtered_data)

            elif input_domain == "rfft":
                # freqs = fftfreq(npts, 1. / self._sampling_rate)
                tfdata = rfft(data)
                filtered_tfdata = rfft(filtered_data)

            else:
                raise NotImplementedError(input_domain)

            expected_response = filtered_tfdata / tfdata

            plt.figure()
            plt.subplot(311, title=f"{zerophase}")
            plt.plot(freqs, expected_response.real, linewidth=3)
            plt.plot(freqs, response.real, linewidth=1)

            plt.subplot(312)
            plt.plot(freqs, expected_response.imag, linewidth=3)
            plt.plot(freqs, response.imag, linewidth=1)

            plt.subplot(313)
            plt.loglog(np.abs(freqs), np.abs(expected_response), linewidth=3)
            plt.loglog(np.abs(freqs), np.abs(response), linewidth=1)
            plt.show()

        return freqs, response

    def __call__(self, data, zerophase=False, axis=-1, input_domain="time"):
        """
        return the filtered data
        can be called on time domain (real or complex) data
        fft or rfft transformed data (use input_domain)
        """
        if input_domain == "time":
            return self.timecall(data=data, zerophase=zerophase, axis=axis)

        elif input_domain in ["fft", "rfft"]:
            _, response = self.response(
                npts=len(data), zerophase=zerophase,
                input_domain=input_domain, qc=False)
            return data * response

        else:
            raise ValueError(input_domain)

    def show(self, fig, freqs=None, zerophase=False, **kwargs):
        freqs, response = sosfreqz(self._sos, worN=freqs, whole=False, fs=self._sampling_rate)

        ax = fig.add_subplot(121)
        bx = fig.add_subplot(122, sharex=ax)

        if zerophase:
            response = np.abs(response) ** 2.0

        ax.loglog(freqs, np.abs(response), **kwargs)
        bx.semilogx(freqs, np.angle(response), **kwargs)

        ax.set_xlabel('frequency (Hz)')
        bx.set_xlabel('frequency (Hz)')
        ax.set_ylabel('response modulus')
        bx.set_ylabel('response phase')
        ax.grid(True, linestyle="--")
        bx.grid(True, linestyle="--")


class BandpassFilter(ButterworthFilter):

    def __init__(self, freqmin, freqmax, sampling_rate, order=4):
        ButterworthFilter.__init__(
            self, freqmin=freqmin, freqmax=freqmax,
            sampling_rate=sampling_rate, order=order)


class LowpassFilter(ButterworthFilter):

    def __init__(self, freqmax, sampling_rate, order=4):
        ButterworthFilter.__init__(
            self, freqmin=None, freqmax=freqmax,
            sampling_rate=sampling_rate, order=order)


class HighpassFilter(ButterworthFilter):

    def __init__(self, freqmin, sampling_rate, order=4):
        ButterworthFilter.__init__(
            self, freqmin=freqmin, freqmax=None,
            sampling_rate=sampling_rate, order=order)


class ButterworthFilter2x1d(object):
    def __init__(self, lmin, lmax, dx, dy, order):
        fmin = 1. / lmax if lmax is not None else None
        fmax = 1. / lmin if lmin is not None else None
        self.filterx = ButterworthFilter(
            freqmin=fmin, freqmax=fmax, sampling_rate=1. / dx, order=order)
        self.filtery = ButterworthFilter(
            freqmin=fmin, freqmax=fmax, sampling_rate=1. / dy, order=order)

    def response(self, nx, ny, zerophase=True, input_domain="fft"):
        freqx, responsex = self.filterx.response(npts=nx, zerophase=zerophase, input_domain=input_domain)
        freqy, responsey = self.filtery.response(npts=ny, zerophase=zerophase, input_domain=input_domain)
        responsey = responsey[:, np.newaxis]
        return freqx, freqy, responsex, responsey

    def __call__(self, data, zerophase=True, input_domain="fft"):
        if input_domain in ["fft", "rfft"]:
            pass
        elif input_domain in ["time", "space"]:
            data = fft2(data)
        else:
            raise ValueError(input_domain)

        ny, nx = data.shape
        freqx, freqy, responsex, responsey = \
            self.response(nx, ny, zerophase=zerophase, input_domain=input_domain)

        data = (data * responsex) * responsey

        if input_domain in ["fft", "rfft"]:
            pass
        elif input_domain in ["time", "space"]:
            data = ifft2(data)
        else:
            raise ValueError(input_domain)

        return data


if __name__ == '__main__':
    from seiscod.signal.taper import cos_taper_width

    npts = 1200
    sampling_rate = 1.0123456
    data = 1.0 * np.random.randn(npts)
    data *= cos_taper_width(len(data), sampling_rate=sampling_rate, width=250.0)

    freqmin = 0.03
    freqmax = 0.08
    fftfreqs = fftfreq(npts, 1. / sampling_rate)

    bp = BandpassFilter(freqmin=freqmin, freqmax=freqmax, sampling_rate=sampling_rate, order=4)

    import matplotlib.pyplot as plt
    bp.show(plt.figure(), zerophase=False)
    bp.show(plt.figure(), zerophase=True)

    plt.figure()
    plt.plot(data, 'k')
    plt.plot(bp(data, zerophase=True), "b", linewidth=3)
    plt.plot(ifft(bp(fft(data), zerophase=True, input_domain="fft")).real, "g-")
    plt.plot(irfft(bp(rfft(data), zerophase=True, input_domain="rfft")).real, "m--")

    plt.show()
