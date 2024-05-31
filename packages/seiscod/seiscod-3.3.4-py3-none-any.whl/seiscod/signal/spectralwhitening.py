import numpy as np
from scipy.fftpack import fft, ifft, fftfreq
from seiscod.signal.fsmooth import fftsmooth
from seiscod.signal.parseval import fft_energy
from seiscod.signal.butter import ButterworthFilter


def spectral_whitening(
        fftdat: np.array, delta: float,
        width_octave: float,
        freqmin: float, freqmax: float,
        zerophase: bool = True,
        order: int = 4,
        water_level: float = 0.001) -> np.ndarray:
    """
    WARNING : this method does not work well in case of very narrow spectral lines !!!
    """

    if width_octave <= 0:
        raise ValueError('width_octave must be > 0')

    fenergy = fft_energy(fftdat, delta=delta)
    if fenergy == 0:
        raise ValueError('the input data cannot be 0')

    modulus = abs(fftdat)
    smooth_modulus = fftsmooth(modulus, delta, width_octave=width_octave)

    # === whiten
    wfftdat = fftdat / (smooth_modulus + modulus.max() * water_level)

    # === bandpass filter
    bp = ButterworthFilter(freqmin=freqmin, freqmax=freqmax, sampling_rate=1. / delta, order=order)
    wfftdat = bp.__call__(data=wfftdat, zerophase=zerophase, input_domain="fft")

    # === equilibrate the energy
    wenergy = fft_energy(wfftdat, delta=delta)
    wfftdat *= np.sqrt(fenergy / wenergy)

    return wfftdat  # complex


def power_whitening(
        fftdat: np.array,
        delta: float,
        power: float,
        freqmin: float, freqmax: float,
        zerophase: bool = True,
        order: int = 4,
        same_power: bool = True,
        ) -> np.ndarray:
    """
    Equalization of spectral amplitudes using a power low
    power = 0 => all spectral components to 1
    power = 1 => no whitening at all
    """

    if not 0 <= power <= 1.:
        raise ValueError('power must be in ] 0 , 1 ]')

    # === whiten
    # wfftdat = np.exp(1.j * np.angle(fftdat)).astype(fftdat.dtype) * np.abs(fftdat) ** power
    modulus = np.abs(fftdat)
    wfftdat = fftdat.copy()

    if modulus.any():
        mask = modulus != 0.

        wfftdat[mask] *= modulus[mask] ** (power - 1.)

        # === bandpass filter in fft domain
        bp = ButterworthFilter(freqmin=freqmin, freqmax=freqmax, sampling_rate=1. / delta, order=order)
        wfftdat = bp.__call__(data=wfftdat, zerophase=zerophase, input_domain="fft")

        # === equilibrate the energy in the band of interest
        if same_power:
            bp_fftdat = bp.__call__(data=fftdat, zerophase=zerophase, input_domain="fft")

            input_energy = \
                fft_energy(bp_fftdat, delta=delta)

            output_energy = \
                fft_energy(wfftdat, delta=delta)

            wfftdat *= np.sqrt(input_energy / output_energy)

    return wfftdat  # complex


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    npts = 1024
    delta = 0.123
    t = np.arange(npts) * delta
    nu = fftfreq(npts, delta)

    data0 = 1 * np.random.randn(npts)

    data1 = 15. * np.random.randn(npts)
    data1 = ifft(fft(data1) * np.exp(-50. * (abs(nu) / 0.5 - 1.0) ** 2.0)).real

    data2 = 15. * np.random.randn(npts)
    data2 = ifft(fft(data2) * np.exp(-50000. * (abs(nu) / 2.5 - 1.0) ** 2.0)).real

    data = (data0 + data1 + data2) * 2e+20
    data = fft(data)
    data[(1.5 <= abs(nu)) & (abs(nu) < 1.8)] = 0.
    data = ifft(data).real

    F = fft(data)

    width_octave = 0.2
    G = fftsmooth(fftdat=np.abs(F), delta=delta, width_octave=width_octave)
    W = spectral_whitening(
        fftdat=F, delta=delta, width_octave=width_octave,
        freqmin=0.1, freqmax=3.0)
    w = ifft(W).real

    P = power_whitening(
        fftdat=F, delta=delta, power=0.2,
        freqmin=0.1, freqmax=3.0)
    p = ifft(P).real

    plt.subplot(211)
    plt.plot(t, data, color="k")
    plt.plot(t, w, color="b")
    plt.plot(t, p, color="m")

    plt.subplot(223)
    plt.plot(nu[:npts//2], abs(F)[:npts//2], color="k")
    plt.plot(nu[:npts//2], G[:npts//2], color="r")
    plt.plot(nu[:npts//2], abs(W)[:npts//2], color="b")
    plt.plot(nu[:npts // 2], abs(P)[:npts // 2], color="m")

    plt.subplot(224)
    plt.loglog(abs(nu), abs(F), color="k")
    plt.loglog(abs(nu), G, color="r")
    plt.loglog(abs(nu), abs(W), color="b")
    plt.loglog(abs(nu), abs(P), color="m")
    plt.show()
